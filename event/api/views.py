from rest_framework import viewsets, permissions, response, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from event.models import Event, Category, Genre, Application
from event.serializers import EventSerializer, ApplicationSerializer
from event.permissions import EventPermissions, ApplicationPermissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [EventPermissions]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        role = request.user.role
        if role != 'organizer':
            return Response(
                    {"detail": "You must be registered as organizer to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                    )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationPermissions]    

    def create(self, request, pk=None):
        try:
            event=Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Respose({'detail': 'Event Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(
                data=request.data,
                context={'event': event, 'user': request.user}
                )
        
        if serializer.is_valid():
            application = serializer.save()
            return Response({'id': application.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExists:
            return Response({'detail': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        if application.event.author != request.user and application.user != request.user:
            raise PermissionDenied('You do not have permission to view this application.')

        serializer = self.get_serializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        if event.author != request.user:
            return Response({'detail': 'You do not have permission to view these applications.'}, 
                            status=status.HTTP_403_FORBIDDEN)

        applications = Application.objects.filter(event=event)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

