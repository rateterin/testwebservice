import datetime
import os
from testwebservice.settings import MEDIA_ROOT
from rest_framework.serializers import HyperlinkedModelSerializer
from .models import ImportLog, Deal
from customer.models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction


@receiver(post_save, sender=ImportLog)
@transaction.atomic
def processing_import_file_into_deal(sender, instance, **kwargs):
    if instance.success:
        return
    error = None
    deal_fields_list = [f.name for f in Deal._meta.fields if not f.name == 'id']
    with open(os.path.join(MEDIA_ROOT, str(instance.file))) as f:
        head = None
        try:
            head = f.readline()
        except UnicodeDecodeError:
            error = {'Status': 'Error', 'Desc': 'Ошибка UnicodeDecodeError'}
        else:
            head = head.removesuffix('\n').split(',')
            if head != deal_fields_list:
                error = {'Status': 'Error', 'Desc': 'Ошибка в заголовке файла'}
            else:
                for num, line in enumerate(f.readlines()):
                    if error:
                        break
                    customer_f, item_f, total_f, quantity_f, date_f = line.removesuffix('\n').split(',')
                    if not total_f.isdecimal():
                        error = {'Status': 'Error',
                                 'Desc': f'Ошибка в файле строка {num} поле \'total\'. \r\n'
                                         f'Должно быть целым положительным числом.'
                                 }
                        break
                    if not quantity_f.isdecimal():
                        error = {'Status': 'Error',
                                 'Desc': f'Ошибка в файле строка {num} поле \'quantity\'. \r\n'
                                         f'Должно быть целым положительным числом.'
                                 }
                        break
                    try:
                        datetime.datetime.fromisoformat(date_f)
                    except ValueError:
                        error = {'Status': 'Error',
                                 'Desc': f'Ошибка в файле строка {num} поле \'date\'. \r\n'
                                         f'Должно быть датой в iso-формате.'
                                 }
                        break

                    customer_rf = Customer.objects.filter(pk=customer_f).first()
                    if not customer_rf:
                        customer_rf = Customer(pk=customer_f)
                        customer_rf.save()

                    if not Deal.objects.filter(customer=customer_f, item=item_f, total=total_f, quantity=quantity_f,
                                               date=date_f):
                        row = Deal()
                        row.customer = customer_rf
                        row.item, row.total, row.quantity, row.date = \
                            item_f, total_f, quantity_f, date_f
                        row.save()

                        customer_row = Customer.objects.get(pk=customer_f)
                        customer_row.spent_money += int(total_f)
                        customer_row.save()

    os.remove(os.path.join(MEDIA_ROOT, str(instance.file)))
    if error:
        instance.err = error
    else:
        instance.success = True
        instance.err = None
        instance.save()


class ImportLogSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ImportLog
        fields = ('file',)

    def to_representation(self, instance):
        if instance.success:
            return {'Status': 'Ok'}
        else:
            return instance.err
