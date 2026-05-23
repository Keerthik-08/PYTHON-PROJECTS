import requests
import smtplib
from email.mime.text import MIMEText

# --------- CONFIG ---------
API_KEY = "4eede592ee043abc23b194378625318c"
CITY = "tiruvallur"

EMAIL = "kkrithika726@gmail.com"
PASSWORD = "wuwcpfgfjgryotzg"
TO_EMAIL = "krithikaindira2006@gmail.com"

# --------- GET WEATHER DATA ---------
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()
if data["cod"]!=200:
    print("error:",data["message"])
    exit()

weather = data["weather"][0]["main"]
temp = data["main"]["temp"]
print(f"Weather in {CITY}: {weather}, Temp: {temp}°C")

# --------- CHECK WEATHER ---------
if weather.lower() in ["rain", "clouds"]:
    
    message = f"Hey! Today weather is {weather} in {CITY}. Don't forget to take an umbrella ☔"

    msg = MIMEText(message)
    msg["Subject"] = "Weather Alert!"
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    # --------- SEND EMAIL ---------
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
    server.quit()

    print("Email sent successfully!")
else:
    print("No rain today 😄")