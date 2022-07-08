import telebot
from telebot import types 
from turtle import update
from bs4 import BeautifulSoup
from time import sleep, time
import requests
import json
import sys
import os

from telegram import InlineKeyboardMarkup
print("Bot Is Started")
token = "5502185335:AAHt-PkXQWAlusaXdVIgBvlc0YqGmYT8OxM"
sudo_id = ''
bot = telebot.TeleBot(token)
ch ="titantrex"
msg = """مرحباً، هذا البوت يقوم بتحميل القصص من السناب شات بالكامل. كل ماعليك هو ققط ادخال اسم المستخدم.
🍔 لإستخدام هذه الخدمة يجب عليك الإنضمام الى هذه القناة - : @titantrex """

msg2 = """
● طريقة استخدام البوت
● قم بإرسال اسم المستخدم وسيقوم البوت بتحميل القصة الخاصة به بالكامل
● البوت يدعم تطبيق سناب شات فقط
● يجب ان يكون الحساب لديه ملف تعريفي عام
● يعمل في جميع الأوقات."""
def gituser(id):
    result = False
    file = open ("users.txt",'r')
    for line in file:
        if line.strip()==id:
            result = True
    file.close()
    return result



keyborad = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text= "انضممت" , callback_data="click1")
keyborad.add(button1)
def start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    chat = types.KeyboardButton(text="ادخل اسم المستخدم-",)
    chat2 = types.KeyboardButton(text="⚙️ طريقة استخدام البوت",)
    markup.add(chat,chat2)

    return markup 
@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type == 'private':
      idu = message.from_user.id
      f = open("users.txt",'a')
      if(not gituser(str(idu))):
        f.write("{}\n".format(idu))
        f.close()  
    id = message.from_user.id
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={id}"
    req = requests.get(url)
    if id == sudo_id or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        bot.send_message(message.chat.id, "🏡الرئيسية" ,reply_markup=start_markup())
    else:
       bot.send_message(message.chat.id, "{}".format(msg),reply_markup=keyborad)
@bot.message_handler(commands=["users"])
def get(message):
    
    file = open("users.txt",'r')
    lines = 0
    for line in file:
        words = line.split(" ")
        lines += len(words)
    file.close()
    bot.send_message(message.chat.id,"users : {}".format(lines))
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
        if call.data == "click1":
            id = call.from_user.id
            url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={id}"
            req = requests.get(url)
            if id == sudo_id or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="تم التفعيل ",)
                bot.answer_callback_query(call.id, "تم التفعيل ✅ .")
            if id == sudo_id or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
                bot.send_message(call.message.chat.id, "🏡الرئيسية" ,reply_markup=start_markup())
@bot.message_handler()
def re(m):
                id = m.from_user.id
                url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={id}"
                req = requests.get(url)
                if id == sudo_id or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
                    
                    if m.text == "ادخل اسم المستخدم-":
                        bot.send_message(m.chat.id,"قم بإرسال اسم المستخدم الآن")
                    elif m.text == "⚙️ طريقة استخدام البوت":
                        bot.send_message(m.chat.id,msg2 , reply_markup=start_markup())
                    elif m.text == str(m.text) not in  "ادخل اسم المستخدم-":
                            bot.send_message(m.chat.id,"جاري التاكد من المستخدم ...")
                            userr=m.text
                            url = "https://story.snapchat.com/@"
                            mix = url + str(userr)
                            headers = {
                                'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
                            }

                            r = requests.get(mix, headers=headers)

                            if r.ok:
                                bot.send_message(m.chat.id,'تم العثور علئ المستخدم')


                            else:
                                bot.send_message(m.chat.id,'لام يتم العثور علئ الحساب')
                                sys.exit(1)

                            soup = BeautifulSoup(r.content, "html.parser")
                            #print(soup)

                            snaps = soup.find(id="__NEXT_DATA__").string.strip()


                            data = json.loads(snaps)

                            try:
                                bitmoji = data["props"]["pageProps"]["userProfile"]["publicProfileInfo"]["snapcodeImageUrl"]
                                bio = data["props"]["pageProps"]["userProfile"]["publicProfileInfo"]["bio"]

                            except KeyError:
                                bitmoji = data["props"]["pageProps"]["userProfile"]["userInfo"]["snapcodeImageUrl"]
                                bio = data["props"]["pageProps"]["userProfile"]["userInfo"]["displayName"]
                                bot.send_message(m.chat.id,'الحساب خاص')
                                sys.exit(1)





                            try:
                                for i in data["props"]["pageProps"]["story"]["snapList"]:

                                    file_url = i["snapUrls"]["mediaUrl"]

                                    if file_url == "":
                                        continue

                                    r = requests.get(file_url, stream=True, headers=headers)
                                    unl = r.url

                                    if "image" in r.headers['Content-Type']:
                                        file_name = r.headers['ETag'].replace('"', '') + ".jpeg"
                            
                                        bot.send_photo(m.chat.id,unl)
                                    elif "video" in r.headers['Content-Type']:
                                        file_name = r.headers['ETag'].replace('"', '') + ".mp4"

                                        bot.send_video(m.chat.id,unl)

                                        continue
                                
                                    sleep(0.3)	


                            except KeyError:
                                bot.send_message(m.chat.id,'لام يتم التنزيل مقاطع او صور اليوم')
                            else:
                                bot.send_message(m.chat.id,'تم التنزيل')
                                bot.send_message(m.chat.id,"تابعنا على حسابنا في سناب شات: sr2ip https://www.snapchat.com/add/sr2ip")

                        

bot.infinity_polling()
