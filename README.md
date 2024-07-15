# Software de Gravação de áudio em Formato A e Processamento para Converter áudio para Formato B

O código "GravacaoCliente" faz a gravação dos 4 canais de um arranjo tetraédrico abaixo com uma taxa de amostragem de 192kHz. A sua estrutura tem os microfones arranjados de forma que cada um fique posicionado a 45 graus relativo aos eixos cartesianos. Tais microfones são comumente rotulados como LF (Left-Forward - verde), RF (Right-Forward - azul), LB (Left-Backward - laranja) e RB (Right-Forward - lilás).

<p align="center"> <img src="https://github.com/RT-DSP/AI_SE_DA_Audio/assets/42192356/b403acd1-3b4c-488e-bcf6-2b5535db3ab5" width=50% height=50%></p>

# Configuração para gravação e transmissão de dados
O código começa com a configuração dos parâmetros que compõem a captura:
CHUNK -> Tamanho do buffer de amostras de áudio por comando de gravação
FORMAT -> Tipo de conversão digital utilizada, no código original é usado 16 bits de números inteiros  para a amostragem.
CHANNELS -> Número de canais para a gravação simultanea.
RATE -> Taxa de amostragem da gravação.
FORMAT2 ou CODE -> Tipo de codificação utilizada para as mensagens e comandos de rotina da transmissão WIFI

As mensagens de rotina "CHUNK COMPLETE", "CHUNK INCOMPLETE", "READY" e "FILE SENT" são mensagens que codificadas tem o mesmo tamanho em bytes e servem para guiar a transmissão de dados, caso algum pacote se perca na transmissão ou quando o sistema está pronto para mais aquisições.

Para a comunicação WIFI, é necessário que seja declarado em GravacaoCliente.py o Ipv4 do terminal de Processamento na variavel "host_ip".

Setado os parametros do cliente, o loop começa com a aquisição das amostras dos 4 canais, aonde o primeiro FOR indica quantas amostras irão ser computadas. No codigo original está 1000 repetições, totalizando 4*256000 amostras. Cada loop, as amostras são concatenadas em um vetor "frame" para salvar o sinal gravado.

as gravações de áudio serão feitas para 4 canais com codificação de 16~bits para cada amostra de áudio coletada de cada canal, logo serão 4*16 ou 8 bytes por quadro de áudio, em uma taxa de amostragem de 192000 Hz. 

Após a aquisição, a transmissão começa aonde é mandando 2048 bytes por vez via WIFI para o terminal do servidor para o processamento de áudio.

O cliente então recebe uma mensagem informando se o pacote chegou completo ou não: caso receba "CHUNK INCOMPLETE", ele irá remandar o pacote; caso receba "CHUNK COMPLETE", ele continua para mandar os próximos 2048 bytes.

Depois o cliente espera receber o sinal do servidor pela mensagem "READY" para repetir o loop de gravação.

# Processamento Digital de Sinal e Salvando Arquivos

O sinal é captado pelos microfones em A-formato (LF, RF, LB e RB) e deve ser convertido em B-formato (W, X, Y e Z) tal que

$$
\begin{equation}
W = s_{LF} + s_{RF} + s_{LB} + s_{RB}
\end{equation}
$$

$$
\begin{equation}
X = s_{LF} + s_{RF} - s_{LB} - s_{RB}
\end{equation}
$$

$$
\begin{equation}
Y = s_{LF} - s_{RF} + s_{LB} - s_{RB}
\end{equation}
$$

$$
\begin{equation}
Z = s_{LF} - s_{RF} - s_{LB} + s_{RB}
\end{equation}
$$

O codigo "ProcessamentoServidor.py" começa com a configuração WIFI, fazendo uma transmissão TCP, onde primeiro ele abre um canal de "escuta", até que o cliente acesse sua rede. OBSERVAÇÃO: O código do Servidor precisa ser aberto primeiro, e depois o cliente conecta com o servidor.

Os equalizadores Eq1, Eq2, Eq3 e Eq4 são carregados para convoluir os sinais a serem processados para que a calibração garanta coincidencia dos sinais.

Com o comando "try", começa o loop infinito: o primeiro "while" é para o recebimento do áudio completo gravado pelo Cliente. É recebido 2048 bytes por vez.
Depois de recebido o sinal, é recolhido a data de aquisição e salvo no nome do arquivo.

Para o processamento, o arquivo em bytes e convertido para um vetor numpy, cada canal é separado, equalizado e depois convertido para formato B, e depois cada canal de formato B resultante é concatenado e gravado em formato FLAC e salvo no HD do terminal.

O algoritmo então manda uma mensagem para o cliente indicando que está pronto para uma nova aquisição, depois da confirmação do cliente, começa um novo ciclo.
___


import socket
import numpy as np
from scipy.io import loadmat
from scipy import signal
from datetime import datetime
import time
import soundfile as sf
## Bibliotecas necessárias

* numpy
* socket
* scipy.io import loadmat
* scipy import signal
* time
* soundfile
* pyaudio
