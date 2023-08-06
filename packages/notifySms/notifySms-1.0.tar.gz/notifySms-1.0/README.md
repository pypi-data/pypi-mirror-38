This program helps to send sms notification to specified mobile.

Pre-Requisite : 
    - Twilio account, Its Account, Token And Moblile number.

Usage : 
<pre>
1. Using Program to send sms.
   python sendSms.py [Message needs to be sent]
2. Using module in other script to nofiy via sms.
    from nofiySms import sendSms
    sendSms.send_sms("Message body",[To Number]) 
</pre>