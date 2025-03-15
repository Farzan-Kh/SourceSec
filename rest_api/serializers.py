from rest_framework import serializers

class AnalysisRequestSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    source_code = serializers.CharField(required=False)
    repo_url = serializers.URLField(required=False)

    def validate(self, data):
        if not data.get('file') and not data.get('source_code') and not data.get('repo_url'):
            raise serializers.ValidationError("At least one of 'file', 'source_code', or 'repo_url' must be provided.")
        return data