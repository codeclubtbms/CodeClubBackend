import os

import requests
import simplejson
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from CodeClubBackend.utils import createResponse
from Github.utils import get_session_info


class GeneralView(APIView):
    def get(self,request):
        url = request.build_absolute_uri()
        url = url[url.index("github/")+len("github/"):]
        print('https://api.github.com/' + url)
        response = requests.get('https://api.github.com/' + url, auth=(os.environ.get('GITHUB_USERNAME'), os.environ.get('GITHUB_PAT')))

        response = Response(simplejson.loads(response.text))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

        return response
class SessionsView(APIView):
    def get(self,request):
        REQUEST_URL = "https://api.github.com/repos/codeclubtbms/Sessions/contents"
        try:
            SESSION_ID = request.GET['session_id']
        except:
            SESSION_ID = None
        data = requests.get(REQUEST_URL,auth=(os.environ.get('GITHUB_USERNAME'), os.environ.get('GITHUB_PAT')))
        data = simplejson.loads(data.text)

        if not SESSION_ID: #return list of all sessions
            files = []
            for repo in data:
                file = {}
                file['name'] = str(repo['name'])
                file['url'] = str(repo['download_url'])
                sessionData = requests.get(str(repo['download_url']))
                file['properties'] = get_session_info(sessionData.text) if get_session_info(sessionData.text) is not None else {}
                files.append(file)

            return createResponse(files)

        else: #return details of specified Session ID

            repo = data[int(SESSION_ID)]
            file = {}
            file['name'] = str(repo['name'])
            file['url'] = str(repo['download_url'])
            return createResponse(file)