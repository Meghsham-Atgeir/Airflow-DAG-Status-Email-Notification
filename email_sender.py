from email.message import EmailMessage
import ssl
import smtplib
import configparser
import datetime
from rich.console import Console
console = Console()
def send_email(dags, status):
    config = configparser.ConfigParser()
    config.read('project.ini')

    smtp_server = config['Email']['smtp_server']
    smtp_port = config.getint('Email', 'smtp_port')
    sender_email = config['Email']['sender_email']
    sender_password = config['Email']['sender_password']
    receivers = [email.strip() for email in config['Email']['receivers'].split(',')]

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    if len(status) > 1:
        subject = f"List of {' & '.join(status)} DAGs - {current_date}"
    else:
        subject = f"List of {' '.join(status)} DAGs - {current_date}"

    body = f"""\
<html>
<head>
<style type="text/css">
    .success {{
        color: green;
    }}

    .failed {{
        color: red;
    }}
</style>
</head>
<body>
<h2>{subject}</h2>
<table border='1'>
<tr>
<th>DAG ID</th>
<th>DAG Run ID</th>
<th>Task ID</th>
<th>Duration</th>
<th>Execution Date</th>
<th>State</th>
</tr>
"""

    for dag_info in dags:
        body += "<tr>"
        for info in dag_info:
            if info == dag_info[-1] and str(info).lower() == 'failed':
                body += f"<td class='failed'>{info}</td>"
            elif info == dag_info[-1] and str(info).lower() == 'success':
                body += f"<td class='success'>{info}</td>"
            else:
                body += f"<td>{info}</td>"

        body += "</tr>"

    body += "</table></body></html>"


    try:
        em = EmailMessage()
        em['From'] = sender_email
        em['Subject'] = subject
        em['Bcc'] = ', '.join(receivers)  # Bcc recipients

        em.add_alternative(body, subtype='html')

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.send_message(em)

        if len(receivers) > 1:
            console.print("[green]Email Sent Successfully to multiple recipients")
        else:
            console.print("[green]Email Sent Successfully to a single recipient")
    except Exception as err:
        console.print(f"[red] Error sending Email due to {err}")

