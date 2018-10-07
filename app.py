from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile
import requests
import re

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('61McGwsMpI8NWihh97arMsPWldpawwXmJpA8qRzJstMASY0xQ38g5MK0yK5AQN+9/4oTO1eqQ9E46zi1V0p/SFZxIeBmBX0Bt6il9gXlbABdP6d/QFU0VXtzJe2Q71po4XpUxm2UbtPUFw/FIAMAAQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('46aa35d5668f6a13ee7c871544287c91')
#===========[ NOTE SAVER ]=======================
notes = {}

#INPUT DATA MHS
def inputmhs(nrp, name, alamat):
    r = requests.post("http://www.aditmasih.tk/api_kelompok2/insert.php", data={'nrp': nrp, 'name': name, 'alamat': alamat})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+ name +' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'


# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)
    data = text.split('-')
    if(data[0] == 'tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = inputmhs(data[1],data[2],data[3])))


# def handle_message(event):
#     text = event.message.text #simplify for receove message
#     sender = event.source.user_id #get usesenderr_id
#     gid = event.source.sender_id #get group_id
#     profile = line_bot_api.get_profile(sender)
#     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Halo '+profile.display_name+'\nApa maksudmu bilang "'+text+'"?'))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)