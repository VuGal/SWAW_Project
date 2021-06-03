import os
import can
import paramiko
from datetime import datetime


os.system('sudo ip link set can0 type can bitrate 250000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')

date = str()


def log(message):
    with open('/home/pi/SWAW_Project/log.txt', 'a') as file:
        file.write(message+'\n')

def update_date():
    global date
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def parse_can_frame(message):
    data = message.split()
    temperature = int(data[8]+data[7], 16)
    humidity = int(data[10]+data[9], 16)
    pressure = int(data[12]+data[11], 16)
    illuminance = int(data[14]+data[13], 16)
    return { 'temperature': str(temperature),\
             'humidity': str(humidity),\
             'pressure': str(pressure),\
             'illuminance': str(illuminance) }

def fetch_data_from_can_bus():
    msg = can0.recv(2400.00)
    if msg is not None:
        update_date()
        log(f'[{date}] Received some data!')
        data = parse_can_frame(str(msg))
        log(f'[{date}] Temperature: ' + data['temperature'] + ' °C')
        log(f'[{date}] Humidity: ' + data['humidity'] + ' %')
        log(f'[{date}] Pressure: ' + data['pressure'] + ' hPa')
        log(f'[{date}] Illuminance: ' + data['illuminance'] + ' Lx')
        ack_msg = can.Message(arbitration_id=0x123, data=[6, 5, 6, 7, 7, 6, 0, 0], extended_id=False)
        can0.send(ack_msg)
    else:
        log('Timeout occurred, no message received!')
    return data

def save_to_text_file(values):
    with open('/home/pi/SWAW_Project/data.txt', 'w') as file:
        file.write(date+'\n')
        file.write('Temperature: ' + values['temperature'] + '\n')
        file.write('Humidity: ' + values['humidity'] + '\n')
        file.write('Pressure: ' + values['pressure'] + '\n')
        file.write('Illuminance: ' + values['illuminance'] + '\n')

def save_to_html_file(values):
    with open('/home/pi/SWAW_Project/index.html', 'w') as file:
        file.write('<div id="Date">' + date + '</div>\n')
        file.write('<div id="Temperature">' + values['temperature'] + '</div>\n')
        file.write('<div id="Humidity">' + values['humidity'] + '</div>\n')
        file.write('<div id="Pressure">' + values['pressure'] + '</div>\n')
        file.write('<div id="Illuminance">' + values['illuminance'] + '</div>')

def send_html_file(file_path):
    ssh = paramiko.SSHClient()
    ssh.load_host_keys('/home/pi/.ssh/known_hosts')
    ssh.connect('23.102.182.59', username='swawproject')
    sftp = ssh.open_sftp()
    sftp.put(file_path, '/var/www/html/index.html')
    sftp.close()
    ssh.close()

if __name__ == '__main__':
    while True:
        update_date()
        log(f'[{date}] Waiting for new sensor values...\n')
        try:
            sensor_values = fetch_data_from_can_bus()
            log(f'[{date}] Fetching sensor values - SUCCESS!')
        except:
            log(f'[{date}] Fetching sensor values - ERROR!')
            continue
        log(f'[{date}] Saving sensor values to text file...')
        try:
            save_to_text_file(sensor_values)
            log(f'[{date}] Saving to text file - SUCCESS!')
        except:
            log(f'[{date}] Saving to text file - ERROR!')
        log(f'[{date}] Saving sensor values to HTML file...')
        try:
            save_to_html_file(sensor_values)
            log(f'[{date}] Saving to HTML file - SUCCESS!')
        except:
            log(f'[{date}] Saving to HTML file - ERROR!')
            continue
        log(f'[{date}] Sending HTML file to the remote server...')
        try:
            send_html_file('/home/pi/SWAW_Project/index.html')
            log(f'[{date}] Sending HTML file to remote server - SUCCESS!')
        except:
            log(f'[{date}] Sending HTML file to remote server - ERROR!')
