from cmath import log10
import time
import numpy as np
import suaBibSignal
import matplotlib.pyplot as plt
from suaBibSignal import *
import peakutils
import numpy as np
import sounddevice as sd
from scipy.signal import butter 

freq = {1:(1209,679), 2:(1336,679), 3:(1477,679), 4:(1209,770), 5:(1336,770), 6:(1477,770), 7:(1209,852), 8:(1336,852), 9:(1477,852), 0:(1336,941)}

def getFreq(num):
    return freq[num]
# Coeficientes do filtro
NUM = 2
freq = getFreq(NUM)
tone = []
duration = 8
time.sleep(5)
tempo = np.linspace(0, duration, duration*44100,endpoint=False)
tone1 = np.sin(2*np.pi*freq[0]*tempo)
tone2 = np.sin(2*np.pi*freq[1]*tempo)
tone = tone1 + tone2

a = 0.0002532
b = 0.0002494
c = 1   
d = -1.955
e = 0.9557

def filter_signal(x):
    # x: array do sinal de entrada
    # y: array do sinal de saída, inicializado com zeros do mesmo tamanho que x
    
    y = [x[0], x[1]]

    # Aplicando a equação de diferenças para cada ponto no tempo
    for n in range(2, len(x)):
        y.append(-d * y[n-1] - e * y[n-2] + a * x[n-1] + b * x[n-2])

    return y


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #instruções*******************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
    fs = 44100
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels =  1 
    duration =  5 
    numAmostras = fs*duration
    print(f'A gravação vai começar em 3 segundos')
    time.sleep(2)
    print("Gravação iniciada")
    #para gravar, utilize
    audio = sd.rec(int(numAmostras), samplerate=fs, channels=1)
    sd.wait()
    print("...     FIM")
        
    # Exemplo de uso
    fs = 44100  # taxa de amostragem
    t = np.linspace(0, 1, fs)  # tempo de 1 segundo

    # Filtragem do sinal
    y = filter_signal(tone)
    signal.plotFFT(audio[:,0], 44100)
    # x_grafico, y_grafico = signal.calcFFT(tone, fs)
    # plt.subplot(2,1,1)
    # plt.plot(x_grafico, np.abs(y_grafico))
    # plt.title('Fourier do sinal original')
    # plt.xlim(0, 5000)

    # x_grafico, y_grafico = signal.calcFFT(y, fs)    
    # plt.subplot(2,1,2)
    # plt.plot(x_grafico, np.abs(y_grafico))
    # plt.title('Fourier do sinal filtrado')
    # plt.xlim(0, 5000)
    # plt.show()

if __name__ == "__main__":
    main()