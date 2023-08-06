from system_monitor.failure_manager_based_on_db import FailureManagerBasedOnDatabase
from ufs_tools.short_decorator.ignore_exception import ignore_exc
from post_office.utils import send_mail


class MonitorBase(object):
    def is_healthy(self):
        raise NotImplemented


class FailureEmail(object):
    def __init__(self, title, target):
        super(FailureEmail, self).__init__()
        self.title = title
        self.target = target


class RecoverableEventMonitor(object):

    def __init__(self, monitor, target_email=None):
        super(RecoverableEventMonitor, self).__init__()
        self.monitor = monitor
        self.target_email = target_email
        self.event_storage = FailureManagerBasedOnDatabase(monitor.failure_event_name)

    def check_monitor_once(self):
        """
        Check the monitor once, if the monitor
        :return:
        """
        if self.monitor.is_healthy():
            self.event_storage.clear_failure()
        else:
            if self.event_storage.is_alarm_needed():
                self.gui_notify(self.monitor.error_title)
                if self.target_email is not None:
                    send_mail(from_email=self.target_email,
                              recipient_list=[self.target_email],
                              subject=self.monitor.error_title)

    @ignore_exc
    def gui_notify(self, text):
        from iconizer.gui_client.notification_service_client import NotificationServiceClient
        ui_service = NotificationServiceClient()
        ui_service.notify()
