from django.contrib import admin

from django_dragonpay.models import *


def readable_amount(obj):
    return "{} {:,}".format(obj.currency, obj.amount)


class StatusPayoutsFilter(admin.SimpleListFilter):
    '''Admin filter for Payouts Status'''
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return model_admin.model.STATUS_CODES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())


class PayoutUserAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')


class TransactionAdmin(admin.ModelAdmin):
    date_heirarchy = 'created_at'
    search_fields = ('txn_id', 'email')
    list_filter = (StatusPayoutsFilter, )
    list_display = ('token', 'status', readable_amount, 'description', 'email')


class PayoutsAdmin(admin.ModelAdmin):
    class CompletedPayoutsFilter(admin.SimpleListFilter):
        '''Admin filter for Completed Payouts.'''
        title = 'Completed'
        parameter_name = 'completed'

        def lookups(self, request, model_admin):
            return (
                ('yes', 'Completed'),
                ('no', 'Not yet completed'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                # filter for Success/Failed/Voided
                return queryset.filter(status__in=['S', 'F', 'V'])
            elif self.value() == 'no':
                # filter for Pending/In progress
                return queryset.filter(status__in=['P', 'G'])

    date_heirarchy = 'created_at'
    search_fields = ('txn_id', 'user_id', 'user_name', 'email')
    list_filter = (CompletedPayoutsFilter, StatusPayoutsFilter)
    list_display = (
        'txn_id', 'user_name', 'email', readable_amount, 'description')


admin.site.register(DragonpayPayoutUser, PayoutUserAdmin)
admin.site.register(DragonpayTransaction, TransactionAdmin)
admin.site.register(DragonpayPayout, PayoutsAdmin)
