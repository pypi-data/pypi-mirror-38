from django.utils import timezone
from pinax.eventlog.models import log, Log


class FailureManagerBasedOnDatabase(object):
    def __init__(self, failure_name):
        super(FailureManagerBasedOnDatabase, self).__init__()
        self.failure_name = failure_name
        self.tolerable_failure_cnt = 10

    def is_alarm_needed(self):
        log(
            user=None,
            action=self.failure_name,
            obj=None,
            extra={
                "status": "failed"
            }
        )
        q = Log.objects.filter(action=self.failure_name).order_by("-timestamp")

        if q.count() > self.tolerable_failure_cnt:
            cnt = 0
            for log_record in q:
                if log_record.extra["status"] == "cleared":
                    return False
                cnt += 1
                if cnt >= self.tolerable_failure_cnt:
                    timestamp = q[self.tolerable_failure_cnt].timestamp
                    if self.is_within_minutes(timestamp):
                        return True
                    else:
                        return False
        return False

    # noinspection PyMethodMayBeStatic
    def is_within_minutes(self, timestamp, limit=15):
        return timestamp + timezone.timedelta(minutes=limit) > timezone.now()

    def clear_failure(self):
        log(
            user=None,
            action=self.failure_name,
            obj=None,
            extra={
                "status": "cleared"
            }
        )

