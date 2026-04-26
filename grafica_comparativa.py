#!/usr/bin/env python3
# VAD Comparison: Manual vs Automatic

import matplotlib
matplotlib.use('Agg')

import numpy as np
import struct
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Configuracio
fs = 16000
wav_file = 'PAV_2121.wav'
wav_canceled = 'PAV_2121_cancelado2.wav'
manual_file = 'PAV_2121.lab'
auto_file = 'PAV_2121_auto.vad'

# Llegir WAV
with open(wav_file, 'rb') as f:
    f.read(44)
    data = f.read()
samples = np.array(struct.unpack('<' + 'h' * (len(data)//2), data), dtype=np.float32)

# Llegir WAV cancelat
with open(wav_canceled, 'rb') as f:
    f.read(44)
    data = f.read()
samples_canceled = np.array(struct.unpack('<' + 'h' * (len(data)//2), data), dtype=np.float32)

# Temps
N = min(len(samples), len(samples_canceled))
time = np.arange(N) / fs
samples = samples[:N] / 32768.0
samples_canceled = samples_canceled[:N] / 32768.0

# Llegir manual
manual = []
with open(manual_file) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            manual.append((float(parts[0]), float(parts[1]), parts[2]))

# Llegir automatic
auto = []
with open(auto_file) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            auto.append((float(parts[0]), float(parts[1]), parts[2]))

# Crear grafica
fig, axes = plt.subplots(5, 1, figsize=(14, 12), sharex=True)

# 1. Senyal temporal
axes[0].plot(time, samples, 'b', alpha=0.5, label='Original')
axes[0].plot(time, samples_canceled, 'r', alpha=0.5, label='Cancelat')
axes[0].set_title('Comparacio: Original vs Soroll Cancelat')
axes[0].legend(loc='upper right')
axes[0].set_ylabel('Amplitud')
axes[0].grid(True)

# 2. Senyal original
axes[1].plot(time, samples, 'b')
axes[1].set_title('Senyal temporal original')
axes[1].set_ylabel('Amplitud')

# 3. Etiquetat manual
def plot_labels_manual(ax, labels, color):
    for start, end, label in labels:
        if label == 'S':
            ax.axvspan(start, end, alpha=0.3, color='gray')
            ax.text((start + end) / 2, 0.8, 'S', ha='center', va='center', fontsize=10, fontweight='bold')
        if label == 'V':
            ax.axvspan(start, end, alpha=0.5, color=color, hatch='///')
            ax.text((start + end) / 2, 0.8, 'V', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([])

plot_labels_manual(axes[2], manual, 'blue')
axes[2].set_title('Etiquetat manual')
axes[2].grid(True, axis='x')

# 4. Deteccio automatica
def plot_labels_auto(ax, labels, color):
    for start, end, label in labels:
        if label == 'S' or label == 's':
            ax.axvspan(start, end, alpha=0.3, color='gray')
            ax.text((start + end) / 2, 0.8, 'S', ha='center', va='center', fontsize=10, fontweight='bold')
        if label == 'V' or label == 'v':
            ax.axvspan(start, end, alpha=0.5, color=color, hatch='///')
            ax.text((start + end) / 2, 0.8, 'V', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([])

plot_labels_auto(axes[3], auto, 'red')
axes[3].set_title('Deteccio automatica')
axes[3].grid(True, axis='x')

# 5. Comparacio
for start, end, label in manual:
    if label == 'S' or label == 's':
        axes[4].axvspan(start, end, alpha=0.3, color='gray')
    else:
        axes[4].axvspan(start, end, alpha=0.3, color='blue', hatch='///')

for start, end, label in auto:
    if label != 'S' and label != 's':
        axes[4].axvspan(start, end, alpha=0.3, color='red', hatch='...')

axes[4].set_title('Comparacio: Blau=Manual, Vermell=Automatic')
axes[4].set_xlabel('Temps (s)')
axes[4].set_ylim(-0.1, 1.1)
axes[4].set_yticks([])
axes[4].grid(True, axis='x')

plt.tight_layout()
plt.savefig('labels_comparativa.png', dpi=150)
print('Grafic guardat: labels_comparativa.png')

# NOU GRAFIC: Comparacio audio Original vs Cancelat
# ......................................................

fig2, axes2 = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

axes2[0].plot(time, samples, 'b')
axes2[0].set_title('Senyal Original')
axes2[0].set_ylabel('Amplitud')
axes2[0].grid(True)

axes2[1].plot(time, samples_canceled, 'r')
axes2[1].set_title('Senyal Soroll Cancelat')
axes2[1].set_ylabel('Amplitud')
axes2[1].grid(True)

axes2[2].plot(time, samples, 'b', alpha=0.6, label='Original')
axes2[2].plot(time, samples_canceled, 'r', alpha=0.6, label='Cancelat')
axes2[2].set_title('Comparacio')
axes2[2].set_xlabel('Temps (s)')
axes2[2].set_ylabel('Amplitud')
axes2[2].legend(loc='upper right')
axes2[2].grid(True)

plt.tight_layout()
plt.savefig('audio_comparativa.png', dpi=150)
print('Grafic guardat: audio_comparativa.png')