from django.core.mail import send_mail
from django.conf import settings
import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                self.subject,
                self.message,
                settings.EMAIL_HOST_USER,
                self.recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Błąd wysyłania maila: {e}")

def send_welcome_email(user_email, username):
    subject = "Witaj w naptaku!"
    message = f"""
    Cześć {username}!

    Dziękujemy za rejestrację w serwisie Mamsmaka naptaka.
    Nie pytaj co to ten naptak.
    Cieszymy się, że dołączyłeś!
    
    Możesz teraz dodawać własne przepisy i pisać recenzję innych.
    
    Pozdrawiamy,
    Zespół Bizon 🦬
    """
    
    EmailThread(subject, message, [user_email]).start()