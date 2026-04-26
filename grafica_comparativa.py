#!/usr/bin/env python3
# Grafics Comparatius VAD

import matplotlib
matplotlib.use('Agg')

import numpy as np
import struct
import matplotlib.pyplot as plt

fs = 16000
wav_file = 'PAV_2121.wav'
manual_file = 'PAV_2121.lab'
auto_file = 'PAV_2121.vad'
wav_canceled = 'PAV_2121_cancelat.wav'
auto_10db = 'PAV_2121_10db.vad'
auto_7db = 'PAV_2121.vad'

# ===== GRAFIC 1: Audio Original vs Cancelat =====
with open(wav_file, 'rb') as f:
    f.read(44)
    data = f.read()
samples = np.array(struct.unpack('<' + 'h' * (len(data)//2), data), dtype=np.float32)

with open(wav_canceled, 'rb') as f:
    f.read(44)
    data = f.read()
samples_canceled = np.array(struct.unpack('<' + 'h' * (len(data)//2), data), dtype=np.float32)

N = min(len(samples), len(samples_canceled))
time = np.arange(N) / fs
samples = samples[:N] / 32768.0
samples_canceled = samples_canceled[:N] / 32768.0

fig1, axes1 = plt.subplots(3, 1, figsize=(14, 9), sharex=True)
ymax = max(abs(samples.min()), abs(samples.max()), abs(samples_canceled.min()), abs(samples_canceled.max()))

axes1[0].plot(time, samples, 'b')
axes1[0].set_title('Senyal Original')
axes1[0].set_ylabel('Amplitud')
axes1[0].set_ylim(-ymax, ymax)
axes1[0].grid(True)

axes1[1].plot(time, samples_canceled, 'r')
axes1[1].set_title('Soroll Cancelat')
axes1[1].set_ylabel('Amplitud')
axes1[1].set_ylim(-ymax, ymax)
axes1[1].grid(True)

axes1[2].plot(time, samples, 'b', alpha=0.8, linewidth=1, label='Original')
axes1[2].plot(time, samples_canceled, 'r', alpha=0.8, linewidth=1, label='Cancelat')
axes1[2].set_title('Comparacio')
axes1[2].set_xlabel('Temps (s)')
axes1[2].set_ylabel('Amplitud')
axes1[2].set_ylim(-ymax, ymax)
axes1[2].legend(loc='upper right')
axes1[2].grid(True)

plt.tight_layout()
plt.savefig('img/audio_comparativa.png', dpi=150)
print('Grafic 1: img/audio_comparativa.png')

# ===== GRAFIC 2: Labels Manual vs Automatic =====
manual = []
with open(manual_file) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            manual.append((float(parts[0]), float(parts[1]), parts[2]))

auto = []
with open(auto_file) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            auto.append((float(parts[0]), float(parts[1]), parts[2]))

def plot_labels(ax, labels, color):
    for start, end, label in labels:
        if label == 'S' or label == 's':
            ax.axvspan(start, end, alpha=0.3, color='gray')
            ax.text((start + end) / 2, 0.8, 'S', ha='center', va='center', fontsize=8, fontweight='bold')
        if label == 'V' or label == 'v':
            ax.axvspan(start, end, alpha=0.5, color=color, hatch='///')
            ax.text((start + end) / 2, 0.8, 'V', ha='center', va='center', fontsize=8, fontweight='bold')
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([])

fig2, axes2 = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

time2 = np.arange(len(samples)) / fs
axes2[0].plot(time2, samples, 'b')
axes2[0].set_title('Senyal Original')
axes2[0].set_ylabel('Amplitud')
axes2[0].grid(True)

plot_labels(axes2[1], manual, 'blue')
axes2[1].set_title('Etiqueta Manual')
axes2[1].grid(True, axis='x')

plot_labels(axes2[2], auto, 'red')
axes2[2].set_title('Deteccio Automatica (-7dB)')
axes2[2].grid(True, axis='x')

for start, end, label in manual:
    if label == 'S' or label == 's':
        axes2[3].axvspan(start, end, alpha=0.3, color='gray')
    else:
        axes2[3].axvspan(start, end, alpha=0.3, color='blue', hatch='///')

for start, end, label in auto:
    if label != 'S' and label != 's':
        axes2[3].axvspan(start, end, alpha=0.3, color='red', hatch='...')

axes2[3].set_title('Comparacio: Blau=Manual, Vermell=Automatic')
axes2[3].set_xlabel('Temps (s)')
axes2[3].set_ylim(-0.1, 1.1)
axes2[3].set_yticks([])
axes2[3].grid(True, axis='x')

plt.tight_layout()
plt.savefig('img/labels_comparativa.png', dpi=150)
print('Grafic 2: img/labels_comparativa.png')

# ===== GRAFIC 3: Comparacio -10dB vs -7dB =====
auto_10 = []
with open(auto_10db) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            auto_10.append((float(parts[0]), float(parts[1]), parts[2]))

auto_7 = []
with open(auto_7db) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            auto_7.append((float(parts[0]), float(parts[1]), parts[2]))

fig3, axes3 = plt.subplots(5, 1, figsize=(14, 11), sharex=True)

axes3[0].plot(time2, samples, 'b')
axes3[0].set_title('Senyal Original')
axes3[0].set_ylabel('Amplitud')
axes3[0].grid(True)

plot_labels(axes3[1], manual, 'blue')
axes3[1].set_title('Etiqueta Manual')
axes3[1].grid(True, axis='x')

plot_labels(axes3[2], auto_10, 'red')
axes3[2].set_title('Deteccio Automatica (-10dB) - Original')
axes3[2].grid(True, axis='x')

plot_labels(axes3[3], auto_7, 'green')
axes3[3].set_title('Deteccio Automatica (-7dB) - Millorat')
axes3[3].grid(True, axis='x')

for start, end, label in manual:
    if label == 'S' or label == 's':
        axes3[4].axvspan(start, end, alpha=0.3, color='gray')
    else:
        axes3[4].axvspan(start, end, alpha=0.3, color='blue', hatch='///')

for start, end, label in auto_7:
    if label != 'S' and label != 's':
        axes3[4].axvspan(start, end, alpha=0.3, color='green', hatch='...')

axes3[4].set_title('Comparacio: Blau=Manual, Verd=Automatic (-7dB)')
axes3[4].set_xlabel('Temps (s)')
axes3[4].set_ylim(-0.1, 1.1)
axes3[4].set_yticks([])
axes3[4].grid(True, axis='x')

plt.tight_layout()
plt.savefig('img/comparativa_10db_vs_7db.png', dpi=150)
print('Grafic 3: img/comparativa_10db_vs_7db.png')

print("\n=== Tots 3 grafics creats a img/ ===")