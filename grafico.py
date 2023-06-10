import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

def graficar_restricciones(restricciones, tipo, valores, xlim, ylim, solucion):
    x = np.linspace(xlim[0], xlim[1], 500)
    y = np.linspace(ylim[0], ylim[1], 500)
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots()
    for i, restriccion in enumerate(restricciones):
        if tipo[i] == "<=":
            ax.contour(X, Y, restriccion[0] * X + restriccion[1] * Y, levels=[valores[i]], colors='b', linestyles='dashed')
            ax.fill_between(x, (valores[i] - restriccion[0] * x) / restriccion[1], ylim[1], color='gray', alpha=0.2)
        elif tipo[i] == ">=":
            ax.contour(X, Y, restriccion[0] * X + restriccion[1] * Y, levels=[valores[i]], colors='b', linestyles='dashed')
            ax.fill_between(x, (valores[i] - restriccion[0] * x) / restriccion[1], ylim[0], color='gray', alpha=0.2)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    plt.xlabel('x')
    plt.ylabel('y')

    # Plot feasible solution point
    ax.plot(solucion[0], solucion[1], 'ro', label='Solución factible')
    ax.legend()
    
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
        coeficientes = list(map(float, restriccion.split()[:5:2]))
        restricciones.append(coeficientes)
        tipo.append(restriccion.split()[3])
        valores.append(float(restriccion.split()[4]))
        for i in range(len(restriccion) - 1):
            if restriccion[i:i+2] == ">=":
                bandera = True
                cont.append(p)
        p += 1

    xlim = [float(input("Ingrese el límite inferior de x: ")), float(input("Ingrese el límite superior de x: "))]
    ylim = [float(input("Ingrese el límite inferior de y: ")), float(input("Ingrese el límite superior de y: "))]

    c = np.array(list(map(float, input("Ingrese los coeficientes de la función objetivo en la forma 'cx dy': ").split(' '))))
    for ress in restricciones:
        ress.pop()

    if bandera:
        for posicion in cont:
            if 0 <= posicion < len(restricciones):
                subarreglo = restricciones[posicion]
                restricciones[posicion] = [-x for x in subarreglo]

    A = np.array(restricciones)
    b = np.array(valores)

    res = linprog(-c, A_ub=A, b_ub=b, method='highs')

    print("Punto óptimo: ", res.x)
    print("Valor óptimo: ", -res.fun)
    print("Valor maximizado: ", res.fun)  # Agregar esta línea

    graficar_restricciones(restricciones, tipo, valores, xlim, ylim, res.x)


if __name__ == "__main__":
    main()
