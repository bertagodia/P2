#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import numpy as np
import struct
import matplotlib.pyplot as plt

fs = 16000
wav_file = 'PAV_2121.wav'
old_file = 'PAV_2121.vad'
new_file = 'PAV_2121_auto.vad'
manual_file = 'PAV_2121.lab'

with open(wav_file, 'rb') as f:
    f.read(44)
    data = f.read()
samples = np.array(struct.unpack('<' + 'h' * (len(data)//2), data), dtype=np.float32)

N = len(samples)
time = np.arange(N) / fs
samples = samples[:N] / 32768.0

def read_labels(fname):
    labels = []
    with open(fname) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                labels.append((float(parts[0]), float(parts[1]), parts[2]))
    return labels

manual = read_labels(manual_file)
old = read_labels(old_file)
new = read_labels(new_file)

fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

axes[0].plot(time, samples, 'b', alpha=0.5)
axes[0].set_title('Senyal Original')
axes[0].set_ylabel('Amplitud')
axes[0].grid(True)

def plot_labels(ax, labels, color, title):
    for start, end, label in labels:
        if label == 'S':
            ax.axvspan(start, end, alpha=0.3, color='gray')
        else:
            ax.axvspan(start, end, alpha=0.5, color=color, hatch='///')
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([])
    ax.set_title(title)
    ax.grid(True, axis='x')

plot_labels(axes[1], manual, 'blue', 'Manual')
plot_labels(axes[2], old, 'red', 'Autentic (alpha0=13.9, zcr=3200, sil=130)')
plot_labels(axes[3], new, 'green', 'Nou (alpha0=12, zcr=3500, sil=110)')

axes[3].set_xlabel('Temps (s)')

plt.tight_layout()
plt.savefig('canvi.png', dpi=150)
print('Grafic guardat: canvi.png')