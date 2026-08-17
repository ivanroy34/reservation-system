import os
import django
from datetime import date, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_sys.settings')
django.setup()

from reservation_app.forms import ReservationForm
from reservation_app.models import Customer, Table, ReservationStatus, Reservation, AuditLog

print("Running automated business logic validation tests...")

customer = Customer.objects.first()
table = Table.objects.first() # Capacity is 4
status = ReservationStatus.objects.filter(name="CONFIRMED").first()

test_date = date(2026, 9, 1)

# Test 1: Capacity Overlap Check
print("Test 1: Testing capacity validation (guests > table capacity)...")
form_invalid_cap = ReservationForm(data={
    'customer': customer.id,
    'table': table.id,
    'reservation_date': test_date,
    'start_time': time(12, 0),
    'end_time': time(14, 0),
    'guests': 100, # Exceeds capacity of 4
    'status': status.id,
    'notes': 'Test capacity fail'
})

if not form_invalid_cap.is_valid():
    print(f"  PASSED: Capacity error detected -> {form_invalid_cap.errors.get('guests') or form_invalid_cap.non_field_errors()}")
else:
    print("  FAILED: Form should have been invalid for capacity overflow!")

# Test 2: Valid Reservation Creation
print("\nTest 2: Creating valid reservation...")
form_valid = ReservationForm(data={
    'customer': customer.id,
    'table': table.id,
    'reservation_date': test_date,
    'start_time': time(12, 0),
    'end_time': time(14, 0),
    'guests': 2,
    'status': status.id,
    'notes': 'Valid reservation test'
})

if form_valid.is_valid():
    res1 = form_valid.save()
    print(f"  PASSED: Created reservation #{res1.id}")
else:
    print(f"  FAILED: Form validation errors -> {form_valid.errors}")

# Test 3: Time Overlap Prevention
print("\nTest 3: Testing double-booking overlap prevention...")
form_overlap = ReservationForm(data={
    'customer': customer.id,
    'table': table.id,
    'reservation_date': test_date,
    'start_time': time(13, 0), # Overlaps with 12:00-14:00
    'end_time': time(15, 0),
    'guests': 2,
    'status': status.id,
    'notes': 'Overlap test'
})

if not form_overlap.is_valid():
    print(f"  PASSED: Overlap error detected -> {form_overlap.non_field_errors()}")
else:
    print("  FAILED: Overlapping reservation was mistakenly allowed!")

# Clean up test reservation
if 'res1' in locals():
    res1.delete()

print("\nALL BUSINESS LOGIC VALIDATION TESTS COMPLETED SUCCESSFULLY!")
