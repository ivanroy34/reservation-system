import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_sys.settings')
django.setup()

from reservation_app.models import (
    Customer, TableCategory, Table, ReservationStatus,
    Reservation, Payment, AuditLog
)

print("Seeding database...")

# 1. Categories
c1, _ = TableCategory.objects.get_or_create(
    name="Main Dining",
    defaults={"description": "Standard dining room tables with comfortable seating."}
)
c2, _ = TableCategory.objects.get_or_create(
    name="VIP Lounge",
    defaults={"description": "Exclusive booth seating with premium ambiance."}
)
c3, _ = TableCategory.objects.get_or_create(
    name="Patio Outdoor",
    defaults={"description": "Al fresco garden terrace dining area."}
)

# 2. Tables
t1, _ = Table.objects.get_or_create(
    table_number="T-01",
    defaults={"category": c1, "capacity": 4, "location": "Window Side", "is_active": True}
)
t2, _ = Table.objects.get_or_create(
    table_number="T-02",
    defaults={"category": c1, "capacity": 2, "location": "Center Floor", "is_active": True}
)
t3, _ = Table.objects.get_or_create(
    table_number="V-01",
    defaults={"category": c2, "capacity": 6, "location": "VIP Section A", "is_active": True}
)
t4, _ = Table.objects.get_or_create(
    table_number="P-01",
    defaults={"category": c3, "capacity": 4, "location": "Garden Patio", "is_active": True}
)

# 3. Reservation Statuses
s_pending, _ = ReservationStatus.objects.get_or_create(
    name="PENDING",
    defaults={"description": "Reservation received, awaiting confirmation.", "is_active": True}
)
s_confirmed, _ = ReservationStatus.objects.get_or_create(
    name="CONFIRMED",
    defaults={"description": "Reservation confirmed by staff.", "is_active": True}
)
s_cancelled, _ = ReservationStatus.objects.get_or_create(
    name="CANCELLED",
    defaults={"description": "Reservation cancelled.", "is_active": True}
)
s_completed, _ = ReservationStatus.objects.get_or_create(
    name="COMPLETED",
    defaults={"description": "Party seated and finished dining.", "is_active": True}
)

# 4. Customers
cust1, _ = Customer.objects.get_or_create(
    email="john.doe@example.com",
    defaults={"first_name": "John", "last_name": "Doe", "phone": "+1 555-0192"}
)
cust2, _ = Customer.objects.get_or_create(
    email="sarah.connor@example.com",
    defaults={"first_name": "Sarah", "last_name": "Connor", "phone": "+1 555-0144"}
)
cust3, _ = Customer.objects.get_or_create(
    email="bruce.wayne@example.com",
    defaults={"first_name": "Bruce", "last_name": "Wayne", "phone": "+1 555-0188"}
)
cust4, _ = Customer.objects.get_or_create(
    email="ivan@example.com",
    defaults={"first_name": "Ivan", "last_name": "Mailem", "phone": "+1 555-0188"}
)

# 5. Reservations
today = date.today()

r1, r1_created = Reservation.objects.get_or_create(
    customer=cust1,
    table=t1,
    reservation_date=today,
    start_time=time(18, 0),
    defaults={
        "end_time": time(20, 0),
        "guests": 3,
        "status": s_confirmed,
        "notes": "Window seat preferred. Celebrating anniversary."
    }
)
if r1_created:
    AuditLog.objects.create(
        reservation=r1,
        action="CREATED",
        performed_by="System Direct",
        details="Sample reservation created."
    )

r2, r2_created = Reservation.objects.get_or_create(
    customer=cust3,
    table=t3,
    reservation_date=today + timedelta(days=1),
    start_time=time(19, 30),
    defaults={
        "end_time": time(21, 30),
        "guests": 5,
        "status": s_confirmed,
        "notes": "VIP party setup required."
    }
)
if r2_created:
    AuditLog.objects.create(
        reservation=r2,
        action="CREATED",
        performed_by="System Direct",
        details="Sample VIP reservation created."
    )

# 6. Payments
Payment.objects.get_or_create(
    reservation=r1,
    defaults={
        "amount": 50.00,
        "payment_method": "Credit Card",
        "payment_status": "PAID"
    }
)

print("Sample data populated successfully!")
