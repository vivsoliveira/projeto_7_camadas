from cmath import log10
import time
import numpy as np
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
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
    fs = 44100  # taxa de amostragem

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
    print("...FIM")
        
    # Exemplo de uso
    import scipy.signal

    fs = 44100  # taxa de amostragem

    # Filtragem do sinal
    y = filter_signal(audio[:,0])

    nyq = 0.5 * fs

    # Butterworth low-pass filter with frequency cutoff at 2.5 Hz
    b, a = scipy.signal.iirfilter(4, Wn=159, fs=fs, btype="low", ftype="butter")
    # apply filter once
    yfilt = scipy.signal.lfilter(b, a, audio[:,0])

    signal.plotFFT(audio[:,0], fs)
    signal.plotFFT(y, fs)
    signal.plotFFT(yfilt, fs)
    plt.show()


if __name__ == "__main__":
    main()