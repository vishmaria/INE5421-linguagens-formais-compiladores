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

    # Getter do destino de uma trasnicao:
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
        # Inicialmente, o epsilon_closure é um set vazio (set é utilizado para evitar repetições)
        if visited is None:
            visited = set()

        # Verificar se estado já teve o epsilon_closure calculado para evitar loops infinitos
        if state in visited:
            return set()

        visited.add(state)

        epsilon_closure = {state}
        # Percorrer todas as transições para encontrar estados alcançáveis por epsilon
        for transition in self.transitions:

            # Separar os elementos da transição
            origin, symbol, destiny = transition.split(",")

            # Se o símbolo for epsilon, adicionar o estado ao epsilon_closure
            if symbol == "&" and origin == state:
                # Abordagem recursiva para encontrar todos os estados alcançáveis por epsilon
                epsilon_closure |= self.epsilon_closure(destiny,visited)

        return epsilon_closure
    
    # Método para determinizar o autômato:
    def determinize(self):
        # Primiero passo é iniciar um conjunto de transições do novo automato:
        det_transitions = set()

        # Verificar se há epsilon-transição para não chamar o método desnecessariamnete:
        if '&' in self.alphabet:
            self.epsilon = True
            begin_closure = self.epsilon_closure(self.initial)
        else:
            # Se não houver transição por epsilon, o estado inicial continua o mesmo
            begin_closure = {self.initial}

        # Ordenar os estados que vão ser verificados e os que já foram verificados:
        states_to_check = [begin_closure]
        states_checked = set()

        # Enquanto houver estados a serem verificados:
        while states_to_check:
            current = states_to_check.pop(0)
            states_checked.add(tuple(current))

            for symbol in self.alphabet:
                # Calcular estados-destino para os dois caos
                # Primeiro caso: se não houver transição por epsilon
                if not self.epsilon:
                    # Iniciar um conjunto vazio para os estados alcançáveis
                    destiny = set()

                    # Para cada estado do conjunto atual:
                    for state in current:
                        destiny.update(self.get_destiny(state, symbol))
                # Segundo caso: se houver transição por epsilon
                e_destiny = self.epsilon_closure(destiny) if self.epsilon else destiny

                if e_destiny and tuple(e_destiny) not in states_checked:
                    states_to_check.append(e_destiny)

                det_transitions.add((set(current), symbol, set(e_destiny)))
        # Agora, vamos calcular os estados de aceitação.
        #  O conjunto de estados finais de um DFA equivalente ao NFA é o conjunto
        # de  estados intermediários que contém pelo menos um estado de aceitação do NFA original.

        det_accept = set()
        for state in states_checked:
            if any(s in self.final for s in state):
                det_accept.add(''.join(sorted(state)))

        format_state = '{{' + '},{'.join(sorted(det_accept)) + '}}'

        # Cálculo das transições do DFA:
        format_transitions = []
        for st, symb, nxt in det_transitions:
            format_transitions.append(f'{"".join(sorted(st))},{symb},{"".join(sorted(nxt))}')

        # Ajustar a formatação das transições
        format_transitions = sorted(format_transitions, key=lambda x: (x.split(',')[0].replace('{', '').replace('}', ''), 
                                                                       x.split(',')[1].replace('{','').replace('}','') ))

        # Ajustar o alfabeto:
        if self.epsilon:
            self.alphabet.remove('&')

        # Saída no padrão <número de estados>;<estado inicial>;{<estados finais>};
        output =  f'{len(states_checked)};{"".join(sorted(begin_closure))};{format_state};'
        return output

