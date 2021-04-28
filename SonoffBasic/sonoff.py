from aiohttp import ClientSession, WSMsgType, ClientConnectorError, WSMessage, ClientWebSocketResponse
import requests
import base64
import hashlib
import hmac
import json
import time


class Sonoff:
    def __init__(self, username: str, password: str, timezone: str='US/Pacific', region: str='us'):
        self.username = username
        self.password = password
        self.region = region
        self.timezone = timezone
        self.appid = 'oeVkj2lYFGnJu5XUtWisfW4utiN4u9Mq'
        self.appsecret = '6Nz4n0xA8s8qdxQf2GqurZj2Fs55FUvM'
        self.baseurl = f'https://{self.region}-api.coolkit.cc:8080/'
        self.ts = int(time.time())
        self.version = 8
        self.login()
        self.lang = 'en'
        self.devices()
   
    def login(self):
        payload = {
            'appid': self.appid,
            'nonce': str(self.ts),  # 8-digit random alphanumeric characters
            'ts': self.ts,  # 10-digit standard timestamp
            'version': self.version,
            'email': self.username, 
            'password': self.password
        }
        hex_dig = hmac.new(self.appsecret.encode(),
                           json.dumps(payload).encode(),
                           digestmod=hashlib.sha256).digest()
        auth = "Sign " + base64.b64encode(hex_dig).decode()
        r = requests.post(self.baseurl + 'api/user/login', json=payload, headers={'Authorization': auth}).json()
        self.token = r['at']
        self.auth = "Bearer " + r['at']

    def devices(self):
        payload = {
            'appid': self.appid,
            'lang': self.lang,
            'ts': self.token,
            'version': self.version,
            'nonce': str(self.ts) 
            }
        r = requests.get(self.baseurl + 'api/user/device', params=payload, headers={'Authorization': self.auth})
        devices = []
        for i in r.json()['devicelist']:
            if 'switches' in i['params']:
                for switch in i['params']['switches']:
                    d = {'name': i['name'],
                         'deviceid': i['deviceid'],
                         'outletid': switch['outlet'],
                         'status': switch['switch'],
                    # 'onlineTime': i['onlineTime'], TODO format as YYYY-MM-DD HH:MM:SS with tz
                    # 'offlineTime': i['offlineTime'
                         }
                    devices.append(d)

            else: #Single switch devices
                d = {'name': i['name'],
                     'deviceid': i['deviceid'],
                     'outletid': 0,
                     'status': i['params']['switch'],
                    # 'onlineTime': i['onlineTime'], TODO format as YYYY-MM-DD HH:MM:SS with tz
                    # 'offlineTime': i['offlineTime'
                    }
                devices.append(d)
        self.devices = devices

    def change_device_status(self, deviceid: str, new_status: str, outletid: int = 0):
        self.status = [stat.get('status') for stat in self.devices if stat.get('deviceid') == deviceid and stat.get('outletid') == outletid][0] 
        if new_status == self.status:
            print(f'device is already {new_status}')
            return

        if outletid != 0:
            params = {'switches': deviceid['params']['switches']}
            params['switches'][outletid]['switch'] = new_status

        else:
            params = {'switch': new_status }

        payload = {
            'action': 'update',
            'deviceid': deviceid,
            'params': params,
            'appid': self.appid,
            'lang': self.lang,
            'ts': self.token,
            'version': self.version,
            'nonce': str(self.ts)
            }

        r = requests.post(self.baseurl + 'api/user/device/status', data=json.dumps(payload), headers={'Authorization': self.auth})
        if r.json()['error'] == 0:
            print(f'deviceid: {deviceid} status successfully changed to {new_status}')
