from rest_framework import serializers, viewsets
from partner.serializers import PartnerSerializer
from .models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    partner = PartnerSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'number',
            'title',
            'partner',
            'description',
            'resolution',
            'deadline',
            'state',
            'created_at',
        )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
