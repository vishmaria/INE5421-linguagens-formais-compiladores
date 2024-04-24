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
                self.epsilon = True
                # Abordagem recursiva para encontrar todos os estados alcançáveis por epsilon
                epsilon_closure |= self.epsilon_closure(destiny,visited)
                
        return epsilon_closure


nfa = NFA()
nfa.input("2;A;{B};{a};A,&,A")


nfa1 = NFA()
nfa1.input("3;A;{C};{a,b};A,&,A;A,a,B")


nfa2 = NFA()
nfa2.input("3;A;{C};{a,b};A,&,A;B,&,C")

nfa3 = NFA()
nfa3.input("3;A;{C};{a,b};A,a,B")
