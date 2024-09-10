import numpy as np

class Matrix:
    def __init__(self, data):
        """
        Inicializa una matriz a partir de una lista de listas o un array de Numpy.
        """
        self.data = np.array(data)

    def __repr__(self):
        return str(self.data)

    def __iter__(self):
        """
        Devuelve un iterador que itera sobre cada fila de la matriz.
        """
        return iter(self.data.tolist())

    def __getitem__(self, index):
        """
        Permite la suscripción para acceder a elementos de la matriz.

        Parámetros:
        index -- índice o tupla de índices para acceder a un elemento o submatriz

        Retorna:
        El valor del elemento o una submatriz.
        """
        # Verificar si el índice es una tupla de dos elementos
        if isinstance(index, tuple) or isinstance(index, list) or isinstance(index, int):
            if len(index) == 2:
                row, col = index
                return self.data[row, col]
            else:
                raise IndexError("Para una matriz 2D, el índice debe ser una tupla de dos elementos.")
        else:
            raise IndexError("El índice debe ser una tupla de dos elementos.")

    def shape(self):
        """
        Devuelve la forma (número de filas y columnas) de la matriz.
        """
        return self.data.shape

    def transpose(self):
        """
        Devuelve la transpuesta de la matriz.
        """
        return Matrix(self.data.T)

    def determinant(self):
        """
        Devuelve el determinante de la matriz si es cuadrada.
        """
        if self.data.shape[0] == self.data.shape[1]:
            return np.linalg.det(self.data)
        else:
            raise ValueError("El determinante solo se puede calcular para matrices cuadradas.")

    def add(self, other):
        """
        Suma dos matrices del mismo tamaño.
        """
        if self.data.shape == other.data.shape:
            return Matrix(self.data + other.data)
        else:
            raise ValueError("Las matrices deben tener el mismo tamaño para sumarlas.")

    def multiply(self, *matrices):
        """
        Multiplica la matriz actual por una o más matrices. Las dimensiones deben ser compatibles.

        Parámetros:
        matrices: Una o más matrices a multiplicar con la matriz actual.

        Retorna:
        Una nueva instancia de Matrix con el resultado de la multiplicación.
        """
        result = self.data  # Empezar con la matriz actual

        for matrix in matrices:
            if isinstance(matrix, Matrix):
                # Multiplicar usando np.dot
                result = np.dot(result, matrix.data)
            else:
                raise ValueError("Todos los elementos deben ser instancias de Matrix.")

        return Matrix(result)

    def scalar_multiply(self, scalar):
        """
        Multiplica la matriz por un escalar.
        """
        return Matrix(self.data * scalar)

    def inverse(self):
        """
        Devuelve la inversa de la matriz si es cuadrada y tiene inversa.
        """
        if self.data.shape[0] == self.data.shape[1]:
            return Matrix(np.linalg.inv(self.data))
        else:
            raise ValueError("Solo se puede calcular la inversa de matrices cuadradas.")

    def reshape(self, new_rows, new_cols):
        """
        Cambia la forma de la matriz a la nueva dimensión (new_rows x new_cols),
        siempre y cuando el número total de elementos se mantenga constante.

        Parámetros:
        new_rows -- número de filas en la nueva forma
        new_cols -- número de columnas en la nueva forma

        Retorna:
        Una nueva instancia de Matrix con la nueva forma.
        """
        # Verificar si la transformación es válida
        total_elements = self.data.size  # Número total de elementos en la matriz
        if total_elements != new_rows * new_cols:
            raise ValueError(
                f"No se puede redimensionar la matriz a ({new_rows}, {new_cols}) porque los elementos no coinciden.")

        # Realizar el cambio de forma
        new_data = self.data.reshape(new_rows, new_cols)
        return Matrix(new_data)

def minimos_cuadrados(A, b):
    Am = Matrix(A)
    bm = Matrix(b)
    At = Am.transpose()
    AtA = At.multiply(Am)
    AtAinv = AtA.inverse()
    return AtAinv.multiply(At, bm)
