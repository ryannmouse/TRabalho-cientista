from questao_2 import AVLTree, Node

class RankingNode(Node):
    def __init__(self, id_participante, pontuacao):
        super().__init__(id_participante)  # Chama o construtor da classe base
        self.pontuacao = pontuacao  # Adiciona o atributo específico de ranking

class RankingAVL(AVLTree):
    def __init__(self):
        super().__init__()  # Inicializa a árvore AVL

    def insert(self, root, id_participante, pontuacao):
        # Insere um novo participante na árvore AVL
        if not root:
            return RankingNode(id_participante, pontuacao)  # Cria um novo nó se a raiz for None

        # Decide se deve inserir à esquerda ou à direita
        if id_participante < root.value:
            root.left = self.insert(root.left, id_participante, pontuacao)
        elif id_participante > root.value:
            root.right = self.insert(root.right, id_participante, pontuacao)
        else:
            root.pontuacao = pontuacao  # Atualiza a pontuação se o participante já existir

        return self.balance(root)  # Balanceia a árvore e retorna a nova raiz

    def inserir(self, id_participante, pontuacao):
        # Método público para inserir um participante na árvore
        self.root = self.insert(self.root, id_participante, pontuacao)

    def buscar(self, root, id_participante):
        # Busca um participante na árvore AVL
        if not root or root.value == id_participante:
            return root  # Retorna o nó se encontrado ou None se não houver

        if id_participante < root.value:
            return self.buscar(root.left, id_participante)  # Busca à esquerda
        return self.buscar(root.right, id_participante)  # Busca à direita

    def atualizar_pontuacao(self, id_participante, nova_pontuacao):
        # Atualiza a pontuação de um participante
        participante = self.buscar(self.root, id_participante)
        if participante:
            participante.pontuacao = nova_pontuacao
            self.root = self.insert(self.root, id_participante, nova_pontuacao)  # Reinsere para balancear

    def remover(self, id_participante):
        # Remove um participante da árvore AVL
        self.root = self.delete(self.root, id_participante)

    def top_10(self):
        # Retorna os 10 participantes com as maiores pontuações
        resultado = []
        self._inorder_desc(self.root, resultado)
        return resultado[:10]  # Retorna os 10 primeiros da lista

    def menor_pontuacao(self):
        # Retorna o participante com a menor pontuação
        if not self.root:
            return None
        return self.min_value_node(self.root)  # Encontra o nó com a menor pontuação

    def participantes_com_pontuacao_minima(self, min_pontuacao):
        # Retorna todos os participantes com pontuação maior ou igual a uma pontuação específica
        resultado = []
        self._buscar_maior_igual(self.root, min_pontuacao, resultado)
        return resultado

    def _buscar_maior_igual(self, node, min_pontuacao, resultado):
        # Coleta participantes com pontuação maior ou igual a uma pontuação específica
        if not node:
            return
        if node.pontuacao >= min_pontuacao:
            self._buscar_maior_igual(node.right, min_pontuacao, resultado)
            resultado.append((node.value, node.pontuacao))
            self._buscar_maior_igual(node.left, min_pontuacao, resultado)

    def _inorder_desc(self, node, resultado):
        # Percurso Em-Ordem Decrescente para coletar os nós em uma lista
        if not node:
            return
        self._inorder_desc(node.right, resultado)
        resultado.append((node.value, node.pontuacao))
        self._inorder_desc(node.left, resultado)

# Teste da classe RankingAVL
# Teste da classe RankingAVL
# Teste da classe RankingAVL
if __name__ == "__main__":
    ranking = RankingAVL()

    # Inserir participantes usando o método 'inserir' da classe RankingAVL
    ranking.inserir("player1", 100)
    ranking.inserir("player2", 150)
    ranking.inserir("player3", 200)
    ranking.inserir("player4", 120)
    ranking.inserir("player5", 130)
    ranking.inserir("player6", 170)
    ranking.inserir("player7", 90)
    ranking.inserir("player8", 180)
    ranking.inserir("player9", 110)
    ranking.inserir("player10", 160)
    ranking.inserir("player11", 140)

    # Testar a exibição dos 10 melhores
    top_10 = ranking.top_10()
    print("Top 10 participantes:")
    for participante in top_10:
        print(f"ID: {participante[0]}, Pontuação: {participante[1]}")
    
    # Testar a busca e atualização de pontuação
    print("\nAtualizando a pontuação do player5...")
    ranking.atualizar_pontuacao("player5", 200)

    # Buscar um participante
    print("\nBuscando o player5:")
    participante = ranking.buscar(ranking.root, "player5")
    if participante:
        print(f"ID: {participante.value}, Pontuação: {participante.pontuacao}")
    else:
        print("Participante não encontrado.")
    
    # Testar a remoção de um participante
    print("\nRemovendo o player7...")
    ranking.remover("player7")

    # Verificar o ranking após a remoção
    print("\nRanking após remoção do player7:")
    top_10 = ranking.top_10()
    for participante in top_10:
        print(f"ID: {participante[0]}, Pontuação: {participante[1]}")

    # Testar a busca do participante com a menor pontuação
    print("\nBuscando o participante com a menor pontuação:")
    menor = ranking.menor_pontuacao()
    if menor:
        print(f"ID: {menor.value}, Pontuação: {menor.pontuacao}")
    else:
        print("Não há participantes.")
    
    # Testar a busca de participantes com pontuação mínima
    print("\nBuscando participantes com pontuação maior ou igual a 150:")
    participantes = ranking.participantes_com_pontuacao_minima(150)
    for participante in participantes:
        print(f"ID: {participante[0]}, Pontuação: {participante[1]}")

