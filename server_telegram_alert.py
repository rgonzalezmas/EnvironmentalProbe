import Adafruit_DHT
import requests
import params
import socket
from w1thermsensor import W1ThermSensor

sensor_ds18b20 = W1ThermSensor()
sensor_dht11 = Adafruit_DHT.DHT11
hostname = socket.gethostname()

print ('Running ...')
    
humidity, temp = Adafruit_DHT.read_retry(sensor_dht11, params.pin)
temperature = sensor_ds18b20.get_temperature()

if temperature <= params.bad_low_temp or temperature >= params.bad_high_temp:
    requests.post('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text=Wrong temperature lecture from {2}: {3}ºC'.format(params.token, params.chat_id, hostname, temperature))
elif humidity <= params.bad_low_hum or humidity >= params.bad_high_hum:
    requests.post('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text=Wrong humidity lecture from {2}: {3}%'.format(params.token, params.chat_id, hostname, humidity))  
elif temperature >= params.max_temp:
    requests.post('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text=WARNING at {2}! Temperature too high: {3}ºC'.format(params.token, params.chat_id, hostname, temperature))
elif humidity >= params.max_hum:
    requests.post('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text=WARNING at {2}! Humidity too high: {3}%'.format(params.token, params.chat_id, hostname, humidity))
  

