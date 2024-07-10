from requests_oauthlib import OAuth1
from urllib.parse import urlencode
import requests

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 

from django.conf import settings
from django.http.response import  HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http.response import JsonResponse

from .utils import create_user, create_token

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class Logout(APIView):
    def get(self, request):
        logout(request)
        content = {'message': 'Logged out successfully'}
        return Response(content)

class TwitterTokenEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        try:
            oauth = OAuth1(
                        settings.TWITTER_API_KEY, 
                        client_secret=settings.TWITTER_API_SECRET_KEY
            )
                #Step one: obtaining request token
            request_token_url = "https://api.twitter.com/oauth/request_token"
            data = urlencode({
                        "oauth_callback": settings.TWITTER_AUTH_CALLBACK_URL
            })
            response = requests.post(request_token_url, auth=oauth, data=data)
            response.raise_for_status()
            response_split = response.text.split("&")
            oauth_token = response_split[0].split("=")[1]
            oauth_token_secret = response_split[1].split("=")[1]

            payload = {
                "oauth_token": oauth_token
            }
            return JsonResponse(payload, status=status.HTTP_200_OK)
        except ConnectionError:
            html="<html><body>You have no internet connection</body></html>"
            return HttpResponse(html, status=403)
        except:
            html="<html><body>Something went wrong.Try again.</body></html>"
            return HttpResponse(html, status=403)

class TwitterAuthEndpoint(APIView):
    def post(self, request, *args, **kwargs):
        try:
            req_data = JSONParser().parse(request)
            oauth_token = req_data.get("oauth_token")
            oauth_verifier = req_data.get("oauth_verifier")
            oauth = OAuth1(
                                settings.TWITTER_API_KEY,
                                client_secret=settings.TWITTER_API_SECRET_KEY,
                                resource_owner_key=oauth_token,
                                verifier=oauth_verifier,
            )
            res = requests.post(
                        f"https://api.twitter.com/oauth/access_token", auth=oauth
            )
            res_split = res.text.split("&")
            oauth_token = res_split[0].split("=")[1]
            oauth_secret = res_split[1].split("=")[1]
            user_id = res_split[2].split("=")[1] if len(res_split) > 2 else None
            user_name = res_split[3].split("=")[1] if len(res_split) > 3 else None

            user, n_user = create_user(user_name, user_id, oauth_secret)
            token = create_token(user, oauth_token)

            # Do we need to verify the twitter response status?
            login(request, user)

            response = {
                "user_id": n_user.twitter_user_id,
                "token": token.key
            }
            return JsonResponse(response, status=status.HTTP_200_OK)

        except ConnectionError:
            return HttpResponse(
                "<html><body>You have no internet connection</body></html>", status=403
            )
        except:
            return HttpResponse(
                "<html><body>Something went wrong.Try again.</body></html>", status=403
            )