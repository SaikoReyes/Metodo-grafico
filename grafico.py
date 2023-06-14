import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

restricciones_comp=[]
restricciones_graph = []


def graficar_restricciones(tipo, valores, xlim, ylim, solucion, restricciones_comp):

    
    x = np.linspace(xlim[0], xlim[1], 500)
    y = np.linspace(ylim[0], ylim[1], 500)
    X, Y = np.meshgrid(x, y)
    ligma = 0

    fig, ax = plt.subplots()
    #ax.margins(x=0.05, y=0.05)  # Ajusta los márgenes en un 5% del rango de datos
    plt.draw()

    # Crear una matriz de booleanos para almacenar las áreas factibles
    factible = np.ones_like(X, dtype=bool)

    restriccion_x = [0, 1]  # Ecuación de la línea del eje X: x = 0
    restriccion_y = [1, 0]  # Ecuación de la línea del eje Y: y = 0

    ax.plot([0, 0], ylim, color='blue', linestyle='dashed')  # Graficar línea del eje Y
    ax.plot(xlim, [0, 0], color='blue', linestyle='dashed')  # Graficar línea del eje X
    plt.draw()
    plt.pause(1)

    # Actualizar el área factible considerando las líneas de los ejes X e Y como restricciones
    factible = np.logical_and(factible, restriccion_x[0] * X + restriccion_x[1] * Y >= 0)
    factible = np.logical_and(factible, restriccion_y[0] * X + restriccion_y[1] * Y >= 0)

    for i, restriccion in enumerate(restricciones_comp):
        if tipo[i] == "<=":
            ax.contour(X, Y, restriccion[0] * X + restriccion[1] * Y, levels=[valores[i]], colors='b', linestyles='dashed',label='Restricción {i}')
            factible = np.logical_and(factible, restriccion[0] * X + restriccion[1] * Y <= valores[i])
        elif tipo[i] == ">=":
            ax.contour(X, Y, restriccion[0] * X + restriccion[1] * Y, levels=[valores[i]], colors='b', linestyles='dashed', label='Restricción {i}')
            factible = np.logical_and(factible, restriccion[0] * X + restriccion[1] * Y >= valores[i])
        plt.draw()
        plt.pause(1)

    # Rellenar el área factible con un color diferente
    ax.imshow(factible, extent=(xlim[0], xlim[1], ylim[0], ylim[1]), origin='lower', alpha=0.3, cmap='Greens')
    

    plt.draw()

    plt.pause(1)
    # Calcular el centro del área factible
    x_center = solucion[0]
    y_center = solucion[1]

    #ablecer los límites de los ejes X e Y alrededor del centro del área factible
    ax.set_xlim(x_center - 20, x_center + 20)
    ax.set_ylim(y_center - 20, y_center + 20)
    
    plt.xlabel('x')
    plt.ylabel('y')

    for restriccion in restricciones_graph:
        ax.text(0, ylim[1]-ligma, "'x'{restriccion[0]}'+ y'{restriccion[1]}' '{tipo[ligma]}' '{valores[ligma]}", color='blue', fontsize=10, ha='center')
        ligma = ligma + 1    
    

    
   
    plt.text(solucion[0], solucion[1],solucion)
    # Plot feasible solution point
    ax.plot(solucion[0], solucion[1], 'ro', label='Solución factible')
    plt.legend()
    plt.draw
    plt.draw()
    plt.pause(1)
    
    plt.show()


def main():
    num_restricciones = int(input("Ingrese el número de restricciones: "))
    restricciones = []
    tipo = []
    valores = []
    cont = []
    
    bandera = False
    p = 0
    for i in range(num_restricciones):
        restriccion = input(f"Ingrese la restricción {i + 1} en la forma 'ax + by <= ó >= c': ")
        restricciones_graph.append(restriccion)
        coeficientes = list(map(float, restriccion.split()[:5:2]))
        restricciones.append(coeficientes)
        tipo.append(restriccion.split()[3])
        valores.append(float(restriccion.split()[4]))
        for i in range(len(restriccion) - 1):
            if restriccion[i:i+2] == ">=":
                bandera = True
                cont.append(p)
        p += 1

    
    xlim = [-50,50]
    ylim = [-50,50]

    c = np.array(list(map(float, input("Ingrese los coeficientes de la función objetivo en la forma 'cx dy': ").split(' '))))
    for ress in restricciones:
        ress.pop()
        restricciones_comp.append(ress)

    if bandera:
        for posicion in cont:
            if 0 <= posicion < len(restricciones):
                subarreglo = restricciones[posicion]
                restricciones[posicion] = [-x for x in subarreglo]

    print(restricciones)
    A = np.array(restricciones)
    b = np.array(valores)

    res = linprog(-c, A_ub=A, b_ub=b, method='highs')

    print("Punto óptimo: ", res.x)
    print("Valor óptimo: ", -res.fun)
    print("Valor maximizado: ", res.fun)  # Agregar esta línea

    graficar_restricciones(tipo, valores, xlim, ylim, res.x, restricciones_comp)


if __name__ == "__main__":
    main()
