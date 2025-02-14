from fastapi import FastAPI
import requests
import uuid
import string
import random
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get('/rest/{email}')
def send_reset_password(email: str):
    try:
        
        if not email:
            return JSONResponse(content={'error': 'Email is required'}, status_code=400)

        url = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
        csrf_token = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32))

        headers = {
            'Content-Length': '319',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Instagram 6.12.1 Android (30/11; 320dpi; 720x1339; realme; RMX3269; RED8F6; RMX3265; ar_IQ)',
            'Accept-Language': 'ar-IQ, en-US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': 'AQ==',
            'Accept-Encoding': 'gzip',
        }

        data = {
            'user_email': email,
            'device_id': str(uuid.uuid4()),
            'guid': str(uuid.uuid4()),
            '_csrftoken': csrf_token
        }

        response = requests.post(url, headers=headers, data=data)

        if "obfuscated_email" in response.text:
            return JSONResponse(content={'message': f'Password reset link sent to {email}', "rest": response.json().get("obfuscated_email"),"By":"@jokerpython3"}, status_code=200)
        else:
            return JSONResponse(content={'error': 'Please use VPN or try again later'}, status_code=400)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)
