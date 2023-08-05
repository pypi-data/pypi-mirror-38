Tool send email via SMTP

Example code:
subject = 'subject here'
content = 'html content or plain content here'
cc = 'cc here or None'
bcc = 'bcc here or None'

from_addr = "send email from email"
to_addr = 'send email to email'

email_obj = Email('smtp.gmail.com', 587, 'smtp login username', 'smtp login pwd')
email_obj.send_mail(from_addr, to_addr, subject, content, cc, bcc)