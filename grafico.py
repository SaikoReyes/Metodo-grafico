import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

restricciones_comp=[]
restricciones_graph = []

def mostrar_resultado(punto_optimo, valor_optimo):
    ventana = tk.Tk()
    ventana.title("Resultado")
    ventana.geometry("600x400")

    etiqueta = tk.Label(ventana, text="Este es el resultado:", font=("Arial", 18))
    etiqueta.pack(pady=10)

    etiqueta_punto_optimo = tk.Label(ventana, text=f"Punto óptimo: {punto_optimo}", font=("Arial", 14))
    etiqueta_punto_optimo.pack(pady=5)

    etiqueta_valor_opt = tk.Label(ventana, text=f"Valor óptimo: {valor_optimo}", font=("Arial", 14))
    etiqueta_valor_opt.pack(pady=5)

    boton_cerrar = tk.Button(ventana, text="Mostrar grafico", command=ventana.destroy, font=("Arial", 14))
    boton_cerrar.pack(pady=10)

    ventana.mainloop()

def graficar_restricciones(tipo, valores, xlim, ylim, solucion, restricciones_comp):

    x = np.linspace(xlim[0], xlim[1], 500)
    y = np.linspace(ylim[0], ylim[1], 500)
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots()
    plt.draw()

    factible = np.ones_like(X, dtype=bool)

    restriccion_x = [0, 1]
    restriccion_y = [1, 0]

    ax.plot([0, 0], ylim, color='blue', linestyle='dashed')
    ax.plot(xlim, [0, 0], color='blue', linestyle='dashed')
    plt.draw()
    plt.pause(1)

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

    ax.imshow(factible, extent=(xlim[0], xlim[1], ylim[0], ylim[1]), origin='lower', alpha=0.3, cmap='Greens')
    

    plt.draw()

    plt.pause(1)

    x_center = solucion[0]
    y_center = solucion[1]


    ax.set_xlim(x_center - 20, x_center + 20)
    ax.set_ylim(y_center - 20, y_center + 20)
    
    plt.xlabel('x')
    plt.ylabel('y')
   
    plt.text(solucion[0], solucion[1],solucion)

    ax.plot(solucion[0], solucion[1], 'ro', label='Solución factible')
    plt.legend()
    plt.draw
    plt.draw()
    plt.pause(1)
    
    plt.show()

def solucionador(restricciones, tipo, valores, cont, c, bandera):
 
    xlim = [-50,50]
    ylim = [-50,50]


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
    print("Valor maximizado: ", res.fun)

    punto_optimo = res.x
    valor_optimo = -res.fun
    mostrar_resultado(punto_optimo, valor_optimo)
    graficar_restricciones(tipo, valores, xlim, ylim, res.x, restricciones_comp)


def obtener_datos():
    try:
        num_restricciones = int(entry_num_restricciones.get())
        restricciones = []
        tipo = []
        valores = []
        cont = []
        bandera = False
        p = 0

        for i in range(num_restricciones):
            restriccion = entries_restricciones[i].get()
            coeficientes = list(map(float, restriccion.split()[:5:2]))
            restricciones.append(coeficientes)
            tipo.append(restriccion.split()[3])
            valores.append(float(restriccion.split()[4]))
            for i in range(len(restriccion) - 1):
                if restriccion[i:i+2] == ">=":
                    bandera = True
                    cont.append(p)
            p += 1

        c = np.array(list(map(float, entry_func_objetivo.get().split(' '))))
        ventana.destroy()
        solucionador(restricciones, tipo, valores, cont, c, bandera)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese datos válidos.")


ventana = tk.Tk()
ventana.title("Metodo grafico")

tk.Label(ventana, text="Número de restricciones:\n(Solo ingresar el numero de restricciones a colocar en los recuadros)\n\n\n").grid(row=0, column=0, sticky="w")
entry_num_restricciones = tk.Entry(ventana)
entry_num_restricciones.grid(row=0, column=1)

tk.Label(ventana, text="Función objetivo:\n(Ejemplo: 2 3 para 2x + 3y:)\n\n\n").grid(row=1, column=0, sticky="w")
entry_func_objetivo = tk.Entry(ventana)
entry_func_objetivo.grid(row=1, column=1)

tk.Label(ventana, text="Restricciones:\n(Ejemplo 2 + 3 <= 8 para 2x + 3y <= 8)").grid(row=2, column=0, sticky="w")
entries_restricciones = []
for i in range(10):
    entry_restriccion = tk.Entry(ventana)
    entry_restriccion.grid(row=2+i, column=1)
    entries_restricciones.append(entry_restriccion)

boton_obtener_datos = tk.Button(ventana, text="Obtener datos", command=obtener_datos)
boton_obtener_datos.grid(row=12, column=1, pady=10)

ventana.mainloop()