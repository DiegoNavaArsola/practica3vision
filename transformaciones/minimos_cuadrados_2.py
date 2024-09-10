import numpy as np
from PIL import Image

def mult_matrices(A, *matrices):
    result = np.array(A)
    for matrix in matrices:
        # Multiplicar usando np.dot
        result = np.dot(result, matrix.data)
    return result

def minimos_cuadrados(A, b):
    A = np.array(A)
    b = np.array(b)
    At = A.transpose()
    AtA = mult_matrices(At,A)
    AtAinv = np.linalg.inv(AtA)
    return mult_matrices(AtAinv, At, b)

def transform_matrix(proy, ort, num_imgs):
    A, b = [], []

    for i in range(num_imgs):
        x, y = proy[i]
        x_p, y_p = ort[i]

        A.append([x, y, 1, 0, 0, 0])
        A.append([0, 0, 0, x, y, 1])

        b.append(x_p)
        b.append(y_p)

    #print(A)
    #print(b)

    #t_matrix = minimos_cuadrados(A,b)
    t_matrix = np.linalg.solve(A, b)

    return t_matrix


def t_m(proy, ort, num_imgs):
    A = []
    b = []

    for i in range(num_imgs):
        x, y = proy[i]
        u, v = ort[i]

        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])

        b.append([0])
        b.append([0])

    print(np.array(A))
    print(np.array(b))

    A = np.array(A)
    b = np.array(b)

    t_matrix = minimos_cuadrados(A, b)
    #t_matrix, residuals, rank, s = np.linalg.lstsq(A)
    #U, S, Vh = np.linalg.svd(A)

    return np.array(t_matrix).reshape(3,3)

def create_homography_matrix(src, dst):
    # Construir la matriz A para Ax = 0
    A = []
    for i in range(len(src)):
        x, y = src[i][0], src[i][1]
        u, v = dst[i][0], dst[i][1]
        A.append([-x, -y, -1, 0, 0, 0, u * x, u * y, u])
        A.append([0, 0, 0, -x, -y, -1, v * x, v * y, v])

    A = np.array(A)

    # Resolver utilizando SVD
    U, S, Vh = np.linalg.svd(A)

    # La última fila de Vh corresponde al vector de solución (h11, h12, ..., h33)
    H = Vh[-1].reshape(3, 3)

    # Normalizar para que H33 sea igual a 1
    H = H / H[-1, -1]

    return H


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
            original_coords = np.dot(transformation_matrix, [x, y, 1])
            orig_x, orig_y = int(round(original_coords[0])), int(round(original_coords[1]))

            # Verificar si las coordenadas originales están dentro de los límites de la imagen original
            if 0 <= orig_x < width and 0 <= orig_y < height:
                # Asignar el valor del píxel original a la nueva imagen
                new_image_array[y, x] = image_array[orig_y, orig_x]

    # Convertir el array de vuelta a una imagen
    new_image = Image.fromarray(new_image_array)

    return new_image

if __name__ == "__main__":

    #A = [[0,1],[1,1],[2,1]]
    #b = [[6],[0],[0]]
    #A1 = np.array(A)
    #b1 = np.array(b)
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

    t = transform_matrix(puntos_proyectados,puntos_ortogonales, num_imgs)
    #t_m = t.reshape(2,3)
    #print(t_m)

    #t2 = create_homography_matrix(puntos_ortogonales, puntos_ortogonales)
    #print(t2)

    t_3 = t_m(puntos_proyectados, puntos_ortogonales, num_imgs)
    print(t_3)

    #img_ort = project_image(img, t_3)
    #img_ort.show()

    #img_ort = project_image(img,t2)
    #img_ort.show()
