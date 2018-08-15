'''
Programa de ic para resolver o problema dos missionarios e canibais

Estado é [Margem, Margem, Barco] representa todo o mundo do problema

Margem é (Missionario, Canibal) representa a quantidade de
missionarios e canibais tem em uma margem do rio

Missionario e Canibal são numeros [0, 3] indicando quanto de cada um
tempo numa margem do rio


Barco é o lado que o barco está, sendo "direito" e "esquerdo"

Movimento é (Missionario, Canibal) representa os possiveis movimentos
que o barco pode fazer


Profundidade é Number, representa a profundidade máxima da árvore
'''

from functools import reduce
import operator as op
from pprint import PrettyPrinter

ESTADO_INICIAL = [(3, 3), (0, 0), "esquerda"]
META = [(0, 0), (3, 3), "direita"]
MOVIMENTOS = [(2, 0), (1, 0), (1, 1), (0, 1), (0, 2)]


def estado_valido(estado):
    """
    Estado -> Bool
    """
    def intervalo(termo):
        """
        Missionario ou Canibal -> Bool
        """
        return termo >= 0 and termo <= 3

    def sem_canibalismo(margem):
        """
        Margem -> Bool
        """
        return margem[0] == 0 or margem[0] >= margem[1]

    def verificacoes():
        """
        -> [Bool]
        """
        return [sem_canibalismo(estado[0]),
                sem_canibalismo(estado[1]),
                *list(map(intervalo, [*estado[0], *estado[1]]))]

    return reduce(op.and_, verificacoes())


def margem_operacao(operador):
    """
    (Number, Number)(->) -> (Margem, Movimento) -> (Number, Number)
    """
    def _margem_operacao(margem, movimento):
        """
        Margem, Movimento -> (Number, Number)
        """
        return (operador(margem[0], movimento[0]),
                operador(margem[1], movimento[1]))

    return _margem_operacao


margem_menos = margem_operacao(op.sub)
margem_mais = margem_operacao(op.add)


def movimentar(estado, movimento):
    """
    Estado, Movimento -> Estado
    """

    if estado[2] == "esquerda":
        op_esquerda, op_direita, lado = margem_menos, margem_mais, "direita"
    else:
        op_esquerda, op_direita, lado = margem_mais, margem_menos, "esquerda"

    return [op_esquerda(estado[0], movimento),
            op_direita(estado[1], movimento),
            lado]


def movimentos_validos(estado):
    """
    Estado -> [Estado]
    """
    def exec_movimento(movimento):
        """
        Movimento -> Estado
        """
        return movimentar(estado, movimento)
    return list(filter(estado_valido, map(exec_movimento, MOVIMENTOS)))


def resolver(estados, profundidade):
    """
    [Estado], Profundidade -> [Estado]
    """
    if profundidade == 0 or estados == []:
        return []

    if estados[0] == META:
        return [estados[0]]

    filhos = resolver(movimentos_validos(estados[0]), profundidade - 1)

    if filhos != []:
        return [estados[0], *filhos]

    return resolver(estados[1:], profundidade)


def iterativo(profundidade):
    """
    Profundidade -> [Estado]
    """
    resposta = resolver([ESTADO_INICIAL], profundidade)
    if resposta != []:
        return resposta
    return iterativo(profundidade + 1)


if __name__ == '__main__':
    RESPOSTA = iterativo(0)
    PrettyPrinter().pprint(RESPOSTA)
    print("Profundidade necessária: %i" % len(RESPOSTA))
