import pandas as pd
import lexema
import graphviz
import semantico

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
        self.line = None
        self.position = None
        self.children = []
        self.father = None
        self.type = None #Agregado para identificar tipos

# Cargar la tabla de análisis sintáctico
tabla = pd.read_csv("tabla4.csv", index_col=0)


# Inicializar la pila y el árbol
stack = []
symbol_E = NodeStack('GLOBAL', None)
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
    #c = 0
    while stack[-1].symbol != '$':
    #while c < 10:
        #print(entrada[0]["symbol"])
        if stack[-1].symbol == 'e':
            stack.pop()
        elif stack[-1].symbol == entrada[0]["symbol"]:
            nodo_hoja = find_node_by_id(root, stack[-1].id)
            nodo_hoja.lexeme = entrada[0]["lexeme"]
            nodo_hoja.line = entrada[0]["line"]
            nodo_hoja.position = entrada[0]["position"]
            if nodo_hoja.symbol == "NUM":
                nodo_hoja.type = "int"
            elif nodo_hoja.symbol == "DECM":
                nodo_hoja.type = "float"
            elif nodo_hoja.symbol == "BOOL":
                nodo_hoja.type = "bool"
            elif nodo_hoja.symbol == "CHAR":
                nodo_hoja.type = "char"
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
                        #print(nodo_nuevo.symbol)
                        nodo_resultante = find_node_by_id(root,nodo_padre.id)
                        if nodo_resultante:
                            print(f"Encontrado: ID={nodo_resultante.id}, Symbol={nodo_resultante.symbol}, Lexeme={nodo_resultante.lexeme}")
                        else:
                            print(f"No se encontró un nodo con ID={nodo_padre.id}")
                        nodo_resultante.children.append(nodo_nuevo_tree)
                        nodo_nuevo_tree.father = nodo_resultante
            except Exception as e:
                print("Error gramatical en la linea: " + entrada[0]["symbol"])
                break  # Sale del bucle en caso de error
        '''print("--------------")
        for b in range(len(stack)):
            print(stack[b].symbol)
        print("--------------")'''
        #c += 1
def find_node_by_id(node, target_id):
    if node.id == target_id:
        return node
    for child in node.children:
        result = find_node_by_id(child, target_id)
        if result:
            return result
    return None
        

def print_tree(node, depth=0):
    if node:
        # Imprimir el nodo actual con la indentación adecuada
        print("  " * depth + f"ID={node.id}, Symbol={node.symbol}, Lexeme={node.lexeme}")

        # Llamar a la función recursivamente para los hijos
        for child in node.children:
            print_tree(child, depth + 1)
def generate_tree_graph(root):
    dot = graphviz.Digraph(comment='Árbol de Análisis Sintáctico')
    
    def add_nodes(node):
        label = f"ID: {node.id}\nSymbol: {node.symbol}\nLexeme: {node.lexeme}"
        if not node.children:  #nodo hoja
            if node.line is not None:
                label += f"\nLine: {node.line}"
            if node.position is not None:
                label += f"\nPosition: {node.position}"
        
        if node.id == root.id:
            #celeste
            dot.node(str(node.id), label, style='filled', fillcolor='lightblue')
        elif not node.children:
            #verde
            dot.node(str(node.id), label, style='filled', fillcolor='lightgreen')
        else:
            #amarillo
            dot.node(str(node.id), label, style='filled', fillcolor='yellow')
        
        for child in reversed(node.children):
            dot.edge(str(node.id), str(child.id))
            add_nodes(child)
    
    add_nodes(root)
    dot.render('arbol', view=True)  # Generará un archivo 'arbol.pdf'

#_________________________________________#
#SEMANTICO

def busquedaGlobal(node):
    if node.symbol == "TYPE_FUNCTION" and node.children[-1].symbol == "TYPE_VOID": #BUSCA FUNCIONES VOID
        print("Se encontro FUNCTION_VOID")
        semantico.asignarFunctionVoid(node,Tabla)
        #crear una copia del nodo para ponerlo en tabla_funciones
        node_funcion = node
        #node_funcion.children.pop(0)
        Tabla_funciones.append(node_funcion)

        return node
    if node.symbol == "TYPE_FUNCTION" and node.children[-1].symbol == "TYPE": #BUSCA FUNCIONES
        print("Se encontro FUNCTION")
        semantico.asignarFunction(node,Tabla)
        node_funcion = node
        Tabla_funciones.append(node_funcion)
        return node
    if node.symbol == "VARIABLE": #BUSCAR VARIABLES
        print("Se encontro VARIABLE GLOBAL")
        semantico.asignarVariableGlobal(node,Tabla)
        return node
    for child in node.children:
        result = busquedaGlobal(child)
        if result:
            return result
    return None

#INICIAR MAIN

def busquedaKilla(node, num_id):
    if node.id != num_id:
        if node.symbol == "CALL_FUNCTION":
            print("SE ENCONTRO LLAMADO DE FUNCION")
            print(node.id)
            #return node
        if node.symbol == "VARIABLE_AMBIT":
            print("Se encontro VARIABLE - KILLA")
            print(node.id)
            semantico.asignarVariableKilla(node,Tabla)
            #return node
    for child in node.children:
        result = busquedaKilla(child,num_id)
        if result:
            return result
    return None

#TABLA es la Pila de simbolos
Tabla_funciones = []
Tabla = []
pilaCarlitos = []
#estoy usando casa como nodo actual
def buscarSimbolosGlobal(node):
    casa = node
    while casa != None:
        casa=busquedaGlobal(casa.children[0])

def buscarSimbolosKilla(node):
    casa = node
    num_id = 0
    while casa != None:
        casa=busquedaKilla(casa, num_id)
        if casa != None:
            num_id = casa.id

def ordenarTablaFunciones(tabla):
    for a in range(len(tabla)):
        tabla[a].children.pop(0)

def imprimir_ids(node):
    if node is not None:
        print(node.id)
        for child in reversed(node.children):
            imprimir_ids(child)

def postorden(node):
    if node is not None:
        for child in reversed(node.children):
            postorden(child)
        print(node.id)

def busqueda_Inicial(node):
    if node is not None:
        if node.symbol == "TYPE_FUNCTION" and node.children[-1].symbol == "TYPE_VOID": #BUSCA FUNCIONES VOID
            print("Se encontro FUNCTION_VOID")
            buscarTablaError(node)
            semantico.asignarFunctionVoid(node,Tabla)
        if node.symbol == "TYPE_FUNCTION" and node.children[-1].symbol == "TYPE": #BUSCA FUNCIONES
            print("Se encontro FUNCTION")
            buscarTablaError(node)
            semantico.asignarFunction(node,Tabla)
        if node.symbol == "VARIABLE": #BUSCAR VARIABLES
            print("Se encontro VARIABLE GLOBAL")
            buscarTablaError(node)
            semantico.asignarVariableGlobal(node,Tabla)
        #print(node.id)
        for child in reversed(node.children):
            busqueda_Inicial(child)

def busqueda_Inicial_Main(node):
    if node is not None and node.symbol != "GLOBAL":
        if node.symbol == "VARIABLE_AMBIT":
            print("Se encontro una variable killa")
            buscarTablaError(node)
            semantico.asignarVariableKilla(node,Tabla)
            #crear funcion, dependiendo el tipo
            cabecera.write("\nvar_"+node.children[-2].lexeme+":\t.word\t0:1")
        if node.symbol == "CALL_FUNCTION":
            print("Se detecto un llamado a una funcion")
            funcionActual = find_node_by_id(root,llamadoFuncion(node))
            print(funcionActual.id)
        if node.symbol == "LINE" and node.father.symbol == "LINECODE_AMBIT":
            if node.children[-1].children[-1].children[-1].children[-1].type == None:
                pilaCarlitos.append(buscarCopias(node.children[-1].children[-1].children[-1].children[-1].lexeme))
            else:
                pilaCarlitos.append(node.children[-1].children[-1].children[-1].children[-1].type)
            print(node.children[-1].children[-1].children[-1].children[-1].id)
            if node.children[-1].children[-1].children[-1].children[-1].symbol != "ID":
                asseExpresion(node.children[-1].children[-1].children[-1].children[-1])
            teoremaCarlitos(node)
            if node.father.father.children[-1].symbol == "OPER_ASI":
                tipoIdActual = node.father.father.father.children[-1].children[-1].lexeme
                print("----------------------------------------------")
                print(tipoIdActual)
                #llamar funcion ASSEACTUALIZAR VARIABLE, para guardar variable
                asseAsignar(node.father.father.father.children[-2].lexeme)
                verificarTipos(tipoIdActual,pilaCarlitos.pop())
            #otra funcion
        if node.symbol == "IF":
            print("SE DETECTO UN IFFFFFFFFFFFFFFF")
            #cuerpo.write("\nIFFFFFFFFFFFFFF")
            #primer parametro
            if node.father.children[-3].children[-1].children[-1].symbol == "ID":
                ifVariable(node.father.children[-3].children[-1].children[-1])
            elif node.father.children[-3].children[-1].children[-1].symbol == "NUM":
                ifNumero(node.father.children[-3].children[-1].children[-1])
            #push
            cuerpo.write("\nsw $a0, 0($sp)\nadd $sp, $sp, -4")
            #segundo parametro
            if node.father.children[-3].children[-3].children[-1].symbol == "ID":
                ifVariable(node.father.children[-3].children[-3].children[-1])
            elif node.father.children[-3].children[-3].children[-1].symbol == "NUM":
                ifNumero(node.father.children[-3].children[-3].children[-1])
            #comparacion
            cuerpo.write("\nlw $t1, 4($sp)\nadd $sp, $sp, 4")
            ifComparador(node.father.children[-3].children[-2].children[-1])
            #cuerpo.write("\nFin del IF\n")

            cuerpo.write("\n\nlabel_true:")
        if node.symbol =="IF_ELSE":
            print("SE ENCONTROOOO IF_ELSE")
            cuerpo.write("b label_end\n\nlabel_false:")
        if node.symbol == "LINECODE_AMBIT" and node.father.father.children[1].symbol == "IF_ELSE":
            print("CERRAMOS ELSE")
            cuerpo.write("\nlabel_end:")
        for child in reversed(node.children):
            busqueda_Inicial_Main(child)
def ifComparador(node):
    if node.symbol == "OPER_MYQ":
        print("EL COMPARADOR ES MAYOR QUE")
        cuerpo.write("\nbgt $a0, $t1, label_false")
    elif node.symbol == "OPER_MNQ":
        print("EL COMPARADOR ES MENOR QUE")
        cuerpo.write("\nblt $a0, $t1, label_false")
    elif node.symbol == "OPER_MYI":
        print("EL COMPARADOR ES MAYOR IGUAL QUE")
        cuerpo.write("\nbge $a0, $t1, label_false")
    elif node.symbol == "OPER_MNI":
        print("EL COMPARADOR ES MENOR IGUAL QUE")
        cuerpo.write("\nble $a0, $t1, label_false")
    elif node.symbol == "OPER_IQL":
        print("EL COMPARADOR ES IGUAL QUE")
        cuerpo.write("\nbne $a0, $t1, label_false")
    elif node.symbol == "OPER_DIF":
        print("EL COMPARADOR ES DIFERENTE QUE")
        cuerpo.write("\nbeq $a0, $t1, label_false")
def ifVariable(node):
    print("Se encontro VARIABLE IFFFFFFF")
    cuerpo.write("\nla $t0, var_"+node.lexeme)
    cuerpo.write("\nlw $a0, 0($t0)")

def ifNumero(node):
    print("Se encontro NUMERO IFFFFFFFFF")
    cuerpo.write("\nli $a0, "+str(node.lexeme))
#BUSCAR FUNCION MAIN "KILLA()"
def buscarMain(node):
    if node.symbol == "START_KILLA":
        return node
    for child in reversed(node.children):
        result = buscarMain(child)
        if result:
            return result
    #print("NO SE CUENTA CON MAIN")
    return None

def separarMain(node):
    mainKilla = buscarMain(node)
    if mainKilla != None:
        print("Existe un main")
        #conMainKilla = mainKilla.children.pop(0)
        #generate_tree_graph(mainKilla)
        return mainKilla
    else:
        print("No existe el main")
        exit(1)

def buscarCopias(nombre):
    for a in range(len(Tabla)):
        if Tabla[a]['Nombre'] == nombre:
            return Tabla[a]['Tipo']
        else:
            print("VARIABLE NO DEFINIDA")
            exit(0)


def teoremaCarlitos(node):
    if node is not None:
        if node.symbol == "VALUE" and node.father.father.father.father.symbol != "LINECODE_AMBIT" and node.children[-1].symbol != "ID":
            print("se encontro un VALUE")
            print(node.children[0].lexeme)
            print(node.children[0].type)
            operador = node.father.father.father.father.children[-1].children[-1].lexeme #auxiliar
            print("dato 1:",pilaCarlitos[-1])
            print("dato 2:",node.children[0].type)
            print("operador:",operador)
            if operador != "=":
                asseOperacion(node.children[0],operador)
                pilaCarlitos.append(verificarTipos(pilaCarlitos.pop(),node.children[0].type,operador))
                print("resultado:",pilaCarlitos[-1])
                #pilaCarlitos.append(node.children[0])
            else:
                asseExpresion(node.children[0])
        for child in reversed(node.children):
            teoremaCarlitos(child)

def asseAsignar(nombre):
    cabecera.write("\nout_var_"+nombre+": .asciiz \"\\n"+nombre+" = \"")
    cuerpo.write("\nla $t0, var_"+nombre+"\nsw $a0, 0($t0)")
    cuerpo.write("\nli $v0, 4\nla $a0, out_var_"+nombre+"\nsyscall")
    cuerpo.write("\nla $t0, var_"+nombre+"\nlw $a0, 0($t0)")
    cuerpo.write("\nli $v0, 1\nsyscall\n\n")

def asseOperacion(node, operador):
    if operador == "+":
        cuerpo.write("\nsw $a0 0($sp)\naddiu $sp $sp-4")
        asseExpresion(node)
        cuerpo.write("\nlw $t1 4($sp)\nadd $a0 $t1 $a0\naddiu $sp $sp 4")
    elif operador == "-":
        cuerpo.write("\nsw $a0 0($sp)\naddiu $sp $sp-4")
        asseExpresion(node)
        cuerpo.write("\nlw $t1 4($sp)\nsub $a0 $t1 $a0\naddiu $sp $sp 4")
    elif operador == "*":
        cuerpo.write("\nsw $a0 0($sp)\naddiu $sp $sp-4")
        asseExpresion(node)
        cuerpo.write("\nlw $t1 4($sp)\nmul $a0 $t1 $a0\naddiu $sp $sp 4")
    elif operador == "/":
        cuerpo.write("\nsw $a0 0($sp)\naddiu $sp $sp-4")
        asseExpresion(node)
        cuerpo.write("\nlw $t1 4($sp)\ndiv $a0 $t1 $a0\naddiu $sp $sp 4")
    else:
        print("Operador no soportado: {}".format(operador))
        exit(1)


def verificarTipos(tipo1, tipo2, operador = '='):
    print("recibe1:",tipo1)
    print("recibe2:",tipo2)
    reglas_inferencia_aritmetica = {
        ('int', 'float'): 'float',
        ('float', 'int'): 'float',
        ('int', 'int'): 'int',
        ('float', 'float'): 'float',
    }
    valores_comprobar = [
        'int','float','bool','char'
    ]

    if operador in {'+', '-', '*', '/', '='}:
        if tipo1 not in valores_comprobar or tipo2 not in valores_comprobar:
            print("error papi")
            return None
        return reglas_inferencia_aritmetica[(tipo1, tipo2)]
    print("Imcompatibilidad de tipos")
    exit(1)

def llamadoFuncion(node):
    print(node.father.father.children[-1].lexeme)
    for a in range(len(Tabla)):
        if Tabla[a]['Flag'] == "FUNCTION":
            if node.father.father.children[-1].lexeme == Tabla[a]['Nombre']:
                print("Si existe la funcion")
                return Tabla[a]['ID']
    print("La funcion no esta declarada")
    exit(1)
#IMPRIMIR LA TABLA
def imprimirTabla():
    print("ID:  Tipo:   Nombre: Ambito: Flag:   ")
    for a in range(len(Tabla)):
        print(Tabla[a])
#Compara y detecta similitudes con el hijo [-2]
def buscarTablaError(node):
    #print("Se esta buscando una similitud en la tabla")
    for a in range(len(Tabla)):
        if node.children[-2].lexeme == Tabla[a]['Nombre']:
            print(Tabla[a]['Nombre']+" Ya esta declarado en el ambito "+Tabla[a]['Ambito'])
            exit(1)
#_----------------------------------------
#GENERACION DE CODIGO
def asseExpresion(nodo):
    if nodo.symbol == "NUM":
        cuerpo.write("\nli $a0,"+str(nodo.lexeme))
    elif nodo.symbol == "ID":
        cuerpo.write("\nla $t0, var_"+nodo.lexeme+"\nlw $a0, 0($t0)")

def fusionar_archivos(archivo1, archivo2, archivo_salida):
    with open(archivo1, 'r') as f1, open(archivo2, 'r') as f2:
        contenido1 = f1.read()
        contenido2 = f2.read()

    # Combina el contenido de ambos archivos
    contenido_combinado = contenido1 + contenido2

    # Escribe el contenido combinado en un nuevo archivo o en uno de los archivos originales
    with open(archivo_salida, 'w') as fsalida:
        fsalida.write(contenido_combinado)
# Archivo1.py
cabecera = open("cabecera.txt", "w")
cabecera.write(".data")
# Archivo2.py
cuerpo = open("cuerpo.txt", "w")
cuerpo.write("\n.text\nmain:\n")

#EJECUCIONES PRINCIPALES
analizar2()
generate_tree_graph(root)
busqueda_Inicial(root)
imprimirTabla()
mainPrincipal = separarMain(root)
busqueda_Inicial_Main(mainPrincipal)
imprimirTabla()
cuerpo.write("\njr $ra")
#TERMINAR
cabecera.close()
cuerpo.close()
fusionar_archivos("cabecera.txt","cuerpo.txt","salida.txt")
