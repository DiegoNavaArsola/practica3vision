import numpy as np

from matrix import Matrix, minimos_cuadrados
from PIL import Image


def find_transform_matrix_1(proy, ort, num_imgs):
    A, b = [], []

    for i in range(num_imgs):
        x, y = proy[i]
        x_p, y_p = ort[i]

        A.append([x, y, 1, 0, 0, 0])
        A.append([0, 0, 0, x, y, 1])

        b.append(x_p)
        b.append(y_p)

    print(A)
    print(b)

    t_matrix = minimos_cuadrados(A,b)

    return t_matrix

def find_transform_matrix(proy, ort, num_imgs):
    A = []
    b = []

    for i in range(num_imgs):
        x, y = proy[i]
        x_p, y_p = ort[i]

        A.append([x, y, 1, 0, 0, 0, -x_p * x, -x_p * y, -x_p])
        A.append([0, 0, 0, x, y, 1, -y_p * x, -y_p * y, -y_p])

        b.append([0])
        b.append([0])

    print(np.array(A))
    print(np.array(b))

    t_matrix = minimos_cuadrados(A, b)

    return t_matrix

def project_image(image, transformation_matrix):

    width, height = image.size
    # Convertir la imagen a un array de numpy
    image_array = np.array(image)

    # Crear una nueva imagen vacía para almacenar el resultado
    new_image_array = np.zeros_like(image_array)

    # Inversión de la matriz de transformación para mapear los píxeles proyectados de vuelta al espacio original
    #inv_T = np.linalg.inv(np.vstack([transformation_matrix, [0, 0, 1]]))[:2, :]

    # Recorrer cada píxel en la nueva imagen
    for y in range(height):
        for x in range(width):
            # Transformar la coordenada inversamente para saber de qué píxel original proviene
            original_coords = transformation_matrix.multiply(Matrix([x, y, 1]))
            print(original_coords)

            orig_x, orig_y = int(round(original_coords[(0,0)])), int(round(original_coords[(1,1)]))

            # Verificar si las coordenadas originales están dentro de los límites de la imagen original
            if 0 <= orig_x < width and 0 <= orig_y < height:
                # Asignar el valor del píxel original a la nueva imagen
                new_image_array[y, x] = image_array[orig_y, orig_x]

    # Convertir el array de vuelta a una imagen
    new_image = Image.fromarray(new_image_array)

    return new_image

if __name__ == "__main__":

    #A1 = [[0,1],[1,1],[2,1]]
    #b1 = [[6],[0],[0]]
    #v1 = minimos_cuadrados(A1,b1)
    #print(v1)

    img = Image.open("Ajedrez_Proyectado-NW.png")

    num_imgs = 5
    puntos_proyectados = [
        [326, 388],
        [575, 546],
        [511, 360],
        [468, 240],
        [712, 318]
    ]
    puntos_ortogonales = [
        [147, 104],
        [145, 339],
        [264, 222],
        [240, 382],
        [318, 382]
    ]

    valores = find_transform_matrix_1(puntos_proyectados,puntos_ortogonales,num_imgs)
    t = valores.reshape(2,3)

    t2 = np.array(t)
    img_ort = project_image(img, t)

