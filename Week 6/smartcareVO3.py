# SmartCare v0.3 - Domain class skeletons (Week 6)
# Behaviour is intentionally not implemented yet.

class Patient:
    def __init__(self, patient_id, name):
        self.patient_id = patient_id
        self.name = name

    def matches(self, query):
        """Return True if query matches this patient's ID or name."""
        pass


class Practitioner:
    def __init__(self, practitioner_id, name):
        self.practitioner_id = practitioner_id
        self.name = name

    def appointments_on(self, date):
        """Return this practitioner's appointments for a date."""
        pass


class Appointment:
    def __init__(self, patient, practitioner, date, time, status="Booked"):
        self.patient = patient
        self.practitioner = practitioner
        self.date = date
        self.time = time
        self.status = status  # Booked, Cancelled or Completed

    def cancel(self):
        """Mark the appointment as Cancelled (record is kept)."""
        pass

    def conflicts_with(self, other):
        """Return True if other is for the same practitioner, date and time."""
        pass


class AppointmentBook:  # optional class
    def __init__(self):
        self.appointments = []

    def add(self, appointment):
        """Add an appointment, rejecting practitioner conflicts."""
        pass