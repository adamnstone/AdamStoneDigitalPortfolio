from gpiozero import Button, LED
import time, flask, requests
from flask import request
from signal import pause

app = flask.Flask(__name__)

on_input = 26
on_output = 16
input_button = Button(on_input)
output = LED(on_output)
machine_name = "Test Washing Machine 1"
string_code = "XXXXXXXXXXXX"


def turn_on_machine(duration):
    output.on()
    time.sleep(duration)
    output.off()
    client_secret = requests.get("http://34.67.212.21/api/v1/register?code=0xfbce434ee3").json()['client_secret']
    requests.get(f"http://34.67.212.21/api/v1/sendmessage?client_secret={client_secret}&value=1&key={machine_name}&fromapp=true")

def input_func():
    client_secret = requests.get("http://34.67.212.21/api/v1/register?code=0xfbce434ee3").json()['client_secret']
    requests.get(f"http://34.67.212.21/api/v1/sendmessage?client_secret={client_secret}&value=1&key={machine_name}&fromapp=false")

@app.route("/", methods=["GET"])
def home():
    if 'duration' in request.args and 'code' in request.args:
        if request.args['code'] != string_code:
            return "Error: Incorrect code"
        turn_on_machine(int(request.args['duration']))
        return "Success!"
    else:
        return "Error: 'duration' and/or 'code' parameter not provided"

if __name__ == "__main__":
    input_button.when_pressed = input_func
    app.run(host="0.0.0.0", port=80)

    pause()
