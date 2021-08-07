from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Top5


class Top5Serializer(HyperlinkedModelSerializer):
    class Meta:
        model = Top5
        fields = ('username', 'spent_money', 'gems')
