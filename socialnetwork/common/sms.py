from kavenegar import KavenegarAPI, APIException, HTTPException

from socialnetwork.settings import API_KEY


def kave_negar_token_send(receptor, token):
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'receptor': receptor,
            'template': 'your_template',
            'token': token
        }
        response = api.verify_lookup(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)