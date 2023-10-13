import pandas as pd
import lexema

count = 0

class NodeStack:
    def __init__(self, symbol, lexeme):
        global count
        self.symbol = symbol
        self.lexeme = lexeme
        self.id = count + 1
        count += 1

class NodeTree:
    def __init__(self, id, symbol, lexeme):
        self.id = id
        self.symbol = symbol
        self.lexeme = lexeme
        self.children = []
        self.father = None

# Cargar la tabla de análisis sintáctico
tabla = pd.read_csv("tabla1.csv", index_col=0)

# Inicializar la pila y el árbol
stack = []
symbol_E = NodeStack('START_KILLA', None)
symbol_dollar = NodeStack('$', None)

stack.append(symbol_dollar)
stack.append(symbol_E)
root = NodeTree(symbol_E.id, symbol_E.symbol, symbol_E.lexeme)

# Entrada de prueba
'''entrada = [
    {"symbol": "ID", "lexeme": "4"},
    {"symbol": "OPER_ADD", "lexeme": "*"},
    {"symbol": "ID", "lexeme": "5"},
    {"symbol": "ENDLINE", "lexeme": "5"},
    {"symbol": "$", "lexeme": "$"},
]'''

entrada = lexema.ejecutar_lexema()

def analizar2():
    while stack[-1].symbol != '$':
        print(entrada[0]["symbol"])
        if stack[-1].symbol == 'e':
            stack.pop()
        elif stack[-1].symbol == entrada[0]["symbol"]:
            stack.pop()
            entrada.pop(0)
        else:
            try:
                produccion = tabla.loc[stack[-1].symbol, entrada[0]["symbol"]]
                produccion = produccion.split()
                nodo_padre = stack.pop()
                produccion = produccion[::-1] #sirve para voltear los valores de la produccion
                for b in range(len(produccion)):
                    if produccion[b] != " ":
                        nodo_nuevo = NodeStack(produccion[b], None)
                        nodo_nuevo_tree = NodeTree(nodo_nuevo.id, nodo_nuevo.symbol, nodo_nuevo.lexeme)
                        stack.append(nodo_nuevo)
                        root.children.append(nodo_nuevo_tree)
                        print(nodo_nuevo.symbol)
            except Exception as e:
                print("Error gramatical en la linea: " + entrada[0]["symbol"])
                break  # Sale del bucle en caso de error
        print("--------------")
        for b in range(len(stack)):
            print(stack[b].symbol)
        print("--------------")


analizar2()
