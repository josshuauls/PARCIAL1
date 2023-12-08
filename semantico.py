
Tabla = []
def asignarFunction(node,Tabla):
    simbolo={
        "ID": node.id,
        "Tipo":node.children[-1].children[0].symbol,
        "Nombre":node.children[-2].lexeme,
        "Ambito":node.father.father.symbol,
        "Flag":"FUNCTION"
    }
    Tabla.append(simbolo)

def asignarFunctionVoid(node,Tabla):
    simbolo={
        "ID": node.id,
        "Tipo":node.children[-1].symbol,
        "Nombre":node.children[-2].lexeme,
        "Ambito":"GLOBAL",
        "Flag":"FUNCTION"
    }
    Tabla.append(simbolo)

def asignarVariableGlobal(node,Tabla):
    simbolo={
        "ID": node.id,
        "Tipo":node.children[-1].children[0].lexeme, #estoy modificando symbol por lexema
        "Nombre":node.children[-2].lexeme,
        "Ambito":"GLOBAL",
        "Flag":"VARIABLE"
    }
    Tabla.append(simbolo)

# AMBITO MAIN -> KILLA

def asignarVariableKilla(node,Tabla):
    simbolo={
        "ID": node.id,
        "Tipo": node.children[-1].children[0].lexeme, #estoy modificando symbol por lexema
        "Nombre": node.children[-2].lexeme,
        "Ambito":"KILLA",
        "Flag":"VARIABLE"
    }
    Tabla.append(simbolo)