

class FailureManager(object):
    def __init__(self, failure_name):
        super(FailureManager, self).__init__()
        self.failure_cnt = 0
        self.tolerable_failures = 3

    def report_failure(self):
        self.failure_cnt += 1
        if self.failure_cnt > self.tolerable_failures:
            return True
        return False

    def clear_failure(self):
        self.failure_cnt = 0
