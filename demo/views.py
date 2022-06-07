import os
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client


base_url = os.environ["NGROK"]


def get_custom_response(
    success=False, message="something went wrong", data=None, status=400
):
    response = {"success": success, "message": message, "data": data}
    return Response(response, status=status)


@api_view(["POST"])
def call(request):
    """Initiates the call

    Args:
        request (http): this is the request made from client side to the server to initiate a interactive voice call.

    Raises:
        Exception: this is a case when a certain line of code disrupts the flow of the program

    Returns:
        HttpResonse: It returns  with a http response from twilio client on successfull call
    """

    try:
        url = None
        response = requests.get(url)
        response = {}
        response["phone_number"] = settings.PHONE_NUMBER
        phone_number = response.get("phone_number")

    except Exception as e:
        phone_number = request.data.get("phone_number")
        phone_number = settings.PHONE_NUMBER

    msg = "Missing phone number value" if not phone_number else None

    try:
        twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    except Exception as e:
        msg = "Missing configuration variable: {0}".format(e)
        return get_custom_response(message=msg)

    try:
        print(f"{base_url}/demo/play")
        res = twilio_client.calls.create(
            from_=settings.TWILIO_CALLER_ID,
            to=phone_number,
            url=f"{base_url}/demo/play",
        )
        msg = f"Incoming Call!"
        return HttpResponse(str(msg), content_type="application/xml; charset=utf-8")

    except Exception as e:
        message = e.msg if hasattr(e, "msg") else str(e)
        return get_custom_response(message=message)


@csrf_exempt
def playAudio(request):
    """This api runs and records the interaction inside the call initialized via twilio modules

    Args:
        request (http): the purpose of this http request is to continue the IVR call
        by accessing resource on the server and saving the response of the end user

    Returns:
        HttpResponse: this api returns the twilio response with content_type in application/xml
        and redirects the api to the url specified in action variable
    """
    try:
        response = VoiceResponse()
        url = "path_of_audio_clip"
        # response.play(url,loop=1)
        response.say(
            """Is this somesh?  Please leave a message at the beep.\nPress the star key when finished.""",
            voice="alice",
        )
        response.record(
            timeout=5,
            transcribe=True,
            recording_status_callback=f"{base_url}/demo/recording/callback",
            action=f"{base_url}/demo/interact",
            method="GET",
            finish_on_key="*",
        )
        response.say("I did not receive a recording")
        return HttpResponse(
            str(response), content_type="application/xml; charset=utf-8"
        )
    except Exception as e:
        return get_custom_response(message=str(e))


@csrf_exempt
def callback(request):
    """This is the recording_status_callback method after a successfull response from the end user

    Args:
        request (http): The purpose of this http resquest is to trigger when a particular response
        is gathered from user and the recording_url can be processed further

    Returns:
        HttpResponse: This method requests the api of the ML model
        and passes the recorded audio path to the ML model on server
    """
    try:
        recorded_audio_url = request.POST.get("RecordingUrl")
        print(recorded_audio_url)
        url = os.environ(['MODEL_URL'])
        payload = {"url": recorded_audio_url}
        response = requests.post(url=url, json=payload)
        print(response.json)
        return HttpResponse(
            str(response), content_type="application/xml; charset=utf-8"
        )
    except Exception as e:
        print(e)
        return get_custom_response(message=str(e))


@csrf_exempt
def interact(request):
    """This api continues the IVR call

    Args:
        request (http): _description_

    Returns:
        _type_: this api plays the audio file in continuation to the IVR call
        and return the HttpResponse of the twilio's VoiceResponse module
    """
    try:
        response = VoiceResponse()
        response.say("Thank you for you feedback", voice="alice")
        return HttpResponse(
            str(response), content_type="application/xml; charset=utf-8"
        )
    except Exception as e:
        return get_custom_response(message=str(e))
