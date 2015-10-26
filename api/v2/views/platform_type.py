from core.models import PlatformType

from api.v2.serializers.details import PlatformTypeSerializer
from api.v2.views.base import AuthViewSet
from api.v2.views.mixins import MultipleFieldLookup


class PlatformTypeViewSet(MultipleFieldLookup, AuthViewSet):

    """
    API endpoint that allows instance actions to be viewed or edited.
    """

    lookup_fields = ("id", "uuid")
    queryset = PlatformType.objects.all()
    serializer_class = PlatformTypeSerializer
    http_method_names = ['get', 'head', 'options', 'trace']
