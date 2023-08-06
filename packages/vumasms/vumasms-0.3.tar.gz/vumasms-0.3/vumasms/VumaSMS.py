import requests
import base64
import json
from Crypto import Random
from Crypto.Cipher import AES



class VumaSMS:
	 _url = "https://www.vumasms.com/api/send/sms"
	 iv = Random.new().read(AES.block_size)	
    
	 def __init__(self, token, secret):
	 	self.token = token
	 	self.secret = secret
	 def send_sms(self,payload):
	 	self.payload = payload
	 	self.response = requests.request("POST", self._url, data=self._payload(), headers=self._headers())
	 	return self.response.text

	 def _payload(self):
	 	self._boundary = "----VumaApiKitFormBoundary"+self.encode(self.secret)
	 	payload = "--"+self._boundary+"\r\nContent-Disposition: form-data; name=\"payload\"\r\n\r\n"+json.dumps(self.payload)+"\r\n--"+self._boundary+"--"
	 	return payload

	 def _headers(self):
	 	return {'content-type': "multipart/form-data; boundary="+self._boundary,'cache-control': "no-cache",'Authorization': "Bearer "+self.token}
	 def encode(self,message):
	 	obj = AES.new(self.secret, AES.MODE_CFB, self.iv)
	 	return base64.urlsafe_b64encode(obj.encrypt(message))         
         
	 def decode(cipher):
	 	obj2 = AES.new(AKEY, AES.MODE_CFB, self.iv)
	 	return obj2.decrypt(base64.urlsafe_b64decode(cipher))