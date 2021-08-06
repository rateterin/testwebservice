from rest_framework.serializers import HyperlinkedModelSerializer
from .models import ImportLog, Deal


class ImportLogSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ImportLog
        fields = ('file',)
