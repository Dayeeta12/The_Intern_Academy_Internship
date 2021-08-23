from PIL import Image, ImageTk
import io
import requests
from tkinter import Tk, Label, Button, LabelFrame, Entry
from urllib.request import urlopen


# GUI Frame
mainWindow = Tk()
mainWindow.title("Weather App")
mainWindow.geometry("1200x720")
mainWindow.configure(bg="white")

url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
headers = {
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
    'x-rapidapi-key': "5b3b634cf3mshd2f0931908f6d8bp12ef13jsn39395680ab98"  # todo: have to hide my API
}

# logic to get weather report
def weather():
    global photo
    querystring = {"q": entry_label.get(), "days": "3"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    # current weather updates
    place = data["location"]["name"]
    state = data["location"]["region"]

    current_temp_C = data["current"]['temp_c']
    current_temp_F = data["current"]["temp_f"]

    last_update_date = data['current']["last_updated"]

    curr_condition = data["current"]["condition"]["text"]
    curr_humidity = data["current"]["humidity"]

    photo_url = "http:" + data["current"]["condition"]["icon"]
    photo_byte = io.BytesIO(urlopen(photo_url).read())
    pil_image = Image.open(photo_byte)
    photo = ImageTk.PhotoImage(pil_image)

    location_info = place + ", " + state
    large_info = str(current_temp_C) + "°C " + "| " + str(current_temp_F) + "°F"
    final_data = "\n" + f"Condition: {curr_condition}" + "\t\t" + f"Humidity: {curr_humidity}" + "\n" + \
                 f"Last Update: {last_update_date}" + '\n'

    location_view.config(text=location_info)
    Label(labelFrame, bg='white', image=photo).grid(row=2, column=0)
    large_view.config(text=large_info)
    small_view.config(text=final_data)

    # next 3 days report
    all_datas = []
    for i in range(3):
        date = data["forecast"]['forecastday'][i]['date']
        max_temp_C = data["forecast"]['forecastday'][i]['day']['maxtemp_c']
        max_temp_F = data["forecast"]['forecastday'][i]['day']['maxtemp_f']
        min_temp_C = data["forecast"]['forecastday'][i]['day']['mintemp_c']
        min_temp_F = data["forecast"]['forecastday'][i]['day']['mintemp_f']
        chanceOfRain = data["forecast"]['forecastday'][i]['day']['daily_chance_of_rain']
        conditions = data["forecast"]['forecastday'][i]['day']['condition']['text']
        humidity = data["forecast"]['forecastday'][i]['day']['avghumidity']
        sunrise = data["forecast"]['forecastday'][i]['astro']['sunrise']
        sunset = data["forecast"]['forecastday'][i]['astro']['sunset']

        info = f"Date: {date}" + '\n\n' + f"Max Temp: {max_temp_C}°C  |  {max_temp_F}°F" + \
               "\n" + f"Min Temp: {min_temp_C}°C  |  {min_temp_F}°F" + "\n" + "Condition: " + conditions + \
               "\n" + f"Chance Of Rain: {chanceOfRain}%" + "\n" + f"Humidity: {humidity}" + \
               "\n" + f"Sunrise: {sunrise} \t Sunset: {sunset}"
        all_datas.append(info)

    dayOne.config(text=all_datas[0])
    dayTwo.config(text=all_datas[1])
    dayThree.config(text=all_datas[2])


    #GUI WORK
if __name__ == "__main__":
    # entry box
    Entry_labelFrame = LabelFrame(mainWindow, text="Enter IP Address", font='helvetica 12', bg="white")
    Entry_labelFrame.grid(row=0, column=0, padx=5, pady=5)

    entry_label = Entry(Entry_labelFrame, justify="center", font=('poppins', 20))
    entry_label.grid(row=0)
    entry_label.focus()
    Button(Entry_labelFrame, text='Search', font=('poppins bold', 18), bg="light green", command=weather).grid(row=0, column=1, padx=10)

    # Current weather report frame
    labelFrame = LabelFrame(mainWindow, text="Current Weather", font=('helvetica', 12,'bold'), bg='white')
    labelFrame.grid(row=1, column=0, columnspan=20)

    location_view = Label(labelFrame, font=("Calibri bold", 20), bg="white")
    location_view.grid(row=0, column=0)

    large_view = Label(labelFrame, font=("Calibri bold", 38), bg="white")
    large_view.grid(row=3, column=0)

    small_view = Label(labelFrame, font=("Calibri bold", 15), bg="white")
    small_view.grid(row=4, column=0)

    # create 3 divided window frame
    labelFrame_two = LabelFrame(mainWindow, text="Next 3 Days Weather Report", font=('helvetica', 15,'bold'), bg='white')
    labelFrame_two.grid(row=2, column=0, padx=10, pady=10)
    # day 1
    dayOne = Label(labelFrame_two, relief='raised',height=10, width=35, font="helvetica 15")
    dayOne.grid(row=2, column=0)
    # day 2
    dayTwo = Label(labelFrame_two, relief='raised', height=10, width=35, font="helvetica 15")
    dayTwo.grid(row=2, column=1)
    # day 3
    dayThree = Label(labelFrame_two, relief='raised', height=10, width=35, font="helvetica 15")
    dayThree.grid(row=2, column=2)

    mainWindow.mainloop()
