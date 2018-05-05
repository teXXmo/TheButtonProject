# firmware installation process

* Requirements:
  * Python 2.7 ( [windows] (https://www.python.org/downloads/windows/ ) )
  * esptool (pip install esptool )

* Optional:
  * ampy (pip install adafruit-ampy)
  * Azure iot service client (pip install azure-iothub-service-client)

esptool.py --port \<serial-port\> erase_flash

esptool.py --port \<serial-port\> --baud 115200 write_flash -fm dout -fs 1MB 0x00000 <Firmware>

(these settings were tested on ESP8285)

