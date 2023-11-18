from time import sleep

from module.utils.serial_manager import SerialManager

serial = SerialManager('com254', 115200)
send_data = ""
for i in range(1000):
    send_data += "test"
while True:
    serial.send(send_data)
    sleep(1)
