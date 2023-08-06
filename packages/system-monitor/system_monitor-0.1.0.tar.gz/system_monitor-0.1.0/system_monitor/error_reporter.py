from django.contrib.contenttypes.models import ContentType
from pinax.eventlog.models import log, Log
from post_office.utils import send_mail


class EventReporter(object):
    action_for_reported_failure = "failure_occurred"
    action_for_clearing_failure = "failure_cleared"

    def __init__(self, obj, recipient):
        super(EventReporter, self).__init__()
        self.obj = obj
        self.recipient = recipient

    def report_success(self, title_base_message):
        is_last_event_a_failure_report = self.is_last_event_same_as(EventReporter.action_for_reported_failure)
        event = log(
            user=None,
            action=EventReporter.action_for_clearing_failure,
            obj=self.obj)
        if is_last_event_a_failure_report:
            send_mail(from_email=self.recipient, recipient_list=[self.recipient],
                      subject="ID %d: %s" % (event.id, title_base_message), message="ID: %d")

    def report_error(self, title_base_message, exception_msg):
        is_last_event_a_clear_failure = self.is_last_event_same_as(EventReporter.action_for_clearing_failure)
        event = log(
            user=None,
            action=EventReporter.action_for_reported_failure,
            obj=self.obj)
        if is_last_event_a_clear_failure:
            send_mail(from_email=self.recipient, recipient_list=[self.recipient],
                      subject="ID %d: %s" % (event.id, title_base_message), message=exception_msg)

    def is_last_event_same_as(self, expected_event):
        events = Log.objects.filter(content_type=ContentType.objects.get_for_model(ContentType).id,
                                    object_id=self.obj.id,
                                    ).order_by("-timestamp")
        return events.exists() and events[0].action == expected_event
