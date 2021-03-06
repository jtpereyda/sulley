import ifuzz_logger


def failure_summary(fl):
    """
    Return test summary string based on fuzz_logger's results.

    :type fl: FuzzLogger
    :param fl: Provides test results data.

    :return: Test summary string, may be multi-line.
    """
    summary = "Test Summary: {0} tests ran.\n".format(len(fl.all_test_cases))
    summary += "PASSED: {0} test cases.\n".format(len(fl.passed_test_cases))

    if len(fl.failed_test_cases) > 0:
        summary += "FAILED: {0} test cases:\n".format(len(fl.failed_test_cases))
        summary += "{0}\n".format('\n'.join(map(str, fl.failed_test_cases.iterkeys())))

    if len(fl.error_test_cases) > 0:
        summary += "Errors on {0} test cases:\n".format(len(fl.error_test_cases))
        summary += "{0}".format('\n'.join(map(str, fl.error_test_cases.iterkeys())))

    return summary


class FuzzLogger(ifuzz_logger.IFuzzLogger):
    """
    Implementation for IFuzzLogger.

    FuzzLogger takes logged data and directs it to the appropriate backends.
    It aggregates an arbitrary number of logger backends, and functions like a
    multiplexer.

    FuzzLogger also maintains failure and error data.
    """

    def __init__(self, fuzz_loggers=None):
        if fuzz_loggers is None:
            fuzz_loggers = []
        self._fuzz_loggers = fuzz_loggers

        self._cur_test_case_id = ''
        self.failed_test_cases = {}
        self.error_test_cases = {}
        self.passed_test_cases = {}
        self.all_test_cases = []

    def open_test_step(self, description):
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.open_test_step(description=description)

    def log_error(self, description):
        if self._cur_test_case_id not in self.error_test_cases:
            self.error_test_cases[self._cur_test_case_id] = []
        self.error_test_cases[self._cur_test_case_id].append(description)
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.log_error(description=description)

    def log_fail(self, description=""):
        if self._cur_test_case_id not in self.failed_test_cases:
            self.failed_test_cases[self._cur_test_case_id] = []
        self.failed_test_cases[self._cur_test_case_id].append(description)
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.log_fail(description=description)

    def log_info(self, description):
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.log_info(description=description)

    def log_recv(self, data):
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.log_recv(data=data)

    def log_pass(self, description=""):
        if self._cur_test_case_id not in self.passed_test_cases:
            self.passed_test_cases[self._cur_test_case_id] = []
        self.passed_test_cases[self._cur_test_case_id].append(description)
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.log_pass(description=description)

    def log_check(self, description):
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.log_check(description=description)

    def open_test_case(self, test_case_id):
        self._cur_test_case_id = test_case_id
        self.all_test_cases.append(test_case_id)
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.open_test_case(test_case_id=test_case_id)

    def log_send(self, data):
        for fuzz_logger in self._fuzz_loggers:
            fuzz_logger.log_send(data=data)
