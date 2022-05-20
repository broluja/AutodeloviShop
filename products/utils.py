from Autodelovi.settings import MAIL_API_KEY, MAIL_SECRET_KEY, HOST_EMAIL
from mailjet_rest import Client


def send_email(receiver, subject='Order', template=None, user=None):

    mailjet = Client(auth=(MAIL_API_KEY, MAIL_SECRET_KEY), version='v3.1')
    data = {
        'Messages': [
            {
                'From': {
                    'Email': HOST_EMAIL,
                    'Name': 'Load66.Admins'
                },
                'To': [
                    {
                        'Email': receiver,
                        'Name': user if user else 'User'
                    }
                ],
                'Subject': subject,
                'TextPart': 'Greetings from Load66.net',
                'HTMLPart': template
            }
        ]
    }
    mailjet.send.create(data=data)
