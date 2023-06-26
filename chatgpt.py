from pynput import keyboard
from email.message import EmailMessage
import ssl,smtplib
import openai
#import sys.exit
global alist
alist=list()
def start(key):
    try:
        a=key.char
        if a=="\"":
            alist.append(a)
        elif alist:
            if alist[-1]=="shift":
                alist[-1]=a.upper()
            else:
                alist.append(a)
        if alist.count("\"")==2:
            # send it to chatgpt
            completion=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"user","content":"".join(alist)}])
            em= EmailMessage()
            em["From"]= email_sender
            em["To"] = email_receiver
            em["Subject"]=subject
            em.set_content(completion.choices[0].message.content)
            context= ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            print("yolladım")
            #print(completion.choices[0].message.content)
            alist.clear()
    except :
        a=key.name
        #if a=="alt_gr":
        #    sys.exit()
        # if any exit situation occurs this code statements will be considered!!!
        if alist:
            if a=="space":
                alist.append(" ")
            elif a=="backspace":
                alist.pop()
            elif a=="shift" and alist[-1] not in ("shift"," ","\""):
                alist.append(a)

if __name__=="main_":
    email_sender="" #Write the sender email
    password=""  #Password of the sender email
    email_receiver="" # Receiver and sender might be the same
    subject="Chatgpt answer"
    openai.api_key=""
    listener=keyboard.Listener(on_press=start)
    listener.start()
    input()