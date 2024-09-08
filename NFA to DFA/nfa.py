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
        self.all_states = None

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

        self.all_states = set()
        for transition in self.transitions:
            origin, symbol, destiny = transition.split(",")
            self.all_states.add(origin)
            self.all_states.add(destiny)

            # Evita que símbolos sejam lidos como estados:
            if symbol not in self.alphabet:
                self.alphabet.append(symbol)

    # Getter do destino de uma transicao:
    def get_destiny(self, state, symbol):
        destiny = set()
        for state in self.all_states:
            for transition in self.transitions:
                org, symb, dest = transition.split(",")
                if org == state and symb == symbol:
                    destiny.add(dest)
        return destiny



    # Episilon closure = conjunto de estados que podem ser alcançados somente por epsilon
    def epsilon_closure(self, state, visited=None):

        if visited is None:
            visited = set()

        state = frozenset(state) 
        if state in visited:
            return set()
        visited.add(state)

        epsilon_closure = {state}
        for transition in self.transitions:
            origin, symbol, destiny = transition.split(",")
            if symbol == "&" and origin in state:
                epsilon_destiny = self.epsilon_closure(destiny, visited)
                epsilon_closure |= epsilon_destiny

        return epsilon_closure



    def determinize(self):
        det_transitions = set()

        if '&' in self.alphabet:
            self.epsilon = True
            begin_closure = self.epsilon_closure(self.initial)
            aux_set = set()
            for conjunto in begin_closure:
                for subset in conjunto:
                    for item in subset:
                        aux_set.add(item)
            estado_novo=""
            for item in aux_set:
                estado_novo+=str(item)
            
            self.all_states.add(estado_novo)
        else:
            begin_closure = {self.initial}

        states_to_check = [begin_closure]
        states_checked = set()
        final_states = set()

        while states_to_check:
            current = states_to_check.pop(0)
            states_checked.add(tuple(current))

            for symbol in self.alphabet:
                if symbol == '&':
                    continue

                destiny = set()
                for state in current:
                    destiny.update(self.get_destiny(state, symbol))
                e_destiny = self.epsilon_closure(destiny) if self.epsilon else destiny

                if e_destiny and tuple(e_destiny) not in states_checked and e_destiny not in states_to_check: 
                    states_to_check.append(e_destiny)

                if e_destiny:
                    #O PROBLEMA: Está adicionando transições mesmo não checando se os estados origem tem qualquer transição com symbol
                    for state in current:
                        if str(str(list(state)[0])+","+str(symbol)+","+str(list(list(e_destiny)[0])[0])) in self.transitions:
                            det_transitions.add((frozenset(current), symbol, frozenset(e_destiny)))

                    for state in e_destiny:
                        
                        if state in self.final:
                            final_states.add(tuple(current)) 


        for state in states_checked:
            if any(s in self.final for s in state):
                final_states.add(state)

        format_final = ','.join(sorted(''.join(state) for state in final_states))

        format_state = ''.join(sorted(''.join(state) for state in begin_closure))
        format_alphabet = '{{' + '},{'.join(set(self.alphabet) - {'&'}) + '}}' 

        format_transitions = []
        for st, symb, nxt in det_transitions:
            format_transitions.append(f'{"".join(sorted("".join(state) for state in st))},{symb},{"".join(sorted("".join(state) for state in nxt))}')

        format_transitions.sort() 
        output = f'{len(states_checked)};{format_state};{{{format_final}}};{format_alphabet};{";".join(format_transitions)}\n'

        return output.strip()

