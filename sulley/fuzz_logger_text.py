from __future__ import print_function

import sys
import time

from sulley import helpers
from sulley import ifuzz_logger_backend


def hex_to_hexstr(input_bytes):
    """
    Render input_bytes as ASCII-encoded hex bytes, followed by a best effort
    utf-8 rendering.

    @param input_bytes: Arbitrary bytes.

    @return: Printable string.
    """
    return helpers.hex_str(input_bytes) + " '" + bytes(input_bytes) + "'"


DEFAULT_HEX_TO_STR = hex_to_hexstr


def get_time_stamp():
    t = time.time()
    s = time.strftime("[%Y-%m-%d %H:%M:%S", time.localtime(t))
    s += ",%03d]" % (t * 1000 % 1000)
    return s


class FuzzLoggerText(ifuzz_logger_backend.IFuzzLoggerBackend):
    """
    This class formats FuzzLogger data for text presentation. It can be
    configured to output to STDOUT, or to a named file.

    Using two FuzzLoggerTexts, a FuzzLogger instance can be configured to output to
    both console and file.
    """
    TEST_CASE_FORMAT = "Test Case: {0}"
    TEST_STEP_FORMAT = "Test Step: {0}"
    LOG_ERROR_FORMAT = "Error!!!! {0}"
    LOG_CHECK_FORMAT = "Check: {0}"
    LOG_INFO_FORMAT = "Info: {0}"
    LOG_PASS_FORMAT = "Check OK: {0}"
    LOG_FAIL_FORMAT = "Check Failed: {0}"
    LOG_RECV_FORMAT = "Received: {0}"
    LOG_SEND_FORMAT = "Transmitting {0} bytes: {1}"
    DEFAULT_TEST_CASE_ID = "DefaultTestCase"
    INDENT_SIZE = 2

    def __init__(self, file_handle=sys.stdout, bytes_to_str=DEFAULT_HEX_TO_STR):
        """
        @type file_handle: io.FileIO
        @param file_handle: Open file handle for logging. Defaults to sys.stdout.

        @type bytes_to_str: function
        @param bytes_to_str: Function that converts sent/received bytes data to string for logging.
        """
        self._file_handle = file_handle
        self._format_raw_bytes = bytes_to_str
        self._indent_level = 0

    def open_test_step(self, description):
        self._indent_level = self.INDENT_SIZE
        self._print_log_msg(self.TEST_STEP_FORMAT.format(description))

    def log_check(self, description):
        self._indent_level = 2 * self.INDENT_SIZE
        self._print_log_msg(self.LOG_CHECK_FORMAT.format(description))

    def log_error(self, description):
        self._indent_level = 2 * self.INDENT_SIZE
        self._print_log_msg(self.LOG_ERROR_FORMAT.format(description))

    def log_recv(self, data):
        self._indent_level = 2 * self.INDENT_SIZE
        self._print_log_msg(self.LOG_RECV_FORMAT.format(self._format_raw_bytes(data)))

    def log_send(self, data):
        self._indent_level = 2 * self.INDENT_SIZE
        self._print_log_msg(
            self.LOG_SEND_FORMAT.format(len(data), self._format_raw_bytes(data)))

    def log_info(self, description):
        self._indent_level = 2 * self.INDENT_SIZE
        self._print_log_msg(self.LOG_INFO_FORMAT.format(description))

    def open_test_case(self, test_case_id):
        self._indent_level = 0
        self._print_log_msg(self.TEST_CASE_FORMAT.format(test_case_id))

    def log_fail(self, description=""):
        self._indent_level = 3 * self.INDENT_SIZE
        self._print_log_msg(self.LOG_FAIL_FORMAT.format(description))

    def log_pass(self, description=""):
        self._indent_level = 3 * self.INDENT_SIZE
        self._print_log_msg(self.LOG_PASS_FORMAT.format(description))

    def _print_log_msg(self, msg):
        msg = indent_all_lines(msg, self._indent_level)
        time_stamp = get_time_stamp()
        print(time_stamp + ' ' + indent_after_first_line(msg, len(time_stamp) + 1), file=self._file_handle)


def indent_all_lines(lines, amount, ch=' '):
    padding = amount * ch
    return padding + ('\n'+padding).join(lines.split('\n'))


def indent_after_first_line(lines, amount, ch=' '):
    padding = amount * ch
    return ('\n'+padding).join(lines.split('\n'))
