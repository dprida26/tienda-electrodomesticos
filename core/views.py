from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CompanyConfiguration
from .serializers import CompanyConfigurationSerializer


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


class CompanyConfigurationAPIView(APIView):
    """API para obtener la configuración de la empresa"""

    def get(self, request):
        config = CompanyConfiguration.get_config()
        serializer = CompanyConfigurationSerializer(config)
        return Response(serializer.data)
