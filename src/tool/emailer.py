from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import uuid
from tool.colorprint import Cprint, bcolor



def sendtoemail(verify_colletion, email, userId):
  content = MIMEMultipart()
  content["subject"] = "[noreply] Parkinson Detect Website Account | Please verify your mail"
  content["from"] = "parkinson.noreply@gmail.com"
  content["to"] = email
  token = str(uuid.uuid4())
  verify_link = f"http://10.1.0.27:3000/verify?token={token}&user_id={userId}"
  content.attach(MIMEText(f'<a href=\"{verify_link}\">Click Here to Verify</a>', 'html'))

  with smtplib.SMTP(host="smtp.gmail.com",port="587") as smtp:
    try:
      smtp.ehlo()
      smtp.starttls()
      smtp.login("parkinson.noreply@gmail.com","vbsimsysoafmkudc")
      smtp.send_message(content)
      print("email sent")
      verify_colletion.insert_one({
            "email": email,
            "email_token": token,
            "expire": datetime.utcnow() + timedelta(minutes=10)
        })
      return token
    except Exception as e:
      Cprint(e, bcolor.FAIL)


def changepasswordemail(verify_colletion, email):
  content = MIMEMultipart()
  content["subject"] = "[noreply] Parkinson Detect Website Account | Please Press To Change Your Password"
  content["from"] = "parkinson.noreply@gmail.com"
  content["to"] = email
  token = str(uuid.uuid4())
  verify_link = f"http://10.1.0.27:3000/verify/change?token={token}&email={email}"
  content.attach(MIMEText(f'<a href=\"{verify_link}\">Click Here to Change password</a>', 'html'))

  with smtplib.SMTP(host="smtp.gmail.com",port="587") as smtp:
    try:
      smtp.ehlo()
      smtp.starttls()
      smtp.login("parkinson.noreply@gmail.com","vbsimsysoafmkudc")
      smtp.send_message(content)
      verify_colletion.insert_one({
        "email": email,
        "email_token": token,
        "expire": datetime.utcnow() + timedelta(minutes=10)
      })
      return token
    except Exception as e:
      print("Error message")


