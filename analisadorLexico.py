# Analisador Lexico (ex 01)
from typing import NamedTuple
import re

class Token(NamedTuple):
    tipo:str
    valor: str
    linha: int
    coluna: int

def tokens_codigo(codigo):
    palavraChave = {'IF', 'ELSE','WHILE', 'RETURN'}
    token_esp = [
        ('NUM', r'\d+(\.\d*)?'), #Numero INteiro ou decimal
        ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'), #identificador
        ('OP', r'[+\-*/]'), #operador aritmetico
        ('NEWLINE', r'\n'), #Fim de linha
        ('SKIP', r'[ \t]+'), #Pulo sobre espaços e tabs
        ('AP', r'\('), #abre parentheses
        ('FP', r'\)'), #fecha parenteses
        ('EQ', r':='), #igual
        ('COMENTARIO', r'//.*'),
        ('SL', r'"[^"]*"'),
        ('OA', r'[\+=\-=\*=\/=]'),
        ('OR', r'[==\!=\<\>\<=\>=]')
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_esp)
    numero_linha = 1
    linha_comeco = 0
    for mo in re.finditer(tok_regex, codigo):
        tipo = mo.lastgroup
        valor = mo.group()
        coluna = mo.start() - linha_comeco
        if tipo == 'NUM':
            valor = int(valor)
        elif tipo == 'ID' and valor in palavraChave:
            tipo = 'PC'
        elif tipo == 'NEWLINE':
            linha_comeco = mo.end()
            numero_linha += 1
            continue
        elif tipo == 'SKIP':
            continue
        yield Token(tipo, valor, numero_linha, coluna)

codigo = '''
    valor >= 2
'''

for token in tokens_codigo(codigo):
    print(token)