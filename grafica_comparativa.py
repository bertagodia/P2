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
manual_file = 'PAV_2121_manual.lab'
auto_file = 'nouparametres.txt'

# Llegir WAV
with open(wav_file, 'rb') as f:
    f.read(44)
    data = f.read()
samples = np.array(struct.unpack('<' + 'h' * (len(data)//2), data), dtype=np.float32)
samples = samples / 32768.0

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

# Temps
N = len(samples)
time = np.arange(N) / fs

# Crear grafica
fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

# 1. Senyal temporal
axes[0].plot(time, samples, 'b')
axes[0].set_title('Senyal temporal')
axes[0].set_ylabel('Amplitud')
axes[0].grid(True)

# 2. Etiquetat manual
def plot_labels_manual(ax, labels, color):
    for start, end, label in labels:
        if label == 'SILENCIO':
            ax.axvspan(start, end, alpha=0.3, color='gray')
            ax.text((start + end) / 2, 0.8, 'S', ha='center', va='center', fontsize=10, fontweight='bold')
        if label == 'VOZ':
            ax.axvspan(start, end, alpha=0.5, color=color, hatch='///')
            ax.text((start + end) / 2, 0.8, 'V', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([])

plot_labels_manual(axes[1], manual, 'blue')
axes[1].set_title('Etiquetat manual')
axes[1].grid(True, axis='x')

# 3. Deteccio automatica
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

plot_labels_auto(axes[2], auto, 'red')
axes[2].set_title('Deteccio automatica')
axes[2].grid(True, axis='x')

# 4. Comparacio
for start, end, label in manual:
    if label == 'S' or label == 's':
        axes[3].axvspan(start, end, alpha=0.3, color='gray')
    else:
        axes[3].axvspan(start, end, alpha=0.3, color='blue', hatch='///')

for start, end, label in auto:
    if label != 'S' and label != 's':
        axes[3].axvspan(start, end, alpha=0.3, color='red', hatch='...')

axes[3].set_title('Comparacio: Blau=Manual, Vermell=Automatic')
axes[3].set_xlabel('Temps (s)')
axes[3].set_ylim(-0.1, 1.1)
axes[3].set_yticks([])
axes[3].grid(True, axis='x')

plt.tight_layout()
plt.savefig('vad_comparison.png', dpi=150)
print('Grafic guardat: vad_comparison.png')
