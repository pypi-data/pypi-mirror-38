# vumasms-python
VumaSMS REST API client for Python. API support for bulk SMS, Numbers, Verify (2FA) and more.

# installation
```
pip install vumasms
```

Create a test.py script and in it add the following
```
from vumasms.VumaSMS import VumaSMS
API_TOKEN = "<from vuma portal>";
API_SECRET = "<from vuma portal>"
SMS_BODY = { 
             "to":["2547XXXXXXX"],
             "sender":"VUMA",
             "message":"Test message from the vumasms Python Client",
             "scheduled_date":"",
             "scheduled_type":""
           }
vuma = VumaSMS(API_TOKEN,API_SECRET)
print vuma.send_sms(SMS_BODY)
```
