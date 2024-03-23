
# Default settings
settings = {
    "foregroundpalette": [[0,0,0],[255,255,255],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255]],
    "backgroundpalette": [[0,0,0],[0,32,0],[0,0,32],[32,32,0],[32,0,32],[0,32,32],[32,32,32],[32,0,0]],
    "brightness": 0.5,
    "speed": 0.1
    }

# messages
messages = {
    "boardid": "",
    "messages": {
        "0":{
            "text": "Globegetter?", #must be a str
            "effect": "scroll", #must be a str
            "speed": 0.1, # must be a float
            "loops": 1, # must be an int
            "foregroundcolour": 1, #must be an int
            "backgroundcolour": 0, #must be an int
            "backgroundtype": "fire", #must be an str
            "backgroundargs": "green", #not validated; up to function to check
            "shadow": False, #must be a bool
            "pause": 0.0, #seconds, must be a float
        },
        "1":{
            "text": "Help us test", #must be a str
            "effect": "scroll", #must be a str
            "speed": 0.1, # must be a float
            "loops": 1, # must be an int
            "foregroundcolour": 1, #must be an int
            "backgroundcolour": 0, #must be an int
            "backgroundtype": "supercomputer", #must be an str
            "backgroundargs": "", #not validated; up to function to check
            "shadow": True, #must be a bool
            "pause": 0.0, #seconds, must be a float
        },
        "2":{
            "text": "Scan our QR code", #must be a str
            "effect": "scroll", #must be a str
            "speed": 0.1, # must be a float
            "loops": 1, # must be an int
            "foregroundcolour": 3, #must be an int
            "backgroundcolour": 0, #must be an int
            "backgroundtype": "rainbow", #must be an str
            "backgroundargs": "", #not validated; up to function to check
            "shadow": True, #must be a bool
            "pause": 0.0, #seconds, must be a float
        },
    },
    "pause": 5.0, #seconds, must be a float
    "loops": 30 #number of loops before restarting board
}

payload = {
    "settings": settings,
    "messages": messages
}