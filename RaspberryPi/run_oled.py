import time

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1331
import os

serial = spi(device=0, port=1)
device = ssd1331(serial)

def parser():
    read_txt = []
    with open('/home/pi/SWAW_Project/data.txt', 'r') as reader:
        read_txt = reader.readlines()
    print(read_txt)
    read_txt_parsed = []
    for x in range(len(read_txt)):
        if(x == 0):
            continue
        read_txt_parsed.append(read_txt[x].split(' '))
    read_txt_parsed[0][0] = 'T:'
    read_txt_parsed[1][0] = 'H:'
    read_txt_parsed[2][0] = 'P:'
    read_txt_parsed[3][0] = 'I:'
    returned = read_txt_parsed[0][0] + ' ' + read_txt_parsed[0][1][:-1] + ' ' + u'\N{DEGREE SIGN}' + 'C\n' + read_txt_parsed[1][0] + ' ' + read_txt_parsed[1][1][:-1] \
    + ' %\n' + read_txt_parsed[2][0] + ' ' + read_txt_parsed[2][1][:-1] + ' hPa\n' +  read_txt_parsed[3][0] + ' ' + read_txt_parsed[3][1][:-1] + ' Lx'
    print(returned)
    print(read_txt_parsed)
    return returned

def lcd_draw(to_draw):
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="red", fill="black")
        draw.text((5, 3), to_draw, fill="green")

if __name__ == "__main__":
    while(1):
        to_draw = parser()
        lcd_draw(to_draw)
        time.sleep(1)
