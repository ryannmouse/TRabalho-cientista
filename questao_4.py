## Questão 4 

# Definição da classe BTreeNode, que representa um nó na árvore B
class BTreeNode:
    def __init__(self, leaf=False):
        # Se o nó é folha ou não
        self.leaf = leaf
        # Lista de chaves armazenadas no nó
        self.keys = []
        # Lista de filhos do nó
        self.child = []


# Definição da classe BTree, que representa a árvore B
class BTree:
    def __init__(self, t):
        # O nó raiz é inicialmente uma folha
        self.root = BTreeNode(True)
        # 't' define a ordem da árvore B
        self.t = t

    # Função para inserir uma chave na árvore
    def insert(self, k):
        root = self.root
        # Se o nó raiz estiver cheio (contém 2t-1 chaves), precisamos dividir o nó
        if len(root.keys) == (2 * self.t) - 1:
            # Cria um novo nó para ser a nova raiz
            temp = BTreeNode()
            self.root = temp
            # A raiz antiga se torna um filho do novo nó
            temp.child.insert(0, root)
            # Divide o nó raiz
            self.split_child(temp, 0)
            # Insere a chave no novo nó
            self.insert_non_full(temp, k)
        else:
            # Caso a raiz não esteja cheia, insere diretamente
            self.insert_non_full(root, k)

    # Função para inserir uma chave em um nó não cheio
    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        # Se o nó é folha, inserimos a chave diretamente
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            # Se o nó não é folha, percorremos os filhos
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1
            i += 1
            # Se o filho está cheio, o dividimos
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k[0] > x.keys[i][0]:
                    i += 1
            # Recursivamente inserimos a chave no filho
            self.insert_non_full(x.child[i], k)

    # Função para dividir um filho que está cheio
    def split_child(self, x, i):
        t = self.t
        # Obtém o nó filho que será dividido
        y = x.child[i]
        # Cria um novo nó que vai conter a segunda metade das chaves de y
        z = BTreeNode(y.leaf)
        # Insere o novo nó como filho de x
        x.child.insert(i + 1, z)
        # Move a chave do meio de y para x
        x.keys.insert(i, y.keys[t - 1])
        # Divide as chaves de y entre y e z
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        # Se y não for folha, divide seus filhos
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t - 1]

    # Função para deletar uma chave de um nó
    def delete(self, x, k):
        t = self.t
        i = 0
        # Localiza a posição da chave k
        while i < len(x.keys) and k[0] > x.keys[i][0]:
            i += 1
        # Se o nó é folha e contém a chave, a remove
        if x.leaf:
            if i < len(x.keys) and x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return

        # Se a chave está no nó interno, chama uma função específica
        if i < len(x.keys) and x.keys[i][0] == k[0]:
            return self.delete_internal_node(x, k, i)
        # Se o filho à esquerda ou à direita não está cheio, resolve o problema com o irmão ou merge
        elif len(x.child[i].keys) >= t:
            self.delete(x.child[i], k)
        else:
            if i != 0 and i + 2 < len(x.child):
                if len(x.child[i - 1].keys) >= t:
                    self.delete_sibling(x, i, i - 1)
                elif len(x.child[i + 1].keys) >= t:
                    self.delete_sibling(x, i, i + 1)
                else:
                    self.delete_merge(x, i, i + 1)
            elif i == 0:
                if len(x.child[i + 1].keys) >= t:
                    self.delete_sibling(x, i, i + 1)
                else:
                    self.delete_merge(x, i, i + 1)
            elif i + 1 == len(x.child):
                if len(x.child[i - 1].keys) >= t:
                    self.delete_sibling(x, i, i - 1)
                else:
                    self.delete_merge(x, i, i - 1)
            self.delete(x.child[i], k)

    # Função para deletar um nó interno (não folha)
    def delete_internal_node(self, x, k, i):
        t = self.t
        # Se o nó é folha, remove a chave diretamente
        if x.leaf:
            if x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return

        # Se o filho da esquerda tem pelo menos t chaves, substitui a chave pelo predecessor
        if len(x.child[i].keys) >= t:
            x.keys[i] = self.delete_predecessor(x.child[i])
            return
        # Se o filho da direita tem pelo menos t chaves, substitui pela chave sucessora
        elif len(x.child[i + 1].keys) >= t:
            x.keys[i] = self.delete_successor(x.child[i + 1])
            return
        # Se os dois filhos têm menos de t chaves, realiza um merge
        else:
            self.delete_merge(x, i, i + 1)
            self.delete_internal_node(x.child[i], k, self.t - 1)

    # Função para deletar o predecessor
    def delete_predecessor(self, x):
        if x.leaf:
            return x.pop()
        n = len(x.keys) - 1
        if len(x.child[n].keys) >= self.t:
            self.delete_sibling(x, n + 1, n)
        else:
            self.delete_merge(x, n, n + 1)
        self.delete_predecessor(x.child[n])

    # Função para deletar o sucessor
    def delete_successor(self, x):
        if x.leaf:
            return x.keys.pop(0)
        if len(x.child[1].keys) >= self.t:
            self.delete_sibling(x, 0, 1)
        else:
            self.delete_merge(x, 0, 1)
        self.delete_successor(x.child[0])

    # Função para resolver o caso de merge de dois filhos
    def delete_merge(self, x, i, j):
        cnode = x.child[i]
        # Se o filho j está à direita de i
        if j > i:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.child) > 0:
                    cnode.child.append(rsnode.child[k])
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child.pop())
            new = cnode
            x.keys.pop(i)
            x.child.pop(j)
        else:
            # Se o filho j está à esquerda de i
            lsnode = x.child[j]
            lsnode.keys.append(x.keys[j])
            for i in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[i])
                if len(lsnode.child) > 0:
                    lsnode.child.append(cnode.child[i])
            if len(lsnode.child) > 0:
                lsnode.child.append(cnode.child.pop())
            new = lsnode
            x.keys.pop(j)
            x.child.pop(i)

        # Se a raiz foi esvaziada, a nova raiz se torna o novo nó
        if x == self.root and len(x.keys) == 0:
            self.root = new

    # Função para transferir uma chave de um irmão para o outro
    def delete_sibling(self, x, i, j):
        cnode = x.child[i]
        # Se i < j, o irmão está à direita
        if i < j:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            x.keys[i] = rsnode.keys[0]
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child[0])
                rsnode.child.pop(0)
            rsnode.keys.pop(0)
        else:
            # Se i > j, o irmão está à esquerda
            lsnode = x.child[j]
            cnode.keys.insert(0, x.keys[i - 1])
            x.keys[i - 1] = lsnode.keys.pop()
            if len(lsnode.child) > 0:
                cnode.child.insert(0, lsnode.child.pop())

    # Função para imprimir a árvore de forma recursiva
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        # Se houver filhos, percorre cada um recursivamente
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)


# Criando a árvore B com ordem 3
B = BTree(3)

# Inserindo chaves na árvore
for i in range(10):
    B.insert((i, 2 * i))

# Imprime a árvore após inserção
B.print_tree(B.root)

# Deletando a chave (8,)
B.delete(B.root, (8,))

# Imprime a árvore após a remoção
print("\n")
B.print_tree(B.root)