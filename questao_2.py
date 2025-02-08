## Questão 2 
class Node:
    def _init_(self, value):
        # Inicializa um novo nó com um valor, e define filhos e altura
        self.value = value
        self.left = None  # Inicializa o filho esquerdo como None
        self.right = None  # Inicializa o filho direito como None
        self.height = 1  # Inicializa a altura do nó como 1


class AVLTree:
    def _init_(self):
        # Inicializa a árvore AVL com a raiz como None
        self.root = None

    def height(self, node):
        # Retorna a altura de um nó, sendo 0 se o nó for None
        if not node:
            return 0
        return node.height

    def balance(self, node):
        # Calcula o fator de balanceamento de um nó
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def insert(self, root, value):
        # Insere um novo valor na árvore AVL
        if not root:
            return Node(value)  # Se a raiz for None, cria um novo nó

        # Decide se deve inserir à esquerda ou à direita
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        # Atualiza a altura do nó atual
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)  # Calcula o fator de balanceamento

        # Realiza rotações para manter a árvore balanceada
        # Rotação à esquerda
        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)

        # Rotação à direita
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)

        # Rotação esquerda-direita
        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Rotação direita-esquerda
        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root  # Retorna o nó atualizado

    def delete(self, root, value):
        # Remove um valor da árvore AVL
        if not root:
            return root  # Se a raiz for None, retorna None

        # Decide se deve buscar à esquerda ou à direita
        if value < root.value:
            root.left = self.delete(root.left, value)
        elif value > root.value:
            root.right = self.delete(root.right, value)
        else:
            # Caso em que o nó a ser deletado é encontrado
            if not root.left:
                temp = root.right  # Se não houver filho esquerdo, promove o filho direito
                root = None  # Remove o nó atual
                return temp
            elif not root.right:
                temp = root.left  # Se não houver filho direito, promove o filho esquerdo
                root = None
                return temp

            # Nó com dois filhos: pega o menor valor do filho direito
            temp = self.min_value_node(root.right)
            root.value = temp.value  # Substitui o valor pelo menor valor encontrado
            root.right = self.delete(root.right, temp.value)  # Remove o nó duplicado

        if not root:
            return root  # Se a raiz se tornou None, retorna None

        # Atualiza a altura do nó atual
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)  # Calcula o fator de balanceamento

        # Realiza rotações para manter a árvore balanceada após a remoção
        # Rotação à esquerda
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        # Rotação à direita
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

        # Rotação esquerda-direita
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Rotação direita-esquerda
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root  # Retorna o nó atualizado

    def left_rotate(self, z):
        # Realiza uma rotação à esquerda em torno do nó z
        y = z.right  # O filho direito de z se torna o novo pai
        T2 = y.left  # T2 é o filho esquerdo de y

        y.left = z  # z se torna o filho esquerdo de y
        z.right = T2  # T2 se torna o filho direito de z

        # Atualiza as alturas dos nós envolvidos
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y  # Retorna o novo nó pai

    def right_rotate(self, z):
        # Realiza uma rotação à direita em torno do nó z
        y = z.left  # O filho esquerdo de z se torna o novo pai
        T3 = y.right  # T3 é o filho direito de y

        y.right = z  # z se torna o filho direito de y
        z.left = T3  # T3 se torna o filho esquerdo de z

        # Atualiza as alturas dos nós envolvidos
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y  # Retorna o novo nó pai

    def min_value_node(self, root):
        # Encontra o nó com o menor valor na subárvore
        current = root
        while current.left:
            current = current.left  # Continua indo para o filho esquerdo
        return current  # Retorna o nó com o menor valor

    def search(self, root, value):
        # Busca um valor na árvore AVL
        if not root or root.value == value:
            return root  # Retorna o nó se encontrado ou None se não houver

        if root.value < value:
            return self.search(root.right, value)  # Busca à direita
        return self.search(root.left, value)  # Busca à esquerda

    def insert_value(self, value):
        # Método público para inserir um valor na árvore
        self.root = self.insert(self.root, value)

    def delete_value(self, value):
        # Método público para deletar um valor da árvore
        self.root = self.delete(self.root, value)

    def search_value(self, value):
        # Método público para buscar um valor na árvore
        return self.search(self.root, value)


# Exemplo de uso:
if '__name__' == "__main__":
    tree = AVLTree()  # Cria uma nova árvore AVL
    tree.insert_value(10)  # Insere valores na árvore
    tree.insert_value(20)
    tree.insert_value(30)
    tree.insert_value(40)
    tree.insert_value(50)

    print("Tree after insertion:")
    
    # Função para percorrer a árvore em ordem e imprimir os valores
    def inorder_traversal(root):
        if root:
            inorder_traversal(root.left)  # Percorre o filho esquerdo
            print(root.value)  # Imprime o valor do nó
            inorder_traversal(root.right)  # Percorre o filho direito

    inorder_traversal(tree.root)  # Chama a função de percurso
    print()

    tree.delete_value(20)  # Deleta um valor da árvore
    print("Tree after deletion of 20:")
    inorder_traversal(tree.root)  # Chama a função de percurso novamente
    print()

    result = tree.search_value(30)  # Busca um valor na árvore
    if result:
        print("Node found")  # Se encontrado, imprime "Node found"
    else:
        print("Node not found")  # Se não encontrado, imprime "Node not found"