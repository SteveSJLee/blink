from flask import Flask, render_template, abort, request
from gpiozero import PWMLED
import threading
import random
import time

app = Flask(__name__)

r,g,b = 16, 21, 20
led_R = PWMLED(r)
led_G = PWMLED(g)
led_B = PWMLED(b)
leds = [led_R, led_G, led_B]

flag = 1

@app.before_first_request
def onStart():
    t = threading.Thread(target=_blink_fancy, daemon=True)
    t.start()

@app.route("/")
def index():
   return render_template('index.html')

# RGB user inputs
@app.route('/command', methods=['POST'])
def process_command():
    valid_commands = ['red', 'green', 'blue', 'off']
    data = json.loads(request.data.decode('utf8'))
    command = data.get('command')

    # Abort if POST request is invalid.
    if command is None or command not in valid_commands:
        abort(400)
    else:
        _toggle(command)
        return "done"

def _toggle(cmd):
    flag = 0
    for l in leds:
        l.off()

    if cmd == 'off':
        break
    elif cmd == 'red':
        led = led_R
    elif cmd == 'green':
        led = led_G
    elif cmd == 'blue':
        led ==led_B
    else:
        abort(500)

    if led.value == 0:
        led.on()

def _count_idle():
    counter = 0
    while True:
        if flag == 0:
            counter += 1
        if counter > 5000000:
            flag = 1
            counter = 0

def _blink_fancy():
    while flag == 1:
        num = random.randrange(3)
        led = leds[num]
        led.pulse()
        time.sleep(random.random()*1.5)
        led.off()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
