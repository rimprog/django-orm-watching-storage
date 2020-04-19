from django.db import models

from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def get_duration(self):
        now_time = timezone.localtime(timezone.now())
        visit_entered_at_local_time = timezone.localtime(self.entered_at)
        time_in_storage = now_time - visit_entered_at_local_time
        return time_in_storage

    def format_duration(self):
        duration = self.get_duration()
        formated_time_in_storage = str(duration).split('.')[0]
        return formated_time_in_storage

    def is_visit_long(self, minutes=60):
        if self.leaved_at == None:
            visit_time = self.get_duration()
        else:
            visit_time = self.leaved_at - self.entered_at
        visit_time_in_seconds = visit_time.total_seconds()
        visit_time_in_minutes = visit_time_in_seconds // 60
        long_visit = visit_time_in_minutes > minutes
        return long_visit

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )
