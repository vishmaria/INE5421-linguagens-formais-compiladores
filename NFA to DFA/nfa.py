""" Trabalho 1 - Determinização de Autômatos """

# Algoritmos para determinização com e sem épsilon(&) de Autômatos Finitos Determinísticos.

"""Estrutura da entrada:
<número de estados>;<estado inicial>;{<estados finais>}; {<alfabeto>};<transições> 
Os estados são sempre identificados com letras maiúsculas.
As transições são da forma <estado origem>,<simbolo do alfabeto>,<estado destino>."""

"""Estrutura da saída:
<número de estados>;<estado inicial>;{<estados finais>}; """

class NFA:
    def __init__(self):
        self.states = 0
        self.initial = None
        self.final = None
        self.alphabet = None
        self.transitions =  None
        # Atributo para verificar se há transição por epsilon, inicilamente falso:
        self.epsilon = False

    def input(self, input):
        # Recebe a entrada e separa os elementos:
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

        all_states = set()
        for transition in self.transitions:
            origin, symbol, destiny = transition.split(",")
            all_states.add(origin)
            all_states.add(destiny)

            # Evita que símbolos sejam lidos como estados:
            if symbol not in self.alphabet:
                self.alphabet.append(symbol)

        # Calcular epsilon fecho para cada estado:, por conta da abordagem recursiva:
        epsilon_closures = {}
        for state in all_states:
            epsilon_closures[state] = self.epsilon_closure(state)

    # Getter do destino de uma transicao:
    def get_destiny(self, state, symbol):
        destiny = set()
        for state in self.states:
            for transition in self.transitions:
                org, symb, dest = transition.split(",")
                if org == state and symb == symbol:
                    destiny.add(dest)
        return destiny



    # Episilon closure = conjunto de estados que podem ser alcançados somente por epsilon
    def epsilon_closure(self, state,visited=None):
        if visited is None:
            visited = set()

        if state in visited:
            return set()

        visited.add(frozenset(state))

        epsilon_closure = {frozenset(state)}
        for transition in self.transitions:
            origin, symbol, destiny = transition.split(",")
            if symbol == "&" and origin in state:
                epsilon_closure |= self.epsilon_closure(destiny, visited)

        return epsilon_closure
    
    # Método para determinizar o autômato:
def determinize(self):
    det_transitions = set()

    if '&' in self.alphabet:
        self.epsilon = True
        begin_closure = self.epsilon_closure(self.initial)
    else:
        begin_closure = {self.initial}

    states_to_check = [begin_closure]
    states_checked = set()

    while states_to_check:
        current = states_to_check.pop(0)
        states_checked.add(tuple(current))

        for symbol in self.alphabet:
            destiny = set()
            for state in current:
                destiny.update(self.get_destiny(state, symbol))
            e_destiny = self.epsilon_closure(destiny) if self.epsilon else destiny

            if e_destiny and tuple(e_destiny) not in states_checked:
                states_to_check.append(e_destiny)

            det_transitions.add((frozenset(current), symbol, frozenset(e_destiny)))

    det_accept = set()
    for state in states_checked:
        if any(s in self.final for s in state):
            det_accept.add(state)

    format_state = '{{' + '},{'.join(''.join(sorted(state)) for state in det_accept) + '}}'
    format_alphabet = '{{' + '},{'.join(self.alphabet) + '}}'

    format_transitions = []
    for st, symb, nxt in det_transitions:
        format_transitions.append(f'{{{",".join(sorted("".join(state) for state in st))}}},{symb},{{{",".join(sorted("".join(state) for state in nxt))}}}')

    format_transitions = sorted(format_transitions, key=lambda x: (x.split(',')[0].replace('{', '').replace('}', ''), 
                                                                   x.split(',')[1].replace('{','').replace('}','') ))

    if self.epsilon:
        self.alphabet.remove('&')

    output = f'{len(states_checked)};{format_state};{format_alphabet};'
    for transition in format_transitions:
        output += f'{transition}\n'
    return output.strip()
