from django.contrib import admin
from .models import (
    Customer,
    TableCategory,
    Table,
    ReservationStatus,
    Reservation,
    Payment,
    AuditLog
)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(TableCategory)
class TableCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'category', 'capacity', 'location', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'location')
    search_fields = ('table_number', 'location')
    list_editable = ('is_active',)

@admin.register(ReservationStatus)
class ReservationStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'description')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'table', 'reservation_date', 'start_time', 'end_time', 'guests', 'status', 'created_at')
    list_filter = ('status', 'reservation_date', 'table__category')
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email', 'table__table_number')
    date_hierarchy = 'reservation_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation', 'amount', 'payment_method', 'payment_status', 'transaction_ref', 'paid_at', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('transaction_ref', 'reservation__id', 'reservation__customer__email', 'reservation__customer__first_name')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation', 'action', 'performed_by', 'action_time')
    list_filter = ('action', 'action_time')
    search_fields = ('performed_by', 'action', 'details', 'reservation__id')
    readonly_fields = ('action_time',)

