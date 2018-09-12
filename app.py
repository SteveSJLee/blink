from flask import Flask, render_template
from gpiozero import PWMLED
import threading
import random
import signal

app = Flask(__name__)

r,g,b = 16, 21, 20
led_R = PWMLED(r)
led_G = PWMLED(g)
led_B = PWMLED(b)
leds = [led_R, led_G, led_B]

flag = 1

@app.route("/")
def index():
   return render_template('index.html')

# RGB user inputs
@app.route('/red')
def toggleRed():
    _toggle(led_R)
    return 'r'

@app.route('/green')
def toggleGreen():
    _toggle(led_G)
    return 'g'

@app.route('/blue')
def toggleBlue():
    _toggle(led_B)
    return 'b'

def _toggle(led):
    flag = 0
    for l in leds:
        l.off()

    if led.value == 0:
        led.on()
    # if idle, blink fancy
    threading.Timer(60.0, _set_flag)

def _set_flag():
    flag = 1

def _blink_fancy():
    while flag == 1:
        num = random.randrange(3)
        led = leds[num]
        led.pulse()
        time.sleep(random.random())
        led.off()

if __name__ == "__main__":
    t = threading.Thread(target=_blink_fancy, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=8080, debug=True)
