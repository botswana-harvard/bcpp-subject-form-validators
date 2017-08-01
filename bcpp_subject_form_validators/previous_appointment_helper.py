import arrow


class PreviousAppointmentHelper:

    def __init__(self, subject_visit=None, **kwargs):
        self.subject_visit = subject_visit
        self.previous_appointment = (
            self.subject_visit.appointment.previous_by_timepoint)
        if self.previous_appointment:
            rdate = arrow.Arrow.fromdatetime(
                self.previous_appointment.appt_datetime,
                tzinfo=self.previous_appointment.appt_datetime.tzinfo)
        else:
            rdate = None
        self.previous_appointment_rdate = rdate
