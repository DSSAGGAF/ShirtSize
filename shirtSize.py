import telebot
import sys
import os
from PIL import Image
import cv2
import mediapipe as mp

telegram_token = '1472069887:AAGqI2csyTUzCPbsRlXyrGC00RaNGaG_1n4'
bot = telebot.TeleBot(telegram_token)
sensorH= 33.50
dis=720
focal=32
w11=0
w12=0
wt=0
objh=0
real=0
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose


@bot.message_handler(commands=['Hi'])
def greeting(message):
    bot.reply_to(message,"fuck u")

@bot.message_handler(content_types= ["photo"])
def img(message):
    # print(message)
    # print(message.photo[0])
    # print(message.photo[2])
    # print(message.photo[2].file_id)
    pose = mpPose.Pose()
    raw = message.photo[2].file_id
    path = raw+".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path,'wb') as new_file:
        new_file.write(downloaded_file)
    im = Image.open(path)
    width, height = im.size
    cap = cv2.VideoCapture(path)

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        # mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    # print(w12)
    # print(w11)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            
            h, w, c = img.shape
            # print(id, lm)
            if id == 11:
                # print(id,lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                w11=round(lm.x,4) * width
            elif id ==12:
                # print(id,lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                w12 = round(lm.x,4) * width
                # print(id, lm)
                # print(lm.x)
    # print(w11)
    # print(w12)
    # print(width)            
    wt = w11 - w12    
    # print(wt)
    del pose
    del results
    objh = (sensorH * wt)/width
    real = (dis * objh) / focal
    print(real)
    bot.reply_to(message,real)
    
bot.polling()