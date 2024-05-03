import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Parâmetros do filtro
order = 6
fs = 44100       # taxa de amostragem, Hz
cutoff = 3000    # frequência de corte desejada da filtragem passa-baixa, Hz

# Geração de dados de teste (sinal simulado)
T = 5.0          # segundos
n = int(T * fs)  # total de amostras
t = np.linspace(0, T, n, endpoint=False)
# Sinal de teste: soma de duas frequências
data = np.sin(1.2 * 2 * np.pi * t) + 1.5 * np.cos(9 * 2 * np.pi * t)

# Filtragem
y = butter_lowpass_filter(data, cutoff, fs, order)

# Plotagem dos resultados
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, data - y, 'r-', label='residual')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()
