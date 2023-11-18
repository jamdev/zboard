import machine, time, gc
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import network, urequests, ujson

# Inspired by...
# Credit: Pimoroni Demo Reel
# https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/galactic_unicorn/launch
# Credit: Jan-Willem Ruys, December 2022
# https://github.com/jruys/GalacticUnicornScroll/blob/main/txtscroll.py


from secrets import * 

# program
name = "zboard"
ver = "1.0a"
boardid = ""

# logging

def log(logmessage,logcategory="" ):
    global boardid
    print("LOG ("+boardid+") "+logcategory+": "+str(logmessage))

# get board id
def board_id():
    s = machine.unique_id()
    boardid = ""
    for b in s: boardid += hex(b)[2:]
    return boardid

boardid = board_id()
log("Starting","Board")


# overclock to 200Mhz
machine.freq(200000000)

# set up wifi
wifi_connected = False

indicator_enabled = True # puts a green dot in pixel 1 if wifi connected

# enable wifi
def connect_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    log("connecting...","Wifi")
    time.sleep(5)
    if wlan.isconnected():
        log(wlan.ifconfig()[0],"Wifi/IP")
        log(wlan.ifconfig()[1],"Wifi/Netmask")
        log(wlan.ifconfig()[2],"Wifi/Gateway")
        log(wlan.ifconfig()[3],"Wifi/DNS")
    
def disconnect_wifi():
    global wlan
    wlan.active(False)
    del wlan
    gc.collect()
    log("disconnected","Wifi")

def check_connection():
    if 'wlan' in globals():
        return wlan.isconnected()
    else: 
        return (0)


# load messages JSON
def load_json():
    global boardid
    try:
        response = None
        response = urequests.get(baseurl, headers={"Authorization":"Bearer "+authtoken,"ZboardID":boardid,"ZboardVer":ver})
        
    except Exception as e:
        log(e,"Request/Failed")
    else:
        if response.status_code == 200:
            try:
                data = ujson.loads(response.text)
                response.close()
            except ValueError as e:
                log(e,"JSON/Parseerror")
            else:
                response.close()
                response = None
                return data
        else:
            log(response.status_code,"HTTP/Errorstatuscode")
            response.close()
    return False

def get_payload():
    connect_wifi()
    payload = load_json()
    # todo - check payload has settings and messages
    # todo - check payload is for correct board ID
    if payload == False:
        import payload as default
        payload = default.payload
        log("Loaded","Payload/Defaults")
    disconnect_wifi()
    return payload

# Handle keypresses
# TODO something useful
def handle_keypresses():
    if galactic.is_pressed(GalacticUnicorn.SWITCH_A):
        indicator_enabled = True
    else:
        indicator_enabled = False

# Settings and messages

speed = 0
settings = messages = {}
foregroundpalette = backgroundpalette = []

def get_settings(payload):
    return payload["settings"]

def get_messages(payload):
    return payload["messages"]

def apply_settings(settings):
    global foregroundpalette, backgroundpalette, speed
    foregroundpalette = settings["foregroundpalette"]
    backgroundpalette = settings["backgroundpalette"]
    galactic.set_brightness(settings["brightness"])
    speed = settings["speed"]

# Draw the background
def draw_background(background_type, background_r, background_g, background_b, background_args):
    # Fake case statement
    def switch(background_type):
        # modules which take arguments
        if (background_type == "fire"):
            effect = __import__(background_type)
            effect.graphics = graphics
            effect.init()
            effect.draw(background_args)
            del effect
            return
        # modules which do not take arguments
        if (background_type == "rainbow" or background_type == "supercomputer"):
            effect = __import__(background_type)
            effect.graphics = graphics
            effect.init()
            effect.draw()
            del effect
            return
        # Default = plain background
        graphics.set_pen(graphics.create_pen(background_r, background_g, background_b))
        graphics.clear()
        return
    switch(background_type)

    # set the indicator led
    if indicator_enabled:
        if check_connection():
            graphics.set_pen(graphics.create_pen(0, 25, 0))
        graphics.pixel(0, 0)

# Clear background
def clear():
    draw_background(0,0,0,0,"")
    galactic.update(graphics)

# Side scrolling text function
# Scroll a single message
def text_scroll(text = "abc", foregroundcolour = 1, backgroundcolour = 6, speed = 0.1, loops = 3, backgroundtype = "plain", backgroundargs = "", shadow = False):
    foreground_r, foreground_g, foreground_b = foregroundpalette[foregroundcolour] 
    background_r, background_g, background_b = backgroundpalette[backgroundcolour] 
    width=graphics.measure_text(text,1,1)
    graphics.set_font("bitmap8")
    for loop_counter in range(loops):
        for position in range(53,-1*width,-1):
            handle_keypresses()
            draw_background(backgroundtype,background_r, background_g, background_b,backgroundargs)
            if shadow:
                graphics.set_pen(graphics.create_pen(0, 0, 0))
                graphics.text(text, position-1, 2, -1, 1)
                graphics.text(text, position+1, 2, -1, 1)
                graphics.text(text, position, 1, -1, 1)
                graphics.text(text, position, 3, -1, 1)
            graphics.set_pen(graphics.create_pen(foreground_r, foreground_g, foreground_b))
            graphics.text(text, position, 2, -1, 1)
            galactic.update(graphics)
            time.sleep(speed)



# Run main

# create galactic object and graphics surface for drawing
galactic = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

# Load payload

payload = get_payload()
messages = get_messages(payload)
apply_settings(get_settings(payload))
log(len(messages),"Messages/Count")
loops = messages["loops"] if ("loops" in messages and type(messages["loops"]) == int)  else 1
log(loops,"Messages/Loops")
# Loop
for i in range(loops):
    log(i,"Messages/Loopno")
    # loop through sorted messages
    for index, message in sorted(messages["messages"].items(), key=lambda item: item[0]):
        #Fake case statement
        def switch(message):
            # start scroll effect
            if message["effect"] == "scroll":
                text_scroll(text = message["text"],
                            speed = message["speed"],
                            backgroundcolour=message["backgroundcolour"],
                            foregroundcolour=message["foregroundcolour"],
                            loops=message["loops"],
                            backgroundtype=message["backgroundtype"],
                            backgroundargs=message["backgroundargs"],
                            shadow=message["shadow"])
                clear()
                return
        # default case
            return
        
        # sanitise
        text = message["text"]
        if type(text) != str and len(text) >= 256: 
            log("notvalid","Message/Text")
            text = "Invalid Message"

        if (type(   message["backgroundcolour"]) != int 
            or type(message["foregroundcolour"]) != int
            or type(message["loops"]) != int
            or type(message["speed"]) != float
            or type(message["backgroundtype"]) != str
            or type(message["shadow"]) != bool):
            log("notvalid","Message/Args")
            backgroundcolour=foregroundcolour=loops=backgroundtype=shadow=1

        # check all in range
        # TODO
                
        # run the message
        switch(message)
        
        # delay after individual message
        gc.collect()
        time.sleep(message["pause"]) if (type(message["pause"]) == float) else log("Typeerror","Delay")
    
    # delay after all messages
    time.sleep(messages["pause"]) if (type(messages["pause"]) == float) else log("Typeerror","Delay")
    
#needed to prevent memory errors
log("Resetting","Board")
machine.reset()   
    

