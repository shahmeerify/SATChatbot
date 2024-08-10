from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from sentence_transformers import SentenceTransformer
import joblib
from core import speech2text
# from core import text2speech
from core import main
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from urllib.parse import unquote
from .models import Chat as ChatModel


class Chat(APIView):
    state = "GREETING"
    FINAL_STATE = "END2"
    buttons = []
    suggested_protocol_pool = []
    additionals = []
    addtional_num = 0
    name = ""
    dof = 0
    previous_questions_embeddings = []
    protocol = ""
    last_state = "GREETING"
    users_state = {}
    suggested_protocol_pool_state = {}
    model = main.Encod_Model()
    bot = main.Chatbot('/content/extracted_lists.yaml', model)

    def post(self, request):
        decoded_text = unquote(request.body.decode("utf-8"))
        print("boddyyyyyy", decoded_text)

        if "message" not in decoded_text:
            username = decoded_text[9:]
            print("username", username)
            Chat.users_state[username] = "GREETING"
            return Response({"status": "success"})

        print("type: ", type(decoded_text))
        message = request.body.decode('utf-8')[8:] #json.loads(request.body.decode('utf-8'))["message"]
        username = decoded_text.split("&")[0][9:].replace("+", " ")
        message = decoded_text.split("&")[1][8:].replace("+", " ")
        # message = unquote(decoded_text.split(":")[1][1:])
        print("text", message)
        try:
            file_obj = request.FILES["voice"]
            path = default_storage.save("stt/voice.wav", ContentFile(file_obj.read()))
            message = speech2text.speech2text("stt/voice.wav")
            print("voice", message)
        except:
            print("file not found!")

        if message == "restart":
            Chat.users_state[username] = "GREETING"

        # ## USAGE: DAILY DIARY
        # Chat.last_state = Chat.state
        # ###

        if username not in Chat.suggested_protocol_pool_state:
            Chat.suggested_protocol_pool_state[username] = []

        if username not in Chat.users_state:
            Chat.users_state[username] = ["GREETING"]

        (
            res,
            Chat.users_state[username],
            Chat.suggested_protocol_pool_state[username],
            Chat.buttons,
            Chat.additionals,
            Chat.addtional_num,
            Chat.name,
            Chat.dof,
        ) = Chat.bot.Information_Retrieval_System(Chat.users_state[username],
                                        message,
                                        Chat.suggested_protocol_pool_state[username],
                                        Chat.additionals,
                                        Chat.addtional_num,
                                        Chat.name,
                                        Chat.dof
                                    )

        ## DAILY DIARY
        # if res == "لطفا تمرین زیر رو انجام بده.":
        #     Chat.protocol = res.title
        # if Chat.last_state == "PROTOCOL_SUGGESTING3":
        #     with open("../core/daily_diary.txt", "a") as f:
        #         f.write("protocol:", Chat.protocol, "message:", message)
        ###

        # Create a new chat entry
        chat_entry = ChatModel(
            username=username,
            user_text=message,
            bot_text=res,
            state=Chat.users_state[username],
        )

        # Save the chat entry to the database
        chat_entry.save()

        if Chat.users_state[username] != Chat.FINAL_STATE:
            if res is str:
                # text2speech.text2speech(res)
                print("speech created!")
            print(res)
            return Response(
                {"status": "success", "response": res, "buttons": Chat.buttons},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": "end",
                "response": "امیدوارم تونسته باشم کمکت کنم.",
                "buttons": Chat.buttons,
            },
            status=status.HTTP_200_OK,
        )
