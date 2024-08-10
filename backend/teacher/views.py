from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from urllib.parse import unquote
from core import SAT_embedding


class SATTeacher(APIView):
    def post(self, request):
        decoded_text = unquote(request.body)
        question = decoded_text[9:].replace("+", " ")

        # question = request.body.decode('utf-8')[9:] # json.loads(request.body.decode('utf-8'))["question"]
        print(question)
        answer = SAT_embedding.get_answer(question)
        return Response({"answer": answer}, status=status.HTTP_200_OK)
