from kavenegar import *

from socialnetwork.settings import API_KEY


def kave_negar_token_send(receptor, token):
    try:
        import json
    except ImportError:
        import simplejson as json
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': '10004346',
            'receptor': receptor,
            'message': str(token)
        }
        response = api.sms_send(params)
    except APIException as e:
        print(str(e))
    except HTTPException as e:
        print(str(e))
