import django_filters

from rest_framework import serializers

from core.models.boot_script import BootScript, ScriptType
from core.models.user import AtmosphereUser
from api.v2.serializers.fields.base import UUIDHyperlinkedIdentityField


class BootScriptSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='username', queryset=AtmosphereUser.objects.all(),
        required=False)
    text = serializers.CharField(source='script_text')
    type = serializers.SlugRelatedField(
        source='script_type',
        slug_field='name',
        queryset=ScriptType.objects.all())
    url = UUIDHyperlinkedIdentityField(
        view_name='api:v2:bootscript-detail',
    )
    def create(self, validated_data):

        if 'created_by' not in validated_data:
            request = self.context.get('request')
            if request and request.user:
                validated_data['created_by'] = request.user
        return super(BootScriptSerializer, self).create(validated_data)

    class Meta:
        model = BootScript
        fields = ('id', 'uuid', 'created_by', 'title', 'text', 'type')
