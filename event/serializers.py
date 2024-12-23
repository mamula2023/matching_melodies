from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Event, Category, Genre 

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

    def validate(self, data):
        if data['event_type'] == 'collaboration' and data.get('date') is not None:
            raise serializers.ValidationError("Collaboration events should not have a date.")
        elif data['event_type'] == 'gig' and not data.get('date'):
            raise serializers.ValidationError("Gig events must have a date.")
        return data
