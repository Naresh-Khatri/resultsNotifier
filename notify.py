import smtplib

server = smtplib.SMTP_SSL("smtp.gmail.com:465")
server.login("rosisgreaterthanpubg@gmail.com", "poojapooja1")
server.sendmail(
    "rosisgreaterthanpubg@gmail.com",
    "naresh.khatri2345@gmail.com",
    "This is a bot... beep boop beep boop... testing 1...2....3....")

server.quit()