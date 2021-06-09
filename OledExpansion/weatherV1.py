import requests
import os
from time import sleep
from datetime import datetime
api_key = <API_KEY>
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = <CITY_NAME>
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
os.system("oled-exp -i")
while True:
    try:
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            now = datetime.now().strftime("%Y/%b/%d %H:%M:%S")
            y = x["main"]
            current_temperature = y["temp"]
            feels = y["feels_like"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            os.system("oled-exp -c > /dev/null")
            os.system("oled-exp cursor 0,0 > /dev/null")
            os.system("oled-exp write 'Temp: {}' > /dev/null".format(str(current_temperature)[:4] + " C"))
            os.system("oled-exp cursor 1,0 > /dev/null")
            os.system("oled-exp write 'Feels: {}' > /dev/null".format(str(feels)[:4] + " C"))
            os.system("oled-exp cursor 3,0 > /dev/null")
            os.system("oled-exp write 'Humidity: {}' > /dev/null".format(str(current_humidity) + "%"))
            os.system("oled-exp cursor 4,0 > /dev/null")
            os.system("oled-exp write 'Description: {}' > /dev/null".format(str(weather_description).title()))
            os.system("oled-exp cursor 7,0 > /dev/null")
            os.system("oled-exp write '{}' > /dev/null".format(now))
            with open("/mnt/mmcblk0p1/weather_log", "a") as logFile:
                logFile.write(now +" "+ str(x) + "\n")
        else:
            os.system("oled-exp write ERROR!")
            raise Exception
    except Exception as e:
        with open("/mnt/mmcblk0p1/weather_log", "a") as logFile:
            logFile.write(str(sys.exc_info()[0]))
            logFile.write(str(e))
    sleep(1800)
