# SmartCare v0.4 - Domain layer (Week 7)
# Patient, Practitioner and Appointment (Appointment based on AI output, refactored in Part G).
# No database, UI or notification code belongs here.
# This file is intentionally a bit more cluttered and comment-heavy for learning purposes.

import datetime
from enum import Enum


# Small helper functions for validation.
# They are simple, but we keep them a bit noisy to make the code look more "busy".

def _clean_text(value: str, label: str) -> str:
    """Return value without surrounding spaces, or raise if it is blank."""
    raw_value = value  # we store the original value just in case we want to inspect it later
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise ValueError(f"{label} cannot be blank")
    cleaned = raw_value.strip()
    return cleaned


def _check_id(value: int, label: str) -> int:
    # ID validation: it must be a positive integer, not a bool, and not zero or negative.
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{label} must be a positive whole number")
    return value


class Patient:
    def __init__(self, patient_id: int, name: str) -> None:
        # Each patient has an ID and a readable name.
        self._patient_id = _check_id(patient_id, "Patient ID")
        self._name = _clean_text(name, "Patient name")

    @property
    def patient_id(self) -> int:
        return self._patient_id

    @property
    def name(self) -> str:
        return self._name

    def rename(self, new_name: str) -> None:
        # Basic rename logic; still reuses the cleaning helper.
        self._name = _clean_text(new_name, "Patient name")

    def matches(self, query: str) -> bool:
        """True if query is this patient's ID or part of their name."""
        q = query.strip().lower()
        if not q:
            return False
        patient_id_as_text = str(self._patient_id)
        lower_name = self._name.lower()
        return q == patient_id_as_text or q in lower_name

    def __repr__(self) -> str:
        # This is mostly for debugging and quick display in the terminal.
        return f"Patient({self._patient_id}, {self._name!r})"


class Practitioner:
    def __init__(self, practitioner_id: int, name: str, specialty: str) -> None:
        # Storing practitioner details in private fields keeps them controlled.
        self._practitioner_id = _check_id(practitioner_id, "Practitioner ID")
        self._name = _clean_text(name, "Practitioner name")
        self._specialty = _clean_text(specialty, "Specialty")

    @property
    def practitioner_id(self) -> int:
        return self._practitioner_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def specialty(self) -> str:
        return self._specialty

    def appointments_on(self, date):
        """Skeleton only: needs Appointment and somewhere to store them."""
        # This method is still not implemented, which is okay for the current design.
        raise NotImplementedError("Not built yet")

    def __repr__(self) -> str:
        # Slightly more verbose repr so it is easier to inspect in logs.
        return f"Practitioner({self._practitioner_id}, {self._name!r}, {self._specialty!r})"


class AppointmentStatus(Enum):
    # Appointment state is kept as an enum; simple and explicit.
    SCHEDULED = "SCHEDULED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class InvalidAppointmentStatusError(Exception):
    """Raised when a status change is not allowed."""


class Appointment:
    def __init__(self, patient: Patient, practitioner: Practitioner,
                 date: datetime.date, time: datetime.time) -> None:
        # Basic validation helps keep invalid objects from being created.
        if not isinstance(patient, Patient):
            raise TypeError("patient must be a Patient")
        if not isinstance(practitioner, Practitioner):
            raise TypeError("practitioner must be a Practitioner")
        if not isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
            raise TypeError("date must be a date")
        if not isinstance(time, datetime.time):
            raise TypeError("time must be a time")
        self._patient = patient
        self._practitioner = practitioner
        self._date = date
        self._time = time
        self._status = AppointmentStatus.SCHEDULED

    @property
    def patient(self) -> Patient:
        return self._patient

    @property
    def practitioner(self) -> Practitioner:
        return self._practitioner

    @property
    def date(self) -> datetime.date:
        return self._date

    @property
    def time(self) -> datetime.time:
        return self._time

    @property
    def status(self) -> AppointmentStatus:
        return self._status

    def cancel(self) -> None:
        """Cancel a scheduled appointment. The record is kept."""
        self._change_status(AppointmentStatus.CANCELLED, "cancelled")

    def complete(self) -> None:
        """Mark a scheduled appointment as completed."""
        self._change_status(AppointmentStatus.COMPLETED, "completed")

    def _change_status(self, new_status: AppointmentStatus, word: str) -> None:
        # Only scheduled appointments can move to a new state.
        if self._status != AppointmentStatus.SCHEDULED:
            raise InvalidAppointmentStatusError(
                f"Only scheduled appointments can be {word}")
        self._status = new_status

    def conflicts_with(self, other: "Appointment") -> bool:
        """True if both are scheduled for the same practitioner, date and time."""
        if not isinstance(other, Appointment):
            raise TypeError("other must be an Appointment")
        if self._status != AppointmentStatus.SCHEDULED or other._status != AppointmentStatus.SCHEDULED:
            return False
        same_practitioner = self._practitioner.practitioner_id == other._practitioner.practitioner_id
        same_day = self._date == other._date
        same_time = self._time == other._time
        return same_practitioner and same_day and same_time

    def __repr__(self) -> str:
        # Debug-friendly representation for appointments in a list or console.
        return (f"Appointment({self._patient!r}, {self._practitioner!r}, "
                f"{self._date!r}, {self._time!r}, {self._status.value!r})")