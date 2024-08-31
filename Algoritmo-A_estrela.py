import heapq
import time

class No:
    def __init__(self, tabuleiro, pai=None, movimento=0, custo=0):
        self.tabuleiro = tabuleiro  # Estado atual do tabuleiro
        self.pai = pai  # Estado pai
        self.movimento = movimento  # Número de movimentos realizados até agora
        self.custo = custo  # Custo total (movimentos + heurística)
        self.pos_zero = self.tabuleiro.index(0)  # Posição do espaço vazio (0)

    def __lt__(self, outro):
        return self.custo < outro.custo  # Comparação baseada no custo para a fila de prioridade

    def gerar_filhos(self):
        filhos = []
        x, y = divmod(self.pos_zero, 3)  # Converter posição linear para coordenadas 2D (3x3)
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimentos possíveis: Cima, Baixo, Esquerda, Direita

        for movimento in movimentos:
            novo_x, novo_y = x + movimento[0], y + movimento[1]
            if 0 <= novo_x < 3 and 0 <= novo_y < 3:  # Verificar se o movimento é válido
                nova_pos = novo_x * 3 + novo_y  # Converter de volta para posição linear
                novo_tabuleiro = self.tabuleiro[:]  # Copiar o tabuleiro atual
                novo_tabuleiro[self.pos_zero], novo_tabuleiro[nova_pos] = novo_tabuleiro[nova_pos], novo_tabuleiro[self.pos_zero]  # Trocar posições
                filhos.append(No(novo_tabuleiro, self, self.movimento + 1))  # Adicionar novo estado filho

        return filhos

    def obter_caminho(self):
        caminho = []
        atual = self
        while atual:
            caminho.append(atual)  # Adicionar estado atual ao caminho
            atual = atual.pai  # Ir para o estado pai
        return caminho[::-1]  # Inverter para obter o caminho na ordem correta


def h1(tabuleiro, objetivo):
    """Heurística h1: número de peças fora da posição."""
    return sum(1 for i in range(len(tabuleiro)) if tabuleiro[i] != objetivo[i] and tabuleiro[i] != 0)


def h2(tabuleiro, objetivo):
    """Heurística h2: Distância Manhattan."""
    distancia = 0
    for i in range(1, 9):  # Peças de 1 a 8
        x1, y1 = divmod(tabuleiro.index(i), 3)
        x2, y2 = divmod(objetivo.index(i), 3)
        distancia += abs(x1 - x2) + abs(y1 - y2)  # Calcular a distância Manhattan
    return distancia

def a_estrela(inicio, objetivo, heuristica):
    tempo_inicio = time.perf_counter()  # Iniciar contagem do tempo
    lista_aberta = []  # Lista de estados a serem explorados
    lista_fechada = set()  # Conjunto de estados já explorados
    heapq.heappush(lista_aberta, (0, inicio))  # Adicionar estado inicial na lista de prioridade

    while lista_aberta:
        _, atual = heapq.heappop(lista_aberta)  # Pegar estado com menor custo

        if atual.tabuleiro == objetivo:  # Verificar se é o estado objetivo
            tempo_fim = time.perf_counter()  # Parar contagem do tempo
            return atual.obter_caminho(), len(lista_fechada), tempo_fim - tempo_inicio  # Retornar caminho, número de nós e tempo

        lista_fechada.add(tuple(atual.tabuleiro))  # Adicionar estado atual aos explorados

        for filho in atual.gerar_filhos():  # Gerar estados filhos
            if tuple(filho.tabuleiro) in lista_fechada:  # Ignorar estados já explorados
                continue

            filho.custo = atual.movimento + heuristica(filho.tabuleiro, objetivo)  # Calcular custo do estado filho
            heapq.heappush(lista_aberta, (filho.custo, filho))  # Adicionar estado filho na lista de prioridade

    return None, None, None  # Caso não encontre solução


def imprimir_tabuleiro(tabuleiro):
    for i in range(0, 9, 3):
        print(tabuleiro[i:i + 3])  # Imprimir tabuleiro em formato 3x3
    print()

def executar_experimento(inicio, objetivo, heuristica, nome_heuristica):
    print()
    print(f"Experimento - {nome_heuristica}:")
    caminho, nos, tempo_gasto = a_estrela(No(inicio), objetivo, heuristica)
    print(f"Nós gerados: {nos}, Tempo: {tempo_gasto:.4f} segundos")
    print("Caminho para a solução:")
    for passo in caminho:
        imprimir_tabuleiro(passo.tabuleiro)
    print("G(n): ", caminho[-1].movimento)

if __name__ == "__main__":
    # Estados para os experimentos
    inicio1 = [2, 8, 3, 1, 6, 4, 0, 7, 5]
    objetivo1 = [1, 2, 3, 8, 0, 4, 7, 6, 5]

    inicio2 = [7, 2, 4, 5, 0, 6, 8, 3, 1]
    objetivo2 = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    # Experimento 1
    executar_experimento(inicio1, objetivo1, h1, "Experimento 1 - h1")
    executar_experimento(inicio1, objetivo1, h2, "Experimento 1 - h2")

    # Experimento 2
    executar_experimento(inicio2, objetivo2, h1, "Experimento 2 - h1")
    executar_experimento(inicio2, objetivo2, h2, "Experimento 2 - h2")