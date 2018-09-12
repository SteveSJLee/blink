from flask import Flask, render_template, redirect, url_for
from gpiozero import PWMLED
import threading
import random
import signal
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
    print('hello world')
    '''
    t = threading.Thread(target=_blink_fancy, daemon=True)
    t.start()
    '''

@app.route("/")
def index():
   return render_template('index.html')

# RGB user inputs
@app.route('/red/', methods=['POST'])
def toggleRed():
    _toggle(led_R)
    return ('', 204)

@app.route('/green/', methods=['POST'])
def toggleGreen():
    _toggle(led_G)
    return ('', 204)

@app.route('/blue/', methods=['POST'])
def toggleBlue():
    _toggle(led_B)
    return ('', 204)

def _toggle(led):
    global flag
    flag = 0
    for l in leds:
        l.off()

    if led.value == 0:
        led.value = 1
    # if idle, blink fancy
    #threading.Timer(60.0, _set_flag)

def _set_flag():
    global flag
    flag = 1

def _blink_fancy():
    global flag
    while True:
        if flag == 1:
            num = random.randrange(3)
            led = leds[num]
            led.pulse()
            time.sleep(random.random()*1.5)
            led.off()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
