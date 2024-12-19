from .models import Application
from rest_framework import serializers

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['id','event', 'user']


    def validate(self, data):
        event = self.context.get('event')
        user = self.context.get('user')

        if user.role == 'organizer':
            raise serializers.ValidationError({'detail': 'Organizers can not apply to event'})

        if Application.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError("You have already applied to this event")

        return data 


    def create(self, validated_data):
        event = self.context.get('event')
        user = self.context.get('user')
        application = Application.objects.create(
                user=user,
                event=event,
                **validated_data
                )
        return application

