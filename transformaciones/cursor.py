from PIL import Image, ImageTk
from math import sin,exp,pi,log
import tkinter as tk
from tkinter import Label, Scale
import numpy as np

def generar_imagen(w,h,k1,k2,q1):
    gray = 255 / 2
    # Crea imagen nueva
    img = Image.new("L",(w,h))
    # En h disminuimos la magnitud del contraste hasta un valor intermedio (de abajo hacia arriba)
    for i in range(h):
        # En w aumentamos la fercuencia
        for j in range(w):
            gray_scale_value = int(gray - (gray) * -exp(q1 * -j) * sin(k1 * exp(k2*i)))
            img.putpixel((i, -1-j), gray_scale_value)
    return img

def coordenadas(evento):
    # Obtiene las coordenadas del cursor
    x, y = evento.x, evento.y
    # Valor asociado al gris
    # Verifica si el cursor está dentro de la imagen
    if 0 <= x < imagen.width and 0 <= y < imagen.height:
        # Muestra las coordenadas
        coords_etiqueta.config(text=f'Coordenadas: ({x}, {y})')
        # Obtiene el valor del píxel y muestra el color
        pixel_value = imagen_array[y, x]
        contraste_etiqueta.config(text=f'Valor de intensidad: {pixel_value}')
""" 
Creación de la imagen
"""
# Tamaño de imagen (width,height)
w, h = 512, 512
# Constantes de la función de frecuencia (exponencial). Obtenidos teóricamente
k2 = log(100*pi)/511
k1 = 1 / (100*k2)
# Constante de la función de difuniación (contraste). Empírica
q1 = 0.013

#Invoca a función para generar la imagen
imagen = Image.open("Ajedrez_Ortogonal-NW.png")
imagen_copia = imagen.copy()

"""
Carga de la imagen para obtenmer coordendas en una ventana
"""
#Convierte la imagen en un array
imagen_array = np.array(imagen)

# Configura la ventana principal
raiz = tk.Tk()
raiz.title("Mostrar Coordenadas de Píxeles")

# Crea un widget para mostrar la imagen
tk_image = ImageTk.PhotoImage(imagen)
etiqueta_imagen = tk.Label(raiz, image=tk_image)
etiqueta_imagen.pack(expand=True)

# Crea una etiqueta para mostrar las coordenadas
coords_etiqueta = Label(raiz, text='Coordenadas: (0, 0)')
coords_etiqueta.pack()

# Crea una etiqueta para mostrar el valor del píxel
contraste_etiqueta = Label(raiz, text='Valor de intensidad: ')
contraste_etiqueta.pack()

# Asocia el evento de movimiento del mouse al widget de imagen
etiqueta_imagen.bind('<Motion>', coordenadas)


# Ejecuta la aplicación
raiz.mainloop()
