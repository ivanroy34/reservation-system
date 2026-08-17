from django import forms
from django.core.exceptions import ValidationError
from .models import Customer, TableCategory, Table, ReservationStatus, Reservation, Payment

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'John'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'Doe'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'john.doe@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': '+1 (555) 019-2834'
            }),
        }


class TableCategoryForm(forms.ModelForm):
    class Meta:
        model = TableCategory
        fields = ['name', 'description']
        labels = {
            'name': 'Category Name',
            'description': 'Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'e.g. VIP Booth'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400 rows-3',
                'placeholder': 'Describe table configuration, layout features, etc...',
                'rows': 3
            }),
        }


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_number', 'capacity', 'location', 'is_active', 'category']
        labels = {
            'table_number': 'Table Number / Name',
            'capacity': 'Guest Capacity',
            'location': 'Location Description',
            'is_active': 'Is Available for Reservations?',
            'category': 'Table Category',
        }
        widgets = {
            'table_number': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'e.g. T-12'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'min': 1
            }),
            'location': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'e.g. Near window, Main Lounge'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:focus:ring-indigo-400'
            }),
            'category': forms.Select(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
        }


class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = ReservationStatus
        fields = ['name', 'description', 'is_active']
        labels = {
            'name': 'Status Name',
            'description': 'Description',
            'is_active': 'Is Active Status?',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'e.g. CONFIRMED'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400 rows-3',
                'placeholder': 'Describe when this status should be used...',
                'rows': 3
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:focus:ring-indigo-400'
            }),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer', 'table', 'reservation_date', 'start_time', 'end_time', 'guests', 'status', 'notes']
        labels = {
            'customer': 'Customer',
            'table': 'Table',
            'reservation_date': 'Reservation Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'guests': 'Number of Guests',
            'status': 'Reservation Status',
            'notes': 'Notes / Special Requests',
        }
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'table': forms.Select(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'reservation_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'min': 1
            }),
            'status': forms.Select(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400 rows-3',
                'placeholder': 'Add guest preferences, dietary requirements, high-chair requests...',
                'rows': 3
            }),
        }

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests is not None and guests <= 0:
            raise ValidationError("Number of guests must be a positive number.")
        return guests

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        table = cleaned_data.get('table')
        guests = cleaned_data.get('guests')
        reservation_date = cleaned_data.get('reservation_date')
        status = cleaned_data.get('status')

        # 1. Validate that the reservation end time is later than the start time
        if start_time and end_time and end_time <= start_time:
            raise ValidationError("The reservation end time must be later than the start time.")

        # 2. Validate that a selected table can accommodate the specified number of guests
        if table and guests and table.capacity < guests:
            raise ValidationError(
                f"The selected table '{table.table_number}' has a capacity of {table.capacity} guests, which cannot accommodate {guests} guests."
            )

        # 3. Check for double booking (excluding CANCELLED reservations, and excluding the current instance if editing)
        if table and reservation_date and start_time and end_time:
            # We check if there's any other active reservation for the same table, on the same date,
            # that overlaps with the requested start and end times.
            overlapping_query = Reservation.objects.filter(
                table=table,
                reservation_date=reservation_date
            ).exclude(
                status__name__iexact='CANCELLED'
            )

            if self.instance and self.instance.pk:
                overlapping_query = overlapping_query.exclude(pk=self.instance.pk)

            for existing in overlapping_query:
                # Visual overlap: start_time < existing.end_time AND end_time > existing.start_time
                if (start_time < existing.end_time) and (end_time > existing.start_time):
                    raise ValidationError(
                        f"Table '{table.table_number}' is already booked on {reservation_date} "
                        f"from {existing.start_time.strftime('%H:%M')} to {existing.end_time.strftime('%H:%M')}."
                    )

        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reservation', 'amount', 'payment_method', 'payment_status', 'paid_at', 'transaction_ref']
        labels = {
            'reservation': 'Reservation Reference',
            'amount': 'Payment Amount ($)',
            'payment_method': 'Payment Method',
            'payment_status': 'Payment Status',
            'paid_at': 'Payment Received Date & Time',
            'transaction_ref': 'Transaction Reference (ID)',
        }
        widgets = {
            'reservation': forms.Select(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'step': '0.01',
                'min': '0.00'
            }),
            'payment_method': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'e.g. Credit Card, Cash, Apple Pay'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'paid_at': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400'
            }),
            'transaction_ref': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-slate-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:focus:border-indigo-400 dark:focus:ring-indigo-400',
                'placeholder': 'e.g. TXN-10928374'
            }),
        }
