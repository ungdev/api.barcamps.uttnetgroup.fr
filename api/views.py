from django.http import HttpResponse
from .models import Barcamp, Speaker, Talk
from .serializers import BarcampSerializer, TalkSerializer, SpeakerSerializer
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .lib.etuutt import get_redirect_link, get_access_code, get_user_info
import jwt
import os

# Create your views here.
def index(request):
    return HttpResponse("Barcamps API.")

class BarcampList(generics.ListCreateAPIView):
    queryset = Barcamp.objects.all()
    serializer_class = BarcampSerializer

class BarcampDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Barcamp.objects.all()
    serializer_class = BarcampSerializer

class TalkList(generics.ListCreateAPIView):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer

class TalkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer

class SpeakerList(generics.ListCreateAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

class SpeakerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

class OauthToken(APIView):
    # allow anyone to POST
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """ Return auth link
        """
        return Response(get_redirect_link())

    def post(self, request, format=None):
        """ Send the authorization_code to EtuUTT to get an access token
        """
        authorization_code = request.POST.get('authorization_code')

        if not authorization_code: # no authorization_code
            return Response("Missing authorization_code", status=status.HTTP_400_BAD_REQUEST)
        # get access_token
        access_token, refresh_token = get_access_code(authorization_code)
        # get info about the user
        user_info = get_user_info(access_token)

        user_jwt = jwt.encode({
            'email': user_info['email'],
            'firstName': user_info['firstName'],
            'lastName': user_info['lastName'],
        }, os.environ.get('JWT_SECRET'), algorithm='HS256')

        return Response(user_jwt)
