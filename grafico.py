import numpy as np
import time
import matplotlib.pyplot as plt

# Definir las restricciones
def restriccion1(x):
    return 4 - x

def restriccion2(x):
    return (12 - 2 * x) / 3

def restriccion3(x):
    return (18 - 3 * x) / 2




# Definir el dominio de x
x = np.linspace(0, 10, 100)

# Calcular los valores de y para cada restricción
y1 = restriccion1(x)
y2 = restriccion2(x)
y3 = restriccion3(x)

# Crear el gráfico
plt.figure()
time.sleep(1)
# Dibujar las restricciones
plt.plot(x, y1, label="x + y <= 4")
time.sleep(1)
plt.plot(x, y2, label="2x + 3y <= 12")
time.sleep(1)
plt.plot(x, y3, label="3x + 2y <= 18")
time.sleep(1)

# Rellenar el área factible
y_min = np.maximum(y1, 0)
y_max = np.minimum(np.minimum(y2, y3), 10)
plt.fill_between(x, y_min, y_max, where=(y_max > y_min), color="gray", alpha=0.5)
time.sleep(1)

# Configurar los ejes
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel("Eje X")
plt.ylabel("Eje Y")

# Agregar leyenda
plt.legend()


# Mostrar el gráfico

plt.show()