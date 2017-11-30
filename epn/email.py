from email.message import EmailMessage
from email.headerregistry import Address
from email.mime.base import MIMEBase
from email.utils import make_msgid, format_datetime
from django.template import Context, loader
import smtplib, io
from email import encoders


from valdyerresweb.settings import DEBUG
from valdyerresweb.settings import epnemailvyvs


fileio = io.BytesIO()
msg = EmailMessage()

if DEBUG:
    recipients = ['r@vyvs.fr']
    server = ("127.0.0.1")
    port = "1025"
else:
    server = epnemailvyvs.server
    port = "25"
    recipients = [mailto]

msg['Subject'] = "[VYVS EPN] " + sujet + " " + hier.strftime("%d/%m/%y")
msg['From'] = Address("Val d'Yerres Val de Seine", "robot", "vyvs.fr")
msg['Reply-To'] = Address("Val d'Yerres Val de Seine", "accueil", "vyvs.fr")
msg['To'] = ",".join(recipients)
msg['Date'] = format_datetime(datetime.now())

texttemplate = loader.get_template('01-epn-mail_text.html')
mycontext = Context({'erreurs': erreurs})
text = texttemplate.render(mycontext)
texttemplate = loader.get_template('01-epn-mail_html.html')
html = texttemplate.render(mycontext)

msg.set_content(text)
dlflogocid = make_msgid()
msg.add_alternative(html.replace("{vyvs-logocid}", dlflogocid[1:-1]), subtype="html")

with open(os.path.join(MY_BASE_DIR, 'img/logo-blanc-vyvs-200.jpg'),
          'rb') as img:
    msg.get_payload()[1].add_related(img.read(), 'image', 'png', cid=dlflogocid)

part = MIMEBase('application', "octet-stream")
fileio.seek(0)
part.set_payload(fileio.getvalue())
encoders.encode_base64(part)
part.add_header('Content-Disposition',
                'attachment; filename="compta-' + slugify(sujet) + "-" + hier.strftime("%d%m%y") + '.xlsx"')
msg.attach(part)
mailserver = smtplib.SMTP()
mailserver.connect(server, port)
mailserver.ehlo()
mailserver.login(epnemailvyvs.login, epnemailvyvs.password)
mailserver.send_message(msg)
mailserver.quit()