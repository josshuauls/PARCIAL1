import ply.lex as lex
import sys
def ejecutar_lexema():
  reserved = {
    'int' : 'TYPE_INT',
    'float' : 'TYPE_FLOAT',
    'bool' : 'TYPE_BOOL',
    'char' : 'TYPE_CHAR',
    'void' : 'TYPE_VOID',
    'print' : 'PRINT',
    'read' : 'READ',
    'return' : 'RETURN',
    'for' : 'FOR',
    'while' : 'WHILE',
    'if' : 'IF',
    'else' : 'ELSE',
    'killa' : 'KILLA',
    'false' : 'BOOL',
    'true' : 'BOOL'
  }

  tokens = ['NUM','DECM','ID',
            'COMMA', 'ENDLINE',
            'OPER_ASI','OPER_ADD','OPER_SUB','OPER_MUL','OPER_DIV','OPER_MOD',
            'OPER_AND','OPER_OR',
            'OPER_MYQ','OPER_MNQ','OPER_MYI','OPER_MNI','OPER_IQL','OPER_DIF',
            'PARENT_OP','PARENT_CL','KEY_OP','KEY_CL','SQUARE_OP','SQUARE_CL',
            'COMMET_SIM','COMMET_COM',
            'LITERAL','CHAR']+list(reserved.values())

  t_OPER_ASI = r'\='
  t_OPER_ADD = r'\+'
  t_OPER_SUB = r'-'
  t_OPER_MUL = r'\*'
  t_OPER_DIV = r'/'
  t_OPER_MOD = r'\%'
  t_OPER_AND = r'\&'
  t_OPER_OR = r'\|'

  t_OPER_MYQ = r'>'
  t_OPER_MNQ = r'<'
  t_OPER_MYI = r'>='
  t_OPER_MNI = r'<='
  t_OPER_IQL = r'\=\='
  t_OPER_DIF = r'!='

  t_PARENT_OP = r'\('
  t_PARENT_CL = r'\)'
  t_KEY_OP = r'\{'
  t_KEY_CL = r'\}'
  t_SQUARE_OP = r'\['
  t_SQUARE_CL = r'\]'

  t_COMMET_SIM = r'//.*'
  t_COMMET_COM = r'///.*///'
  t_LITERAL = r'".*"'
  t_CHAR = r"'.'"

  t_COMMA = r','
  t_ENDLINE = r';'


  def t_DECM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
  def t_ID(t):
    r'([a-zA-Z]|ñ|Ñ|\_)([a-zA-Z]|[0-9]|ñ|Ñ|\_)*'
    t.type = reserved.get(t.value,'ID')
    return t
  def t_NUM(t):
    r'\d+'
    t.value = int(t.value) # guardamos el valor del lexema
    return t

  def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  t_ignore = ' \t'

  def t_error(t):
    print(f"Error lexico linea: {t.lineno}, posicion: {t.lexpos}, caracter: '%s'" % t.value[0])
    sys.exit(1)


  lexer = lex.lex()


  with open('archivo2.txt','r',encoding='utf-8') as archivo:
    data = archivo.read()
  #data = ''' maypi hamuy kunan chaypi kancha lliqlla wañuchiy wakchaq quilway ñawi qillqay'''

  lexer.input(data)

  with open('lexema.txt', 'w', encoding='utf-8') as output_file:
    entrada_lexema = []
    while True:
      tok = lexer.token()
      if not tok:
        break # No more input
      if tok.type == 'ERROR':
        print("Cadena Incorrecta")
        break
      output_file.write(f'{{"symbol": "{tok.type}", "lexeme": "{tok.value}", "line": {tok.lineno}, "position": {tok.lexpos}}},\n')
      entrada_lexema.append({"symbol": tok.type, "lexeme": tok.value, "line": tok.lineno, "position": tok.lexpos})
    output_file.write(f'{{"symbol": "$", "lexeme": "$"}},')
    entrada_lexema.append({"symbol": "$", "lexeme": "$"})
    return entrada_lexema
    print("Se ejecuto correctamente")

print(ejecutar_lexema()[0])
print("Se ejecuto correctamente")