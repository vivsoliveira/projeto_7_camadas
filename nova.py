import numpy as np
from scipy.integrate import odeint
from scipy.fftpack import fft, fftfreq
import matplotlib.pyplot as plt
import sounddevice as sd
import time

# Função para o filtro
def filtro_sistema(y, t, u, params):
    a0, a1, a2, b0, b1, b2 = params
    dydt = [y[1], -a2*y[1] - a1*y[0] + b2*u[int(t)-2] + b1*u[int(t)-1] + b0*u[int(t)]]
    return dydt

# Parâmetros do filtro (exemplo genérico, ajuste conforme necessário)
params = [1.0, 0.5, 0.25, 0.1, 0.15, 0.05]  # Coeficientes do filtro

# Definindo parâmetros de gravação
fs = 44100  # Taxa de amostragem
duration = 5  # Duração da gravação em segundos

# Gravação do áudio
print("Gravação começará em 3 segundos.")
time.sleep(3)
print("Gravando...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
sd.wait()  # Aguarda fim da gravação
print("Gravação finalizada.")
audio = audio.ravel()  # Converte o áudio para um array 1D

# Índices das amostras (substituindo o conceito de 'tempo')
indices = np.arange(len(audio))

# Condições iniciais e simulação
y0 = [0, 0]  # Estado inicial (y e dy/dt)
sol = odeint(filtro_sistema, y0, indices, args=(audio, params))

# Saída do filtro
output = sol[:, 0]

# FFT do áudio original e do áudio filtrado
fft_original = fft(audio)
fft_filtrado = fft(output)
frequencias = fftfreq(len(audio), d=1/fs)

plt.figure(figsize=(12, 8))

# Áudio original e filtrado
plt.subplot(2, 1, 1)
plt.plot(indices/fs, audio, label='Original')
plt.plot(indices/fs, output, label='Filtrado')
plt.title('Áudio Original e Filtrado')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.legend()

# FFT de áudio original e filtrado
plt.subplot(2, 1, 2)
plt.plot(frequencias, np.abs(fft_original), label='FFT Original')
plt.plot(frequencias, np.abs(fft_filtrado), label='FFT Filtrado')
plt.title('FFT do Áudio Original e Filtrado')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.show()
