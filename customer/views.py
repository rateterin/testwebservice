from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models.aggregates import Count
from .models import Top5, Customer
from deal.models import Deal, ImportLog
from .serializers import Top5Serializer
from django.db.models.query import QuerySet
from django.db import transaction


class Top5ViewSet(ReadOnlyModelViewSet):
    queryset = Top5.objects.all()
    serializer_class = Top5Serializer

    def get_queryset(self):
        last_success_import = ImportLog.objects.values('date').first()
        if last_success_import:
            last_success_import = last_success_import['date']
        last_top5 = Top5.objects.values('date').first()
        if last_top5:
            last_top5 = last_top5['date']

        @transaction.atomic
        def top5_expires_or_empty():
            # refresh Top5 from Customer
            Top5.objects.all().delete()
            for row in Customer.objects.all()[:5]:
                Top5(username=row.username, spent_money=int(row.spent_money)).save()

            # gems info add in Top5 algorithm
            top5 = Top5.objects.all()
            top5_lst = list(top5.values_list('username', flat=True))
            gems_lst = list(Deal.objects.filter(customer__in=top5_lst).values_list('item', flat=True).annotate(
                cc=Count('customer', distinct=True)).filter(cc__gt=1))
            for elem in top5_lst:
                gems = list(
                    Deal.objects.filter(customer=elem, item__in=gems_lst).values_list('item', flat=True).annotate(
                        c=Count('id')))
                gems = ', '.join(gems)
                row = Top5.objects.filter(username=elem)
                row.update(gems=gems)

            return Top5.objects.values('date').first()['date']

        if not last_top5:
            if not Customer.objects.all():
                return self.queryset
            last_top5 = top5_expires_or_empty()
        if last_success_import > last_top5:
            top5_expires_or_empty()

        # original get_queryset code
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset
