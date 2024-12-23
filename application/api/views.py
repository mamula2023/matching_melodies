from rest_framework import viewsets, permissions, response, status
from event.models import Event
from application.models import Application
from application.serializers import ApplicationSerializer
from application.permissions import ApplicationPermissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from application.tasks import send_application_email

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationPermissions]    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'event']
    pagination_class = PageNumberPagination

    def create(self, request, pk=None):
        try:
            event=Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'detail': 'Event Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if event.author == request.user:
            raise PermissionDenied({'detail': 'You cannot apply to own event'})

        serializer = self.get_serializer(
                data=request.data,
                context={'event': event, 'user': request.user}
                )
        
        if serializer.is_valid():
            application = serializer.save()
            return Response({'id': application.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        application = self.get_object()

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


    def accept(self, request, pk=None):
        application = self.get_object()       

        if application.event.author != request.user:
            return Response({'detail': 'You are not authorized to accept this application.'},
                            status=status.HTTP_403_FORBIDDEN)

        if application.status != 'pending':
            return Response({'detail': 'Application status already changed!'}, status=status.HTTP_400_BAD_REQUEST)

        application.status='accepted'
        application.save()

        inform_applicant(application, True)

        return Response({'detail': 'Application accepted successfully'})

        
    def reject(self, request, pk=None):
        application = self.get_object()       

        if application.event.author != request.user:
            return Response({'detail': 'You are not authorized to reject this application.'},
                            status=status.HTTP_403_FORBIDDEN)

        if application.status != 'pending':
            return Response({'detail': 'Application status already changed!'}, status=status.HTTP_400_BAD_REQUEST)
        
        application.status = 'rejected'
        application.save()
        
        inform_applicant(application, False)

        return Response({'detail': 'Application rejected successfully'})


    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise NotFound(detail="Application not found")


def inform_applicant(applicaiton, success):
    subject = f"Update about application on {application.event.event_type} {application.event.title}"
    if success:
        message = f"Congratulations! You have been accepted on {application.event.title}"
    else:
        message = f"We are sorry to inform you that author of {application.event.title} has rejected your application"
    send_application_email.delay(application.user.email, subject, message)
    
