import webbrowser, time, PIL, cv2
import pyautogui as pg
import keyboard as kb
from datetime import datetime, timedelta

classes = ["dellison", "cmcrae", "dtaylor", "wstaffieri", "scaddell", "lmoreland"]
times = ["8:44am", "9:39am", "11:04am", "12:49pm", "1:44pm", "2:39pm"]

def open_link_in_chrome(link):
    webbrowser.register('chrome',
        None,
        webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(link)

def time_until_class(next_time):
    next_time_spl = [int(x) for x in next_time.split(":")]
    now = datetime.now()
    return (datetime(hour=next_time_spl[0], minute=next_time_spl[1], year=now.year, month=now.month, day=(now.day if next_time_spl[0] >= now.hour else (now + timedelta(days=1)).day)) - now).total_seconds()

if __name__ == "__main__":
    for i in range(len(times)):
        if times[i].split(":")[0] == "12":
            times[i] = times[i][:-2]
        elif times[i][-2:] == "am":
            times[i] = times[i][:-2]
        elif times[i][-2:] == "pm":
            spl = times[i].split(":")
            spl[0] = str(int(spl[0])+12)
            spl[1] = spl[1][:-2]
            times[i] = ":".join(spl)
    c = 0
    for counter in range(len(classes)):
        if datetime.now().hour < int(times[counter].split(":")[0]):
            c = counter
            break
        elif datetime.now().hour == int(times[counter].split(":")[0]):
            if datetime.now().minute < int(times[counter].split(":")[1]):
                c = counter
                break
    counter = c
    while True:
        waiting_time = time_until_class(times[counter % len(times)])
        print(f"Waiting for {waiting_time}")
        time.sleep(waiting_time)
        print(f"Logging onto {classes[counter]} because it is {times[counter]}!")
        open_link_in_chrome("https://meet.google.com/landing?authuser=1")
        time.sleep(6)
        while pg.locateCenterOnScreen("in_meet_sign.jpg", confidence=.7) is None:
            pg.keyDown("ctrl")
            pg.keyDown("r")
            time.sleep(0.5)
            pg.keyUp("r")
            pg.keyUp("ctrl")
            input_meet_name_box_position = pg.locateCenterOnScreen("input_box_picture.jpg", confidence=.7)
            print(f"Clicking at {input_meet_name_box_position}")
            pg.click(input_meet_name_box_position)
            pg.typewrite(classes[counter], 0.1)
            pg.press("enter")
            time.sleep(5)
        counter += 1

