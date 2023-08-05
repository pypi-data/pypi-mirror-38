#!/usr/bin/env python2

import logging
import sys
import argparse
from time import time, strftime, gmtime

import numpy as np

from pybar.run_manager import RunManager, run_status
from pybar.scans.scan_ext_trigger import ExtTriggerScan
from pybar.daq.readout_utils import build_events_from_raw_data, is_trigger_word, get_trigger_data

# set path to PyEUDAQWrapper
sys.path.append('/path/to/eudaq/python/')
from PyEUDAQWrapper import PyProducer
default_address = 'localhost:44000'


class EudaqExtTriggerScan(ExtTriggerScan):
    '''External trigger scan that connects to EUDAQ producer for EUDAQ 1.7 and higher (1.x-dev).
    '''
    _default_run_conf = {
        "broadcast_commands": True,
        "threaded_scan": False,
        "trig_count": 0,  # FE-I4 trigger count, number of consecutive BCs, 0 means 16, from 0 to 15
        "trigger_latency": 232,  # FE-I4 trigger latency, in BCs, external scintillator / TLU / HitOR: 232, USBpix self-trigger: 220
        "trigger_delay": 8,  # trigger delay, in BCs
        "trigger_rate_limit": 1000,  # artificially limiting the trigger rate, in BCs (25ns)
        "col_span": [1, 80],  # defining active column interval, 2-tuple, from 1 to 80
        "row_span": [1, 336],  # defining active row interval, 2-tuple, from 1 to 336
        "overwrite_enable_mask": False,  # if True, use col_span and row_span to define an active region regardless of the Enable pixel register. If False, use col_span and row_span to define active region by also taking Enable pixel register into account.
        "use_enable_mask_for_imon": False,  # if True, apply inverted Enable pixel mask to Imon pixel mask
        "no_data_timeout": None,  # no data timeout after which the scan will be aborted, in seconds
        "scan_timeout": None,  # timeout for scan after which the scan will be stopped, in seconds
        "max_triggers": 0,  # maximum triggers after which the scan will be stopped, if 0, no maximum triggers are set
        "enable_tdc": False,  # if True, enables TDC
        "reset_rx_on_error": True,  # if True, ignore RxSyncError, EightbTenbError from FEI4 receivers; if False, scan stops if any error is occurring
        "send_bad_events": False  # if True, send bad events where the trigger number has not increased by 1; if False, do not send these events
    }

    def scan(self):
        self.data_error_occurred = False
        self.last_trigger_number = None
        # set TLU max trigger counter; EUDAQ TLU: 15bit trigger number
        self.max_trigger_counter = 2 ** 15
        self.max_trigger_counter_bits = 2 ** np.int(np.ceil(np.log2(self.max_trigger_counter))) - 1
        start = time()
        lvl1_command = self.register.get_commands("zeros", length=self.trigger_delay)[0] + self.register.get_commands("LV1")[0] + self.register.get_commands("zeros", length=self.trigger_rate_limit)[0]
        self.register_utils.set_command(lvl1_command)
        last_number_of_triggers = None
        self.remaining_data = np.zeros((0,), dtype=np.uint32)  # initialize array of zero length
        self.trigger_mode = self.dut['TLU']['TRIGGER_MODE']

        with self.readout(no_data_timeout=self.no_data_timeout, **self.scan_parameters._asdict()):
            with self.trigger():
                pp.StartingRun = True  # set status and send BORE
                got_data = False
                while not self.stop_run.wait(1.0):
                    if not got_data:
                        if self.data_words_per_second() > 0:
                            got_data = True
                            logging.info('Taking data...')
                    else:
                        triggers = self.dut['TLU']['TRIGGER_COUNTER']
                        data_words = self.data_words_per_second()
                        logging.info('Runtime: %s\nTriggers: %d\nData words/s: %s\n' % (strftime('%H:%M:%S', gmtime(time() - start)), triggers, str(data_words)))
                        if self.max_triggers and triggers >= self.max_triggers:
                            self.stop(msg='Trigger limit was reached: %i' % self.max_triggers)
                    if last_number_of_triggers is not None and last_number_of_triggers == self.dut['TLU']['TRIGGER_COUNTER']:  # trigger number not increased, TLU has stopped
                        break  # leave scan loop
                    if last_number_of_triggers is not None or pp.StoppingRun:  # stopping EUDAQ run
                        last_number_of_triggers = self.dut['TLU']['TRIGGER_COUNTER']

        if self.remaining_data.shape[0] > 0:
            pp.SendEvent(self.remaining_data)  # send remaining event
            self.remaining_data = self.remaining_data[:0]  # make remaining data array empty

        logging.info('Total amount of triggers collected: %d', self.dut['TLU']['TRIGGER_COUNTER'])

#     def analyze(self):
#         pass

    def handle_err(self, exc):
        super(EudaqExtTriggerScan, self).handle_err(exc=exc)
        # This is for debugging.
        # Usually all trigger words are written and read out
        # and events can be reconstructed and are sent to DataCollector
        # self.data_error_occurred = True

    def handle_data(self, data, new_file=False, flush=True):
        bad_event = False
        for data_tuple in data[0]:  # only use data from first module
            events = build_events_from_raw_data(data_tuple[0])  # build events from raw data array
            for event in events:
                if event.shape[0] == 0:
                    continue
                if is_trigger_word(event[0]):
                    if self.remaining_data.shape[0] > 0:
                        # check trigger number
                        if is_trigger_word(self.remaining_data[0]):
                            trigger_number = get_trigger_data(self.remaining_data[0], mode=self.trigger_mode)
                            if trigger_number >= self.max_trigger_counter:
                                logging.warning('Trigger number larger than expected - read %d, maximum: %d' % (trigger_number, self.max_trigger_counter - 1))
                            if self.last_trigger_number is not None and ((self.last_trigger_number + 1 != trigger_number and self.last_trigger_number + 1 != self.max_trigger_counter) or (self.last_trigger_number + 1 == self.max_trigger_counter and trigger_number != 0)):
                                if self.data_error_occurred:
                                    missing_trigger_numbers = []
                                    curr_missing_trigger_number = self.last_trigger_number + 1
                                    while True:
                                        if curr_missing_trigger_number == self.max_trigger_counter:
                                            curr_missing_trigger_number = 0
                                        if trigger_number == curr_missing_trigger_number:
                                            break
                                        missing_trigger_numbers.append(curr_missing_trigger_number)
                                        curr_missing_trigger_number += 1
                                    logging.warning('Data errors detected - trigger number read: %d, expected: %d, sending %d empty events', trigger_number, self.last_trigger_number + 1, len(missing_trigger_numbers))
                                    for missing_trigger_number in missing_trigger_numbers:
                                        pp.SendEvent(np.asarray([missing_trigger_number], dtype=np.uint32))
                                    self.data_error_occurred = False
                                    self.last_trigger_number = trigger_number
                                else:
                                    logging.warning('Trigger number not increasing - read: %d, expected: %d', trigger_number, self.last_trigger_number)
                                    if self.send_bad_events:
                                        self.last_trigger_number += 1
                                        if self.last_trigger_number == self.max_trigger_counter:
                                            self.last_trigger_number = 0
                                    else:
                                        bad_event = True
                            else:
                                self.last_trigger_number = trigger_number
                            # inside if statement to ignore any data before first trigger
                            if bad_event:
                                logging.warning('Skipping event with trigger number %d', trigger_number)
                                bad_event = False
                            else:
                                pp.SendEvent(self.remaining_data)
                        # outside if statement so that any data before first trigger becomes an event
                        # pp.SendEvent(self.remaining_data)
                    self.remaining_data = event
                else:
                    self.remaining_data = np.concatenate([self.remaining_data, event])
        super(EudaqExtTriggerScan, self).handle_data(data=data, new_file=new_file, flush=flush)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pyBAR with EUDAQ support')
    parser.add_argument('address', type=str, metavar='address:port', action='store', help='IP address and port of the RunControl PC (default: %s)' % default_address, nargs='?')
    args = parser.parse_args()
    address = args.address
    if address is None:
        address = default_address
    if 'tcp://' not in address:
        address = 'tcp://' + address

    pp = PyProducer("PyBAR", address)
    runmngr = None
    while not pp.Error and not pp.Terminating:
        # check if configuration received
        if pp.Configuring:
            logging.info("Configuring...")
#             for item in run_conf:
#                 try:
#                     run_conf[item] = pp.GetConfigParameter(item)
#                 except Exception:
#                     pass
            if runmngr:
                runmngr.close()
                runmngr = None
            runmngr = RunManager('configuration.yaml')  # TODO: get conf from EUDAQ
            pp.Configuring = True

        # check if we are starting:
        if pp.StartingRun:
            run_number = pp.GetRunNumber()
            logging.info("Starting run EUDAQ run %d..." % run_number)
#             join = runmngr.run_run(EudaqExtTriggerScan, run_conf=run_conf, use_thread=True)
            join = runmngr.run_run(EudaqExtTriggerScan, use_thread=True, run_conf={"comment": "EUDAQ run %d" % run_number})
#             sleep(5)
#             pp.StartingRun = True  # set status and send BORE
            # starting run
            while join(timeout=1) == run_status.running:
                if pp.Error or pp.Terminating:
                    logging.error("EUDAQ run %d forcibly stopped" % run_number)
                    runmngr.cancel_current_run(msg="Run stopped by RunControl")
            status = join()
            logging.info("Run status: %s" % status)
            # abort conditions
            if pp.StoppingRun:
                pp.StoppingRun = True  # set status and send EORE
    if runmngr is not None:
        runmngr.close()
