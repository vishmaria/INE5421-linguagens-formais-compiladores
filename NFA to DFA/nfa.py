""" Trabalho 1 - Determinização de Autômatos """

# Algoritmos para determinização com e sem épsilon(&) de Autômatos Finitos Determinísticos.

"""Estrutura da entrada:
<número de estados>;<estado inicial>;{<estados finais>}; {<alfabeto>};<transições> 
Os estados são sempre identificados com letras maiúsculas.
As transições são da forma <estado origem>,<simbolo do alfabeto>,<estado destino>."""

"""Estrutura da saída:
<número de estados>;<estado inicial>;{<estados finais>}; """

class NFA:
    def __init__(self, nfa,states, initial, final, alphabet, transitions, epsilon=False):
        self.nfa = nfa
        self.states = states
        self.initial = initial
        self.final = final
        self.alphabet = alphabet
        self.transitions = transitions
        # Atributo para verificar se há transição por epsilon, inicilamente falso:
        self.epsilon = epsilon

    def input(self, input):
        # Recebe a entrada e separa os elementos:
        lines = input.split(";")

        # Capturar e tratar exceções
        # (menos de 5 elementos, estados sem iniciar com letra maiúscula ou vazios):
        if len(lines) < 5:
            raise Exception("Entrada inválida! Insira mais elementos.")
        if not lines[0].isupper():
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

    # Episilon closure = conjunto de estados que podem ser alcançados somente por epsilon
    def epsilon_closure(self):
        self.epsilon = True
        # Inicialmente, o epsilon_closure é uma lista vazia
        epsilon_closure = []
        # Novos estados intermediários:
        new_states = []
        for transition in self.transitions:
            # Separação dos elementos da transição:
            origin, symbol, destiny = transition.split(",")
            # Se o símbolo for epsilon, adiciona o estado ao epsilon_closure:
            if symbol == "&":
                if origin not in epsilon_closure:
                    new_states.append(destiny)

            if new_states == epsilon_closure:
                break
            epsilon_closure = new_states.copy()

        return sorted(epsilon_closure)



        
