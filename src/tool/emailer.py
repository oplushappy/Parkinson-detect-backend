from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import uuid

def sendtoemail(email, userId):
  content = MIMEMultipart()
  content["subject"] = "[noreply] Parkinson Detect Website Account | Please verify your mail"
  content["from"] = "parkinson.noreply@gmail.com"
  content["to"] = email
  token = str(uuid.uuid4())
  verify_link = f"http://10.10.0.27:3000/verify?token={token}&user_id={userId}"
  content.attach(MIMEText(f'<a href=\"{verify_link}\">Click Here to Verify</a>', 'html'))

  with smtplib.SMTP(host="smtp.gmail.com",port="587") as smtp:
    try:
      smtp.ehlo()
      smtp.starttls()
      smtp.login("parkinson.noreply@gmail.com","vbsimsysoafmkudc")
      smtp.send_message(content)
      print("completed")
      return token
    except Exception as e:
      print("Error message")


