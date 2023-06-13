import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

restricciones_comp=[]

def graficar_restricciones(tipo, valores, xlim, ylim, solucion, restricciones_comp):
    x = np.linspace(xlim[0], xlim[1], 500)
    y = np.linspace(ylim[0], ylim[1], 500)
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots()
    plt.xlim(xlim[0],xlim[1])
    plt.ylim(ylim[0],ylim[1])
    plt.draw()

    # Crear una matriz de booleanos para almacenar las áreas factibles
    factible = np.ones_like(X, dtype=bool)

    for i, restriccion in enumerate(restricciones_comp):
        if tipo[i] == "<=":
            ax.contour(X, Y, restriccion[0] * X + restriccion[1] * Y, levels=[valores[i]], colors='b', linestyles='dashed')
            factible = np.logical_and(factible, restriccion[0] * X + restriccion[1] * Y <= valores[i])
        elif tipo[i] == ">=":
            ax.contour(X, Y, restriccion[0] * X + restriccion[1] * Y, levels=[valores[i]], colors='b', linestyles='dashed')
            factible = np.logical_and(factible, restriccion[0] * X + restriccion[1] * Y >= valores[i])

    # Rellenar el área factible con un color diferente
    ax.imshow(factible, extent=(xlim[0], xlim[1], ylim[0], ylim[1]), origin='lower', alpha=0.3, cmap='Greens')

    plt.draw()
    plt.pause(1)
    ax.autoscale()
    plt.legend()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    plt.xlabel('x')
    plt.ylabel('y')
   
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
        #restricciones_comp.append(restriccion)
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
