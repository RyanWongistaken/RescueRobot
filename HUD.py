from PIL import Image, ImageDraw, ImageFont
import threading
import math
from sensor import *

class Drawthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.drawNew()
        print("starting thread")


def drawNew()
    while 1:
        sensoPlug = GetData()
        Overlay(sensoPlug[2], sensoPlug[1], sensoPlug[3], sensoPlug[0])


def Overlay(temperature, angle, oxygen_level , heading):
    hud = Image.new('RGBA', (640, 480), (255, 0, 0, 0))
    width, height = hud.size

    #Temperature
    tempString = str(temperature) + "C"
    tempDraw = ImageDraw.Draw(hud)
    font_forground = ImageFont.truetype("Assets\Cataclysmo.otf", 60)
    font_background = ImageFont.truetype("Assets\Cataclysmo.otf", 65)
    if temperature <= 10:
        tempDraw.text((width-58, height-50), tempString, font=font_background, fill=(68, 85, 90, 255))
    elif temperature >= 26 & temperature <= 35:
        tempDraw.text((width-58, height-50), tempString, font=font_background, fill=(92, 89, 24, 255))
    elif temperature > 35:
        tempDraw.text((width-58, height-50), tempString, font=font_background, fill=(92, 25, 4, 255))
    else:
        tempDraw.text((width-58, height-50), tempString, font=font_background, fill=(70, 68, 67, 255))
    tempDraw.text((width-58, height-50), tempString, font=font_forground, fill=(0, 0, 0, 255))


    #Tilt
    wisp_symbol = Image.open("Assets\wisp.png")
    horizon = Image.open("Assets\horizon.png")
    hud.paste(horizon.rotate(angle), (width-110, 10))
    hud.paste(wisp_symbol, (width-99, 22), wisp_symbol)

    #Oxygen
    if oxygen_level == 0:
        O2Level = Image.open("Assets\oxygenlvl1.png")
    elif oxygen_level == 1:
        O2Level = Image.open("Assets\oxygenlvl2.png")
    else:
        O2Level = Image.open("Assets\oxygenlvl3.png")
    hud.paste(O2Level, (width-55, height-110))  # x by y

    #Compasss
    compback = Image.open("Assets\compass.png")
    needle = Image.open("Assets\_needle.png")
    hud.paste(compback.rotate(heading, center=(50, 69)), (10, 0), compback.rotate(heading, center=(50, 69)))
    hud.paste(needle, (28, 25), needle)


    hud.save('hud.png', 'PNG')
    return


