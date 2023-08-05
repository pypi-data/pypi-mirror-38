import numpy as np


class MLPClassifier:

    def __init__(self, x, y, peso_x, peso_y, peso_baias, complex_n=None):
        '''
        [
            {
                'x': {
                    'val': 0,
                    'peso': -5,
                },
                'y': {
                    'val': 0,
                    'peso': 5,
                },
                'ativacao': SIGMOIDE,
                'baias': 2
            },
            {
                'x': {
                    'val': 0,
                    'peso': -5,
                },
                'y': {
                    'val': 1,
                    'peso': 5,
                },
                'ativacao': SIGMOIDE,
                'baias': -3
            },
            {
                'x': {
                    'val': 1,
                    'peso': -5,
                },
                'y': {
                    'val': 0,
                    'peso': 5,
                },
                'ativacao': SIGMOIDE,
                'baias': 2
            },
            {
                'x': {
                    'val': 1,
                    'peso': -5,
                },
                'y': {
                    'val': 1,
                    'peso': 5,
                },
                'ativacao': SIGMOIDE,
                'baias': 2
            },


        ]
        '''
        self.x = x
        self.y = y
        self.peso_x = peso_x
        self.peso_y = peso_y
        self.peso_baias = peso_baias
        self.complex_n = complex_n

    def to_representation(self, funcao_ativacao):
        calculos = []
        if not self.complex_n:
            for idx, val in enumerate(self.x):
                resultado = val * self.peso_x + self.y[idx] * self.peso_y + self.peso_baias
                resultado = funcao_ativacao(resultado)
                calculos.append(resultado)
            return calculos

        for idx, value in enumerate(self.complex_n):
            ativacao = value['ativacao']
            resultado = (
                value['x']['val'] * value['x']['peso'] +
                value['y']['val'] * value['y']['peso'] + 
                value['baias']
            )
            calculos.append(funcao_ativacao(resultado))
        return calculos
    
