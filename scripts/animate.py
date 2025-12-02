import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import os

# Argumentos: archivo_csv, archivo_salida
filename = sys.argv[1] if len(sys.argv) > 1 else "results/data.csv"
output_file = sys.argv[2] if len(sys.argv) > 2 else "results/animacion.gif"
SKIP_STEPS = 5  # Velocidad de la animacion

if not os.path.exists(filename):
    print(f"Error: No se encuentra el archivo de datos: {filename}")
    sys.exit()

print(f"Leyendo datos de {filename}...")
try:
    data = pd.read_csv(filename)
except Exception as e:
    print(f"Error leyendo CSV: {e}")
    sys.exit()

# Detectar numero de particulas (columnas: t, x0, y0, vx0, vy0...)
# Total columnas = 1 (t) + 4*N
N = (len(data.columns) - 1) // 4
width = 20.0  # Asumimos caja 20x20

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, width)
ax.set_ylim(0, width)
ax.set_aspect('equal')
ax.grid(True, alpha=0.2)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title(f"Simulacion N={N}")

# Particulas en azul
particles = ax.scatter([], [], c='dodgerblue', s=60, edgecolors='black', alpha=0.8)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    particles.set_offsets(np.empty((0, 2)))
    time_text.set_text('')
    return particles, time_text

def update(frame):
    row = data.iloc[frame]
    xs = [row[f'x{i}'] for i in range(N)]
    ys = [row[f'y{i}'] for i in range(N)]
    
    xy = np.column_stack((xs, ys))
    particles.set_offsets(xy)
    
    current_time = row['t']
    time_text.set_text(f'Time: {current_time:.2f}')
    return particles, time_text

# Generar frames
n_rows = len(data)
frames_indices = range(0, n_rows, SKIP_STEPS)

print(f"Generando {len(frames_indices)} cuadros para {output_file}...")

ani = animation.FuncAnimation(
    fig, update, frames=frames_indices, init_func=init, blit=True, interval=20
)

# Guardar
if output_file.endswith('.mp4'):
    ani.save(output_file, writer='ffmpeg', fps=30)
else:
    ani.save(output_file, writer='pillow', fps=30)

print(f"¡Animacion guardada exitosamente en {output_file}!")
