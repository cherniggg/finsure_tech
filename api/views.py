import csv
import io

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework import status
from rest_framework.settings import api_settings

from rest_framework_json_api import filters
from rest_framework_json_api import django_filters

from .models import Lender
from .serializers import LenderSerializer, LenderCSVSerializer, LenderReadOnlySerializer
from .renderers import LenderCSVRenderer

class LenderViewSet(ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Lender.objects.all()
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                      django_filters.DjangoFilterBackend)
    filterset_fields = {
        'active': ('exact',),
    }

    def get_serializer_class(self):
        """
        Overriding the default serializer selection to pick up the required serializer
        for list() and retrieve() methods (performance boost)
        """
        if hasattr(self, 'action') and self.action == 'list' or self.action =='retrieve':
            return LenderReadOnlySerializer
        return LenderSerializer      

class LenderCSV(APIView):
    permission_classes = [AllowAny]

    def get_renderers(self):
        """
        Renderer selection for a proper response management
        LenderCSVRenderer is used for GET method to make fields human-readable and sort them
        """
        if self.request.method == 'POST':
            return [renderer() for renderer in api_settings.DEFAULT_RENDERER_CLASSES]
        else:
            return [LenderCSVRenderer()] + [renderer() for renderer in api_settings.DEFAULT_RENDERER_CLASSES]


    def get(self, request):
        lenders = Lender.objects.all()
        serializer = LenderCSVSerializer(lenders, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        csv_file = request.FILES.get('csv_file', '')
        # If there is no file provided - do nothing
        if not csv_file:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={})
        decoded_file = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded_file))
        # Lists for custom JSON handling
        success = []
        errors = []
        data = list(reader)
        for index, obj in enumerate(data):
            serializer = LenderCSVSerializer(data=obj)
            if serializer.is_valid():
                serializer.save()
                success.append(serializer.data)
            else:
                error_obj = {
                    "source": {"row": index + 1},
                    "details": serializer.errors
                }
                errors.append(error_obj)
        data = {
            "success": success,
            "errors": errors
        }
        return Response(status=status.HTTP_200_OK, data=data)