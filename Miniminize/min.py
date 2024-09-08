""" Trabalho 1 - Minimização de Autômatos """

# Algoritmo para minimização de Autômatos Finitos Determinísticos.

"""Estrutura da entrada:
<número de estados>;<estado inicial>;{<estados finais>}; {<alfabeto>};<transições> 

Os estados são sempre identificados com letras maiúsculas. 
As transições são da forma:
 <estado origem>,<simbolo do alfabeto>,<estado destino>.
"""
from dfa import DFA
class Min:

    def __init__(self):
        self.n_states = 0
        self.initial = None
        self.final = None
        self.alphabet = None
        self.transitions = None
        self.dfa = DFA()
        self.dfa_states = self.dfa.states_list
        self.all_states = None


    def input(self, input):
        self.dfa.input(input)

    # Primeiro passo: verificar estados inalcançáveis
    def delete_unreachable(self, initial):
        old_states = set()
        for t in self.dfa.transitions:
            org,_,_ = t.split(",")
            old_states.add(org)
        
        reachable = set()
        states_stack = [initial]

        while states_stack:
            state = states_stack.pop()
            if state not in reachable:
                reachable.add(state)
                for s in self.dfa.alphabet:
                    next_state = None
                    for transition in self.dfa.transitions:
                        temp = transition.split(",")
                        if temp[0] == state and temp[1] == s:
                            next_state = temp[2]
                            states_stack.append(next_state)
                            break
            
        unreachable = old_states - reachable

        for state in unreachable:
            self.dfa.states_list.remove(state)
        
        self.n_states = int(self.dfa.n_states) - len(unreachable)
        self.initial = initial
        self.dfa.final = [state for state in self.dfa.final if state not in unreachable]
        self.alphabet = self.dfa.alphabet

        
        return self.n_states, self.initial, self.alphabet
    
    # Passo 2: remover estados mortos
    def delete_dead(self):
        old_states = set()
        for t in self.dfa.transitions:
            temp = t.split(',')
            old_states.add(temp[0])
        
        new_states = set(self.dfa.final)
        while True:
            aux_new_states = new_states.copy()
        
            for t in self.dfa.transitions:
                org,s,dest = t.split(",")
                if dest in new_states:
                    new_states.add(org)
            if aux_new_states == new_states:
                break
    
        dead = old_states - new_states
        for state in dead:
            self.dfa.states_list.remove(state)

        self.n_states = int(self.dfa.n_states) - len(dead)
        self.final = [state for state in self.dfa.final if state not in dead]

        

        return self.n_states, self.initial, self.final, self.alphabet
    
    # Passo 3: minimizar o autômato

    def min_dfa(self, dfa):
        states = set()
        for t in dfa.transitions:
            org, _, _ = t.split(',')
            states.add(org)

        split_states = [set(dfa.final), states - set(dfa.final)]

        while True:
            new_split_states = []
            for s in split_states:
                if len(s) <= 1:
                    new_split_states.append(s)
                    continue
                dict_split = {}
                for state in s:
                    transitions = {}
                    for symb in dfa.alphabet:
                        next_states = set() 
                        for transition in dfa.transitions:
                            org, symbol, dest = transition.split(',')
                            if org == state and symbol == symb:
                                next_states.add(dest)

                        next_state_group = None
                        for existing_group in split_states:
                            if next_states <= existing_group:
                                next_state_group = existing_group
                                break

                        if next_state_group:
                            transitions[tuple(next_state_group)] = next_states

                    trans_tuple = tuple(sorted(transitions.keys()))
                    if trans_tuple not in dict_split:
                        dict_split[trans_tuple] = set()
                    dict_split[trans_tuple].add(state)

                new_split_states.extend(dict_split.values())

            if new_split_states == split_states:
                break
            else:
                split_states = new_split_states

        # Construir o automato mínimo:
        dfa_min = DFA()
        dfa_min.final = set()
        # Novos estados de equivalencia
        split_eq = []

       # for s in split_states:
        #    aux_st = list(sorted(s))[0]
         #   split_eq.append({aux_st})
        #new_split_st_sort = sorted(split_eq, key=lambda x: list(x)[0])

        for s in new_split_states:
            # Estado auxiliar que vai representar um grupo
            aux_st = list(sorted(s))[0]

            if aux_st in dfa.final:
                dfa_min.final.add(aux_st)

        for symb in dfa.alphabet:
            next_state = None
            for transition in dfa.transitions:
                org,simbolo,dest = transition.split(',')
                if org == state and simbolo == symb:
                    next_state = dest
                    break


        # Definir q0 do automato mínimo
        min_initial = None
        for i, s in enumerate(split_states):
            if dfa.initial in s:
                min_initial= list(sorted(s))[0]
                break
        dfa_min.transitions=set()
        for s in new_split_states:
            aux_st = list(sorted(s))[0]
            for t in dfa.transitions:
                org,simb,dest = t.split(',')
                if org in s:
                    for s_aux in new_split_states:
                        if dest in s_aux:
                            dest = list(sorted(s_aux))[0]
                            break
                    dfa_min.transitions.add(str(aux_st)+","+str(simb)+","+str(dest))


        dfa_min.n_states = len(split_states)
        dfa_min.initial = min_initial
        dfa_min.final.update(dfa_min.final)
        dfa_min.alphabet = dfa.alphabet
        return dfa_min
    
    def output(self, dfa):
        final_str = ','.join(self.dfa.final[0])
        alphabet_str = ",".join(self.dfa.alphabet)
        trans_str=""
        for t in dfa.transitions:
            org,s,dest = t.split(',')
            trans_str+=(org+","+s+","+dest+";")

        return f"{dfa.n_states};{self.initial};{{{final_str}}};{{{alphabet_str}}};{trans_str}"
    
    def minimize(self, input):
        self.input(input)
        self.delete_unreachable(self.dfa.initial)
        self.delete_dead()
        dfa_min = self.min_dfa(self.dfa)
        return self.output(dfa_min)

# Testes:

min = Min()
dfa1="8;P;{S,U,V,X};{0,1};P,0,Q;P,1,P;Q,0,T;Q,1,R;R,0,U;R,1,P;S,0,U;S,1,S;T,0,X;T,1,R;U,0,X;U,1,V;V,0,U;V,1,S;X,0,X;X,1,V"
output = min.minimize(dfa1)
# Saída esperada: #  11;A;{A,F,N};{a,b,c,d};A,a,B;A,b,E;A,c,K;A,d,G;B,a,C;B,b,H;B,c,L;C,a,A;C,b,I;C,c,F;E,b,F;E,c,H;E,d,N;F,b,E;F,c,K;F,d,G;G,d,N;H,b,K;H,c,I;I,b,L;I,c,E;K,b,H;K.c,L;L,b,I;L,c,F;N,d,G
print(output)
