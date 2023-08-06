from vumasms.VumaSMS import VumaSMS

API_TOKEN = "<from vuma portal>";
API_SECRET = "2222222233333333"
SMS_BODY = { 
             "to":["254723681977"],
             "sender":"VUMA",
             "message":"Test message from the vumaSMS Python Client",
             "scheduled_date":"",
             "scheduled_type":""
           }

vuma = VumaSMS(API_TOKEN,API_SECRET)
print vuma.send_sms(SMS_BODY)