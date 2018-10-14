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

# #REQUEST DATA ADMIN RPL
# def caritmn(nrp):
#     URLtmn = "http://www.aditmasih.tk/api_hans/show.php?nrp=" + nrp
#     r = requests.get(URLtmn)
#     data = r.json()
#     err = "Data tidak ditemukan"

#     flag = data['flag']
#     if(flag == "1"):
#         nrp = data['data_teman'][0]['nrp']
#         nama = data['data_teman'][0]['nama']
#         jenis_kelamin = data['data_teman'][0]['jenis_kelamin']
#         nomor_hp = data['data_teman'][0]['nomor_hp']

#         data= "Nama : "+nama+"\nNRP : "+nrp+"\nGender : "+jenis_kelamin+"\nNo. HP : "+nomor_hp
#         return data

#     elif(flag == "0"):
#         return err

#INPUT DATA TMN
def inputtmn(nrp, nama, jenis_kelamin, nomor_hp):
    r = requests.post("http://www.aditmasih.tk/api_hans/insert.php", data={'nrp': nrp, 'nama': nama, 'jenis_kelamin': jenis_kelamin})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data si '+ name +' berhasil dimasukin. Gila temen lu nambah.\n'
    elif(flag == "0"):
        return 'Data gagal dimasukin. Coba lagi deh.\n'

def alltmn():
    r = requests.post("http://www.aditmasih.tk/api_hans/all.php")
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        hasil = ""
        for i in range(0,len(data['data_teman'])):
            nrp = data['data_teman'][int(i)]['nrp']
            nama = data['data_teman'][int(i)]['nama']
            jenis_kelamin = data['data_teman'][int(i)]['jenis_kelamin']
            nomor_hp = data['data_teman'][int(i)]['nomor_hp']
            hasil=hasil+str(i+1)
            hasil=hasil+".\nNrp : "
            hasil=hasil+nrp
            hasil=hasil+"\nNama : "
            hasil=hasil+nama
            hasil=hasil+"\nGender : "
            hasil=hasil+jenis_kelamin
            hasil=hasil+"\nNomor HP : "
            hasil=hasil+nomor_hp
            hasil=hasil+"\n"
        return hasil
    elif(flag == "0"):
        return 'Data gagal dimasukkan. Mungkin emang lo nggak punya teman.\n'


#DELETE DATA MHS
def hapustmn(nrp):
    r = requests.post("http://www.aditmasih.tk/api_hans/delete.php", data = {'nrp': nrp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+ nrp +' berhasil dihapus. Selamat lo berhasil move on dari si dia.\n'
    elif(flag == "0"):
        return 'Data gagal dihapus bro. Gagal move on lo.\n'

def updatetmn(nrpLama, nrp, nama, jenis_kelamin, nomor_hp):
    URLtmn = "http://www.aditmasih.tk/api_hans/show.php?nrp=" + nrpLama
    r = requests.get(URLtmn)
    data = r.json()
    err = "Nggak nemu bos. Salah ketik mungkin."
    nrp_lama=nrpLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api_hans/update.php", data={'nrp': nrp, 'nama': nama, 'jenis_kelamin': jenis_kelamin, 'nomor_hp' = nomor_hp, 'nrp_lama':nrp_lama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data temen lo, si '+nama+'dengan nrp '+nrp_lama+'ini, berhasil diupdate.\n'
        elif(flag == "0"):
            return 'Data gagal diupdate bro. Mungkin lo belum konek ke WiFi TC.\n'

    elif(flag == "0"):
        return err


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
    if(data[0] == 'Cari'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = caritmn(data[1])))
    elif(data[0] == 'Tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = inputtmn(data[1],data[2],data[3],data[4])))
    elif(data[0] == 'Hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = hapustmn(data[1])))
    elif(data[0] == 'Ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = updatetmn(data[1],data[2],data[3],data[4],data[5])))
    elif(data[0] == 'Semua'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = alltmn()))
    elif(data[0] == 'Menu'):
        menu = "1. Cari-[nrp]\nIni buat lo nyari data temen lo pake nrp\n\n2. Tambah-[nrp]-[nama]-[jenis kelamin(L/P)]-[no hp]\nSemisal lo punya temen baru, ini buat masukin ke data dia ke database lo, biar nggak lupa.\n\n3. Hapus-[nrp]\nIni buat menghapus temen lo yang mungkin lo ga suka.\n\n4. Ganti-[nrp lama]-[nrp baru]-[nama baru]-[jenis kelamin baru]-[no hp baru]\nSiapa tau temen lo uda berubah, pastiin datanya lo ganti juga.\n\n5. Semua\nIni buat nampilin seluruh data temen lo (kalo lo punya temen)."
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = menu))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "Ga ketangkep bos"))

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