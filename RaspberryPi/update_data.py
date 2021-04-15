import paramiko
from datetime import datetime

date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

def dummy_get_from_can():
    temperature=30
    humidity=25
    pressure=1005
    illuminance=1200
    return { 'temperature': str(temperature),\
             'humidity': str(humidity),\
             'pressure': str(pressure),\
             'illuminance': str(illuminance) }

def save_to_text_file(values):
    with open('data.txt', 'w') as file:
        file.write(date+'\n')
        file.write('Temperature: ' + values['temperature'] + '\n')
        file.write('Humidity: ' + values['humidity'] + '\n')
        file.write('Pressure: ' + values['pressure'] + '\n')
        file.write('Illuminance: ' + values['illuminance'])

def save_to_html_file(values):
    with open('index.html', 'w') as file:
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
    sensor_values = dummy_get_from_can()
    save_to_text_file(sensor_values)
    save_to_html_file(sensor_values)
    send_html_file('./index.html')
