#port del servidor TCP
#el port ha de coincidir amb l'introduït al checkmk
port_num = 1082

#ruta a la carpeta on es guarden els logs diaris
route_logfile = "/home/andrew/Project/logs/"

#pin al que va connectat el sensor DHT11
pin = 18

#token del bot de telegram
token = '5612389620:AAFj0mZmssG5q1wxnvqu0fPd8dSuqeavsF4'

#id del grup telegram
chat_id = '-796955238'
#chat_id = '5585066219'

#temperature thresholds
max_temp = 30.0
bad_low_temp = 10.0
bad_high_temp = 90.0

#humidity thresholds
max_hum = 50
bad_low_hum = 10
bad_high_hum = 90
