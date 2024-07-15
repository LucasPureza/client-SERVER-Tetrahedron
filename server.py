import socket
import numpy as np
from datetime import datetime
import time
import soundfile as sf

# create socket
Servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
frame = []
RATE = 192000
FORMAT = 'utf-8'
CHUNK_INCOMPLETE= 'CHUNK_NOMPLETE'
CHUNK_COMPLETE= 'CHUNK_COMPLETE'
READY= 'READYFORYOULOV'

Servidor.bind((socket.gethostbyname(socket.gethostname()),5050))
Servidor.listen()
print('Aguardando conexão')

conn, ender = Servidor.accept()
print('Conectado')

try:
  while True:
      
      print('Recebendo arquivo')

      for i in range(0,1000):
          data = conn.recv(2048)
          print(len(data))
          CONTROL1 = True
          while CONTROL1:
              if len(data)<2048:
                 conn.sendall(CHUNK_INCOMPLETE.encode(FORMAT))
              else:
                 conn.sendall(CHUNK_COMPLETE.encode(FORMAT))
                 frame.append(data)
                 CONTROL1=False
              if not data:
                 conn.sendall(READY.encode(FORMAT))
                 time.sleep(10)
                 
      print('Arquivo recebido')
      
      print('Processando arquivo')
      current_datetime = str(datetime.now())
      date = str([current_datetime[11:13],current_datetime[14:16],current_datetime[17:19]])
      newdata = b''.join(frame)
      data_array = np.frombuffer(newdata,dtype='int16')
      
      dataLF = data_array[1::4]
      dataRF = data_array[0::4]
      dataLB = data_array[2::4]
      dataRB = data_array[3::4]   
      
      W= dataLF + dataRF + dataLB + dataRB
      X= dataLF + dataRF - dataLB - dataRB
      Y= dataLF - dataRF + dataLB - dataRB
      Z= dataLF - dataRF - dataLB + dataRB

      FinalData = np.hstack((W,X,Y,Z))
      print('Arquivo processado')
      
      print('Salvando Arquivo')
      sf.write(date+"_.flac", FinalData, 44000)
      print('Arquivo Salvo')
      
      frame = []
      conn.sendall(READY.encode(FORMAT))
      time.sleep(10)

except KeyboardInterrupt:
    print('interrompido!')
    
    
