from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Event, Category, Genre, Application

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'author']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        data['genres'] = GenreSerializer(instance.genres.all(), many=True).data
        return data


    def create(self, validated_data):
        category_ids = validated_data.pop('categories', [])
        genre_ids = validated_data.pop('genres', [])

        event = Event.objects.create(**validated_data)

        event.categories.set(category_ids)
        event.genres.set(genre_ids)

        return event


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

