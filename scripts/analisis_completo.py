import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# --- Configuración ---
if len(sys.argv) < 3:
    print("Uso: python3 analisis_completo.py <archivo_csv> <etiqueta_salida>")
    sys.exit(1)

filename = sys.argv[1]
label = sys.argv[2]  # Ej: "diluido" o "denso"
out_dir = "results"

if not os.path.exists(filename):
    print(f"Error: No se encuentra {filename}")
    sys.exit()

print(f"Procesando {filename}...")
data = pd.read_csv(filename)
time = data['t'].values
N = (len(data.columns) - 1) // 4
steps = len(time)

# --- 1. Calcular Energías (Post-procesamiento) ---
# Nota: Lo ideal es calcularlo en C++, pero hacerlo aquí es flexible.
# Constantes del modelo (deben coincidir con C++)
EPSILON = 1.0
SIGMA = 1.0
MASS = 1.0

K = np.zeros(steps)
V = np.zeros(steps)

print("Calculando energías (esto puede tardar unos segundos)...")

# Extraer posiciones y velocidades en arrays de numpy para velocidad
# Forma: (Steps, N)
X = np.zeros((steps, N))
Y = np.zeros((steps, N))
VX = np.zeros((steps, N))
VY = np.zeros((steps, N))

for i in range(N):
    X[:, i] = data[f'x{i}'].values
    Y[:, i] = data[f'y{i}'].values
    VX[:, i] = data[f'vx{i}'].values
    VY[:, i] = data[f'vy{i}'].values

# Energía Cinética: Sum(0.5 * m * v^2)
V2 = VX**2 + VY**2
K = 0.5 * MASS * np.sum(V2, axis=1)

# Energía Potencial: Sum(Pairs) Lennard Jones
# Vectorizado por pasos de tiempo sería complejo, hacemos bucle optimizado
for t in range(0, steps, 5): # Saltamos pasos para graficar más rápido si son muchos datos
    pos_x = X[t, :]
    pos_y = Y[t, :]
    v_step = 0.0
    
    # Doble bucle de pares
    for i in range(N):
        for j in range(i + 1, N):
            dx = pos_x[i] - pos_x[j]
            dy = pos_y[i] - pos_y[j]
            r2 = dx*dx + dy*dy
            r = np.sqrt(r2)
            
            # Evitar división por cero si colapsan (no debería pasar)
            if r < 0.1: r = 0.1
            
            sr = SIGMA / r
            sr6 = sr**6
            sr12 = sr6**2
            v_step += 4.0 * EPSILON * (sr12 - sr6)
    V[t] = v_step

# Interpolar pasos saltados para suavizar gráfica
mask = V != 0
V_full = np.interp(np.arange(steps), np.arange(steps)[mask], V[mask])
E_total = K + V_full

# --- GRAFICA 1: TRAYECTORIAS ---
plt.figure(figsize=(6, 6))
for i in range(min(N, 10)): # Graficar máx 10 partículas
    plt.plot(X[:, i], Y[:, i], '-', alpha=0.6, lw=1)
    plt.plot(X[0, i], Y[0, i], 'o', markersize=3) # Inicio
    plt.plot(X[-1, i], Y[-1, i], 'x', markersize=5) # Fin
plt.title(f"Trayectorias ({label})")
plt.xlabel("X"); plt.ylabel("Y")
plt.axis('equal'); plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"{out_dir}/trayectoria_{label}.png")
plt.close()

# --- GRAFICA 2: CONSERVACIÓN DE ENERGÍA ---
plt.figure(figsize=(8, 5))
plt.plot(time, E_total, label='Energía Total', color='black', lw=1.5)
plt.plot(time, K, label='Cinética (K)', color='red', alpha=0.5, ls='--')
plt.plot(time, V_full, label='Potencial (V)', color='blue', alpha=0.5, ls='--')
plt.title(f"Estabilidad de Energía - Velocity Verlet ({label})")
plt.xlabel("Tiempo")
plt.ylabel("Energía")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{out_dir}/energia_{label}.png")
plt.close()

# --- GRAFICA 3: HISTOGRAMA DE VELOCIDADES ---
# Tomamos la segunda mitad de la simulación (cuando ya está en equilibrio)
velocities = np.sqrt(V2[steps//2:, :].flatten())
plt.figure(figsize=(7, 5))
plt.hist(velocities, bins=30, density=True, alpha=0.7, color='green', edgecolor='black')
plt.title(f"Distribución de Velocidades ({label})")
plt.xlabel("Velocidad |v|")
plt.ylabel("Probabilidad")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"{out_dir}/histograma_{label}.png")
plt.close()

print(f"¡Listo! Gráficas guardadas en {out_dir}/ como trayectoria_{label}.png, energia_{label}.png, etc.")
