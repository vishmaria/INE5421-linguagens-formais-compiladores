# Assume que já foi minimizado com o método determinize() da classe NFA.

class DFA:
    def __init__(self):
        self.n_states = 0
        self.initial = None
        self.final = None
        self.alphabet = None
        self.transitions = None
        self.states_list = None

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
        
        self.n_states = lines[0]
        self.initial = lines[1]
        # Separação dos estados finais conforme o padrão de entrada:
        self.final = lines[2].strip("{}").split(',')
        self.alphabet = lines[3].strip("{}").split(',')
        # As transições serão as últimas linhas da entrada:
        self.transitions = lines[4:]

        self.states_list = set()
        for transition in self.transitions:
            origin, symbol, destiny = transition.split(",")
            self.states_list.add(origin)
            self.states_list.add(destiny)

            # Evita que símbolos sejam lidos como estados:
            if symbol not in self.alphabet:
                self.alphabet.append(symbol)

