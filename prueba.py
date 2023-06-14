import matplotlib.pyplot as plt

# Crear una lista de valores para el eje X
x = [0, 0]

# Crear una lista de valores para el eje Y
y = [-10, 10]  # Esto generará una línea vertical a lo largo del eje Y

# Graficar la línea correspondiente a X = 0
plt.plot(x, y, 'r-', label='X = 0')

# Graficar la línea correspondiente a Y = 0
plt.axhline(0, color='b', linestyle='--', label='Y = 0')

# Configurar los ejes y el título del gráfico
plt.xlabel('Eje X')
plt.ylabel('Eje Y')
plt.title('Líneas correspondientes a X = 0 e Y = 0')

# Mostrar una leyenda explicando las líneas
plt.legend()

# Mostrar el gráfico
plt.show()
