import graphviz
import third_problem as infixToPostfix

class Node:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None

    def __str__(self):
        return f'{self.value}, {self.right}, {self.left}'

def createTree(postfix):
    stack = []
    for character in postfix:
        if character.isalnum():
            stack.append(Node(character))
        elif character in '?*+':
            treeNode = Node(character)
            treeNode.right = stack.pop()
            stack.append(treeNode)
        elif character in '|¬':
            treeNode = Node(character)
            treeNode.right = stack.pop()
            treeNode.left = stack.pop()
            stack.append(treeNode)
    return stack[0]

def createGraph(tree, filename):
    dot = graphviz.Digraph(comment="Árbol Sintáctico")

    def addNodesEdges(node, counter):
        dot.node(f'node{counter}', f'{node.value}')
        current = counter
        if node.left:
            leftCounter = counter * 2
            dot.edge(f'node{current}', f'node{leftCounter}')
            addNodesEdges(node.left, leftCounter)
        if node.right:
            rightCounter = counter * 2 + 1
            dot.edge(f'node{current}', f'node{rightCounter}')
            addNodesEdges(node.right, rightCounter)

    addNodesEdges(tree, 1)
    dot.render(f'pdf/{filename}', format='pdf', cleanup=True)

with open("regex.txt", "r", encoding="UTF-8") as file:
    expressions = file.readlines()

for i, expression in enumerate(expressions):
    expression = expression.strip()
    if expression:
        postfixExpressions = infixToPostfix.infixToPostfix(expression)
        for postfixExpression in postfixExpressions:
            syntaxTree = createTree(postfixExpression)

        filename = f"syntaxTree{i+1}.gv"
        createGraph(syntaxTree, filename)