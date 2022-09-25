import time
import socket
import datetime
import board
from datetime import date
import Adafruit_DHT
import params
from w1thermsensor import W1ThermSensor
import subprocess

time.sleep(30)

#Avoid Broken Pipe Error
from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL)
 
# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Bind the socket to server address and port 1081
server_address = ('', params.port_num)
tcp_socket.bind(server_address)
 
# Listen on port 1081
tcp_socket.listen(1)

print("Listening...")

#Lectura del sensor
sensor_ds18b20 = W1ThermSensor()
sensor_dht11 = Adafruit_DHT.DHT11

def write_temp(temperature):
    with open(params.route_logfile+file_name,"a") as log:
         log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),("Temperature, {},ºC".format(temperature))))
         
def write_hum(humidity):
    with open(params.route_logfile+file_name,"a") as log:
         log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),("Humidity, {},%".format(humidity))))
 
while True:
    print("Waiting for connection")
    connection, client = tcp_socket.accept()
    try:
        humidity, temp = Adafruit_DHT.read_retry(sensor_dht11, params.pin)
        temperature = sensor_ds18b20.get_temperature()
        print("Connected to client IP: {}".format(client)) 
        data = connection.recv(4*1024)
        dat = data.decode()
        dat = dat.strip()
        print("Received data: {}".format(dat))
        
        if dat == ('humidity'):
            current_date = date.today()
            str_current_date = str(current_date)
            file_name = str_current_date+".csv"
            reply = str(humidity)
            print("Humidity lecture: {}".format(reply))
            connection.send(reply.encode())
            connection.close()
            write_hum(humidity)
        
        elif dat == ('temperature'):
            current_date = date.today()
            str_current_date = str(current_date)
            file_name = str_current_date+".csv"
            reply = str(temperature)
            print("Temperature lecture: {}".format(reply))
            connection.send(reply.encode())
            connection.close()
            write_temp(temperature)
        
        elif dat == ('sai'):
            command_status = "upsc sai_celler@localhost ups.status"
            ret_status = subprocess.run(command_status, capture_output=True, shell=True)
            estat = ret_status.stdout.decode()
            reply = str(estat)
            print("UPS status: {}".format(reply))
            connection.send(reply.encode())
            connection.close()
        
        else:
            print("Wrong lecture")
            reply = ("Comanda incorrecta")
            connection.send(reply.encode())
            connection.close()

    finally:
         connection.close()
