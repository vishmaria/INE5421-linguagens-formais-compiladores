""" Trabalho 1 - Minimização de Autômatos """

# Algoritmo para minimização de Autômatos Finitos Determinísticos.

"""Estrutura da entrada:
<número de estados>;<estado inicial>;{<estados finais>}; {<alfabeto>};<transições> 

Os estados são sempre identificados com letras maiúsculas. 
As transições são da forma:
 <estado origem>,<simbolo do alfabeto>,<estado destino>.
"""

import NFA
class Min:

    def __init__(self):
        self.states = 0
        self.initial = None
        self.final = None
        self.alphabet = None
        self.transitions = None
        self.nfa = NFA()
        self.dfa = None
        self.deterministic = True

    def input(self, input):
        lines = input.split(";")

        # Capturar e tratar exceções
        # (menos de 5 elementos, estados sem iniciar com letra maiúscula ou vazios):
        if len(lines) < 5:
            raise Exception("Entrada inválida! Insira mais elementos.")
        if not lines[1].isupper() or not lines[2].isupper():
            raise Exception("Estados devem ser letras maiúsculas!")
        # Estados/transições vazios:
        if not lines[0] or not lines[1] or not lines[2] or not lines[3] or not lines[4]:
            raise Exception("Really?")
        
        self.states = lines[0]
        self.initial = lines[1]
        # Separação dos estados finais conforme o padrão de entrada:
        self.final = lines[2].strip("{}").split(',')
        self.alphabet = lines[3].strip("{}").split(',')
        # As transições serão as últimas linhas da entrada:
        self.transitions = lines[4:]
    
    # Primeiro, deve-se verificar se o autômato é não determinístico ou determinístico.
    # Para isso, é necessário verificar se há transições para o mesmo estado com símbolos diferentes.

    def is_deterministic(self):
        # Verificar se há transições para o mesmo estado com símbolos diferentes:
        for transition in self.transitions:
            origin, symbol, destiny = transition.split(",")
            for other_transition in self.transitions:
                other_origin, other_symbol, other_destiny = other_transition.split(",")
                if origin == other_origin and symbol != other_symbol and destiny == other_destiny:
                    self.deterministic = False
                    self.dfa = self.nfa.determinize()
        return self.deterministic
