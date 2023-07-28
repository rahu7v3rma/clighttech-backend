from rest_framework import serializers


class TraceFilteredRequestSerializer(serializers.Serializer):
    # pylint: disable=abstract-method
    scan = serializers.IntegerField(required=True)
    mode = serializers.IntegerField(required=True)
    odos = serializers.IntegerField(required=True)


class StatsSummaryRequestSerializer(serializers.Serializer):
    # pylint: disable=abstract-method
    scan = serializers.IntegerField(required=True)
    mode = serializers.IntegerField(required=True)
    odos = serializers.IntegerField(required=True)
