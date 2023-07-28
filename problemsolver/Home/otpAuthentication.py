from django.conf import settings
from django.core.mail import send_mail
def send_otp(otp, recipient):
    try:
        subject="OTP from Solver"
        message=f"OTP:- {otp}"
        from_email=settings.EMAIL_HOST_USER
        recipt=[recipient]
        send_mail(subject, message, from_email, recipt)
        return("Sucessfully send email")
    except Exception as e:
            return e