import pyaudio
import socket

#Configuração para gravação e transmissão de dados
FORMAT2 =’utf-8’
CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 4
RATE = 192000
audio = [ ]
frame1 = [ ]
frame = [ ]
CODE = ’utf-8’

#Mensagens de rotina para comunicação cliente-servidor
CHUNK_COMPLETE=’CHUNK_COMPLETE’
CHUNK_INCOMPLETE=’CHUNK_NOMPLETE’
READY=’READYFORYOULOV’
FILE_SENT=’FILE_SENT’

#Configuraçao da comunicação WIFI
socketCliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip= ’192.168.25.25’
port = 5050
backlog = 1
socketEndereço = (host_ip,port)
socketCliente.connect(socketEndereço)
print(’Conectado com:’,socketEndereço)
#Rotina de Gravação e Transmissão

try:
    while True:
          print("* recording")
          pyaudio_instance = pyaudio.PyAudio()
          stream = pyaudio_instance.open(format=FORMAT,channels = CHANNELS,rate = RATE,input = True,input_device_index = 2,frames_per_buffer = CHUNK)
          for i in range(0,1000):
              data = stream.read(CHUNK)
              frame.append(data)
          print("* done recording")
          stream.stop𝑠𝑡𝑟𝑒𝑎𝑚()
          stream.close()
          pyaudio_instance.terminate()
          print("* sending")
          for i in range(0,1000):
              datasend = frame[i]
              socketCliente.sendall(datasend)
              NEXT = True
              cond = socketCliente.recv(14).decode(FORMAT2)

              while NEXT:
                    if cond==CHUNK𝐼 𝑁 𝐶𝑂𝑀 𝑃 𝐿𝐸𝑇 𝐸 :
                       socketCliente.sendall(datasend)
                       cond = socketCliente.recv(14).decode(FORMAT2)
                    if cond==CHUNK_COMPLETE:
                       NEXT=False
                    if cond==READY:
                       NEXT=False
                    if cond!=CHUNK_INCOMPLETE and cond!=CHUNK_COMPLETE:
                       cond = socketCliente.recv(14).decode(FORMAT2)
              print("* done sending")
              frame = []
              print("* Iniciando proximo...")
              NEXT = True
              
#Rotina para aprovação do servidor para um novo ciclo de gravação
              while NEXT:
                    perm = socketCliente.recv(14).decode(FORMAT2)
                    if perm==READY:
                       data = 0
                       time.sleep(5)
                       NEXT=False
                    else:
                       perm = socketCliente.recv(14).decode(FORMAT2)
except KeyboardInterrupt:
print("Fechando")
