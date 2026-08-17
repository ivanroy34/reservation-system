from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.db.models import Sum, Q, Count
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from datetime import date

from .models import Customer, TableCategory, Table, ReservationStatus, Reservation, Payment, AuditLog
from .forms import CustomerForm, TableCategoryForm, TableForm, ReservationStatusForm, ReservationForm, PaymentForm

# ==========================================
# 0. DASHBOARD VIEW (Analytics & Overview)
# ==========================================
class DashboardView(TemplateView):
    template_name = 'reservation_app/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        # Summary statistics
        context['total_customers'] = Customer.objects.count()
        context['total_tables'] = Table.objects.filter(is_active=True).count()
        context['total_reservations'] = Reservation.objects.count()
        context['total_revenue'] = Payment.objects.filter(payment_status='PAID').aggregate(total=Sum('amount'))['total'] or 0

        # Booking status counts
        status_counts = Reservation.objects.values('status__name').annotate(count=Count('id'))
        context['status_counts'] = {item['status__name']: item['count'] for item in status_counts}

        # Upcoming bookings (today and onwards)
        context['upcoming_reservations'] = Reservation.objects.filter(
            reservation_date__gte=today
        ).order_by('reservation_date', 'start_time')[:5]

        # Recent activities (audit logs)
        context['recent_logs'] = AuditLog.objects.order_by('-action_time')[:5]

        # Table availability stats
        total_tables_count = Table.objects.count()
        context['active_tables_count'] = Table.objects.filter(is_active=True).count()
        
        return context


# ==========================================
# 1. CUSTOMER CRUD
# ==========================================
class CustomerListView(ListView):
    model = Customer
    template_name = 'reservation_app/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Customer.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            )
        return Customer.objects.all()


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'reservation_app/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = self.object.reservations.all().order_by('-reservation_date', '-start_time')
        return context


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'reservation_app/customer_form.html'
    success_url = reverse_lazy('reservation_app:customer_list')


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'reservation_app/customer_form.html'

    def get_success_url(self):
        return reverse_lazy('reservation_app:customer_detail', kwargs={'pk': self.object.pk})


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'reservation_app/customer_confirm_delete.html'
    success_url = reverse_lazy('reservation_app:customer_list')


# ==========================================
# 2. TABLE CATEGORY CRUD
# ==========================================
class TableCategoryListView(ListView):
    model = TableCategory
    template_name = 'reservation_app/table_category_list.html'
    context_object_name = 'categories'


class TableCategoryDetailView(DetailView):
    model = TableCategory
    template_name = 'reservation_app/table_category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = self.object.tables.all()
        return context


class TableCategoryCreateView(CreateView):
    model = TableCategory
    form_class = TableCategoryForm
    template_name = 'reservation_app/table_category_form.html'
    success_url = reverse_lazy('reservation_app:table_category_list')


class TableCategoryUpdateView(UpdateView):
    model = TableCategory
    form_class = TableCategoryForm
    template_name = 'reservation_app/table_category_form.html'

    def get_success_url(self):
        return reverse_lazy('reservation_app:table_category_detail', kwargs={'pk': self.object.pk})


class TableCategoryDeleteView(DeleteView):
    model = TableCategory
    template_name = 'reservation_app/table_category_confirm_delete.html'
    success_url = reverse_lazy('reservation_app:table_category_list')


# ==========================================
# 3. TABLE CRUD
# ==========================================
class TableListView(ListView):
    model = Table
    template_name = 'reservation_app/table_list.html'
    context_object_name = 'tables'


class TableDetailView(DetailView):
    model = Table
    template_name = 'reservation_app/table_detail.html'
    context_object_name = 'table'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = self.object.reservations.all().order_by('-reservation_date', '-start_time')[:10]
        return context


class TableCreateView(CreateView):
    model = Table
    form_class = TableForm
    template_name = 'reservation_app/table_form.html'
    success_url = reverse_lazy('reservation_app:table_list')


class TableUpdateView(UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'reservation_app/table_form.html'

    def get_success_url(self):
        return reverse_lazy('reservation_app:table_detail', kwargs={'pk': self.object.pk})


class TableDeleteView(DeleteView):
    model = Table
    template_name = 'reservation_app/table_confirm_delete.html'
    success_url = reverse_lazy('reservation_app:table_list')


# ==========================================
# 4. RESERVATION STATUS CRUD
# ==========================================
class ReservationStatusListView(ListView):
    model = ReservationStatus
    template_name = 'reservation_app/reservation_status_list.html'
    context_object_name = 'statuses'


class ReservationStatusCreateView(CreateView):
    model = ReservationStatus
    form_class = ReservationStatusForm
    template_name = 'reservation_app/reservation_status_form.html'
    success_url = reverse_lazy('reservation_app:reservation_status_list')


class ReservationStatusUpdateView(UpdateView):
    model = ReservationStatus
    form_class = ReservationStatusForm
    template_name = 'reservation_app/reservation_status_form.html'
    success_url = reverse_lazy('reservation_app:reservation_status_list')


class ReservationStatusDeleteView(DeleteView):
    model = ReservationStatus
    template_name = 'reservation_app/reservation_status_confirm_delete.html'
    success_url = reverse_lazy('reservation_app:reservation_status_list')


# ==========================================
# 5. RESERVATION CRUD & CANCEL
# ==========================================
class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservation_app/reservation_list.html'
    context_object_name = 'reservations'
    paginate_by = 15

    def get_queryset(self):
        queryset = Reservation.objects.select_related('customer', 'table', 'status').all()
        
        # Filter by customer ID
        customer_id = self.request.GET.get('customer')
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
            
        # Filter by date
        date_str = self.request.GET.get('date')
        if date_str:
            queryset = queryset.filter(reservation_date=date_str)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        context['selected_customer'] = self.request.GET.get('customer', '')
        context['selected_date'] = self.request.GET.get('date', '')
        return context


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservation_app/reservation_detail.html'
    context_object_name = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = self.object.payments.all()
        context['audit_logs'] = self.object.audit_logs.all().order_by('-action_time')
        return context


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_app/reservation_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create an audit record
        AuditLog.objects.create(
            reservation=self.object,
            action="CREATED",
            performed_by="Staff/System",
            details=f"Reservation created for {self.object.customer} on Table {self.object.table.table_number} for {self.object.guests} guests."
        )
        return response

    def get_success_url(self):
        return reverse_lazy('reservation_app:reservation_detail', kwargs={'pk': self.object.pk})


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_app/reservation_form.html'

    def form_valid(self, form):
        # We need to capture details before updating for audit logging
        old_obj = Reservation.objects.get(pk=self.kwargs['pk'])
        response = super().form_valid(form)
        
        # Check changes
        changes = []
        if old_obj.table != self.object.table:
            changes.append(f"Table: {old_obj.table} -> {self.object.table}")
        if old_obj.reservation_date != self.object.reservation_date:
            changes.append(f"Date: {old_obj.reservation_date} -> {self.object.reservation_date}")
        if old_obj.start_time != self.object.start_time or old_obj.end_time != self.object.end_time:
            changes.append(f"Time: {old_obj.start_time}-{old_obj.end_time} -> {self.object.start_time}-{self.object.end_time}")
        if old_obj.guests != self.object.guests:
            changes.append(f"Guests: {old_obj.guests} -> {self.object.guests}")
        if old_obj.status != self.object.status:
            changes.append(f"Status: {old_obj.status} -> {self.object.status}")

        change_details = ", ".join(changes) if changes else "No major fields changed"

        AuditLog.objects.create(
            reservation=self.object,
            action="UPDATED",
            performed_by="Staff/System",
            details=f"Reservation updated. Changes: {change_details}."
        )
        return response

    def get_success_url(self):
        return reverse_lazy('reservation_app:reservation_detail', kwargs={'pk': self.object.pk})


class ReservationCancelView(View):
    def get(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        return render(request, 'reservation_app/reservation_confirm_cancel.html', {'reservation': reservation})

    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        
        # Find or create CANCELLED status
        cancelled_status, _ = ReservationStatus.objects.get_or_create(
            name="CANCELLED",
            defaults={"description": "Standard cancelled reservation status.", "is_active": True}
        )
        
        # Save old status for audit details
        old_status = reservation.status.name
        
        reservation.status = cancelled_status
        reservation.save()

        # Audit Log
        AuditLog.objects.create(
            reservation=reservation,
            action="CANCELLED",
            performed_by="Staff/System",
            details=f"Reservation cancelled (Previous status: {old_status})."
        )
        return redirect('reservation_app:reservation_detail', pk=pk)


# ==========================================
# 6. PAYMENT CRUD
# ==========================================
class PaymentListView(ListView):
    model = Payment
    template_name = 'reservation_app/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 15

    def get_queryset(self):
        queryset = Payment.objects.select_related('reservation', 'reservation__customer').all()
        reservation_id = self.request.GET.get('reservation')
        if reservation_id:
            queryset = queryset.filter(reservation_id=reservation_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.all()
        context['selected_reservation'] = self.request.GET.get('reservation', '')
        return context


class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'reservation_app/payment_detail.html'
    context_object_name = 'payment'


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'reservation_app/payment_form.html'

    def get_initial(self):
        initial = super().get_initial()
        reservation_id = self.request.GET.get('reservation')
        if reservation_id:
            initial['reservation'] = reservation_id
        return initial

    def get_success_url(self):
        return reverse_lazy('reservation_app:payment_detail', kwargs={'pk': self.object.pk})


class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'reservation_app/payment_form.html'

    def get_success_url(self):
        return reverse_lazy('reservation_app:payment_detail', kwargs={'pk': self.object.pk})


# ==========================================
# 7. AUDIT LOG CRUD
# ==========================================
class AuditLogListView(ListView):
    model = AuditLog
    template_name = 'reservation_app/audit_log_list.html'
    context_object_name = 'logs'
    paginate_by = 20

    def get_queryset(self):
        queryset = AuditLog.objects.select_related('reservation', 'reservation__customer').all()
        reservation_id = self.request.GET.get('reservation')
        if reservation_id:
            queryset = queryset.filter(reservation_id=reservation_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_reservation'] = self.request.GET.get('reservation', '')
        return context


class AuditLogDetailView(DetailView):
    model = AuditLog
    template_name = 'reservation_app/audit_log_detail.html'
    context_object_name = 'log'


# ==========================================
# 7. AUTHENTICATION VIEWS
# ==========================================
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

