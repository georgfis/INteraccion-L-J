import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

filename = sys.argv[1] if len(sys.argv) > 1 else "results/data.csv"
title_suffix = sys.argv[2] if len(sys.argv) > 2 else ""
out_name = sys.argv[3] if len(sys.argv) > 3 else "results/plot.png"

if not os.path.exists(filename):
    print(f"Error: No existe el archivo {filename}")
    sys.exit()

data = pd.read_csv(filename)
N = (len(data.columns) - 1) // 4

plt.figure(figsize=(7, 7))
limit = min(N, 20) 
colors = plt.cm.viridis(np.linspace(0, 1, limit))

for i in range(limit):
    plt.plot(data[f'x{i}'], data[f'y{i}'], '-', lw=1, alpha=0.8, color=colors[i])
    plt.plot(data[f'x{i}'].iloc[-1], data[f'y{i}'].iloc[-1], 'o', markersize=4, color=colors[i])

plt.title(f"Trayectorias: {title_suffix} (N={N})")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(out_name)
print(f"Gráfica guardada en {out_name}")
