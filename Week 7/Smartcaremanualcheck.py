# Manual checks for the SmartCare domain model.
# These examples confirm that validation and state rules work as expected.

import datetime
from smartcare_v04 import (
    Patient,
    Practitioner,
    Appointment,
    AppointmentStatus,
    InvalidAppointmentStatusError,
)

# 1. Valid objects
patient = Patient(1, "Alice Smith")
practitioner = Practitioner(1, "Dr. John Doe", "General practice")
print("--- valid objects ---")
print(patient, practitioner)
print("matches 'alice':", patient.matches("alice"))
print("matches '1':", patient.matches("1"))
print("matches 'bob':", patient.matches("bob"))

# 2. Invalid input should be rejected
print("--- invalid input ---")
examples = [
    ("blank patient name", lambda: Patient(2, "   ")),
    ("patient ID 0", lambda: Patient(0, "Bob")),
    ("patient ID as text", lambda: Patient("3", "Bob")),
    ("blank specialty", lambda: Practitioner(2, "Dr. Jane Roe", "")),
]

for label, make in examples:
    try:
        make()
        print(label, "-> ACCEPTED (problem)")
    except ValueError as error:
        print(label, "-> rejected:", error)

# 3. Read-only properties and rename logic
print("--- protected state ---")
try:
    patient.patient_id = 99
except AttributeError:
    print("patient_id cannot be changed: OK")

patient.rename("Alice Jones")
print("after rename:", patient)

# 4. Appointment checks
print("--- appointments ---")
appointment = Appointment(
    patient,
    practitioner,
    datetime.date(2026, 10, 5),
    datetime.time(10, 0),
)
print("new appointment status:", appointment.status.value)

other = Appointment(
    Patient(2, "Bob Johnson"),
    practitioner,
    datetime.date(2026, 10, 5),
    datetime.time(10, 0),
)
print("same practitioner, date and time conflict:", appointment.conflicts_with(other))

appointment.cancel()
print("after cancel:", appointment.status.value)
print("conflict now:", appointment.conflicts_with(other))

# Canceling again should fail because the appointment is no longer scheduled.
try:
    appointment.cancel()
    print("second cancel -> ACCEPTED (problem)")
except InvalidAppointmentStatusError as error:
    print("second cancel -> rejected:", error)

# Directly changing status should not be allowed.
try:
    appointment.status = AppointmentStatus.SCHEDULED
    print("status changed directly (problem)")
except AttributeError:
    print("status cannot be set directly: OK")

# 5. Type validation for appointments
for label, args in [
    ("wrong patient type", ("x", practitioner, datetime.date.today(), datetime.time(9))),
    ("date as text", (patient, practitioner, "2026-10-05", datetime.time(9))),
]:
    try:
        Appointment(*args)
        print(label, "-> ACCEPTED (problem)")
    except TypeError as error:
        print(label, "-> rejected:", error)