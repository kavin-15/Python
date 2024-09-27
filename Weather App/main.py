import requests
import win32com.client as wincl
import json

city = input("Please enter the name of the city\n")

url = f"http://api.weatherapi.com/v1/current.json?key=13f0548534fb4bcbb9985134242609&q={city}"
k = requests.get(url)

city_dic = json.loads(k.text)
a = city_dic["current"]["temp_c"]
b = str(a)+" celsius"
print(b)
speak = wincl.Dispatch("SAPI.SpVoice")
speak.Speak(b)