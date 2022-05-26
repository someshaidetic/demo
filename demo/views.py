from django.shortcuts import render
from rest_framework.response import Response
from django.conf import settings
from twilio.twiml.voice_response import VoiceResponse,Say
from twilio.rest import Client
import requests


def get_custom_response(success=False, message='something went wrong', data=None, status=400):

    response = {
        'success': success,
        'message': message,
        'data': data
    }
    return Response(response, status=status)

# Create your views here.
def Call(request):
    # Get phone number we need to call
    try:
        url=None
        phone_number = requests.post(url)
    except Exception as e:
        # raise e
        phone_number = request.GET.get('phoneNumber', 8286739482)


    if not phone_number:
        msg = 'Missing phone number value'
        # return get_custom_response(message=msg)
        raise Exception
    try:
        twilio_client = Client(settings.TWILIO_ACCOUNT_SID,
                            settings.TWILIO_AUTH_TOKEN)
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return get_custom_response(message=msg)

    try:
        res = twilio_client.calls.create(from_=settings.TWILIO_CALLER_ID,
                                   to=phone_number,
                                #    url='https://b482-117-96-242-84.in.ngrok.io/outbound'
                                   url='http://demo.twilio.com/docs/voice.xml',
                                               )

        print('----------->',res.sid)
    
    except Exception as e:
        # app.logger.error(e)
        message = e.msg if hasattr(e, 'msg') else str(e)
        return get_custom_response(message=message)
    msg="Incoming Call!"
    return get_custom_response(message=msg)