import smtplib

sender_email = "yapsonstudio@gmail.com"
password = "hzrr upfj zisk axos"
receiver_email = "theau.yapi@ynov.com"
message = """\
Subject: Test SMTP

Ceci est un test d'envoi d'email via SMTP en utilisant un mot de passe d'application."""

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    server.quit()
    print("Email envoyé avec succès.")
except Exception as e:
    print(f"Erreur lors de l'envoi de l'email: {e}")
