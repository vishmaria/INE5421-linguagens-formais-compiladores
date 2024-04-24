from nfa import NFA


nfa = NFA()
nfa.input("2;A;{B};{a,&};A,&,A")


nfa1 = NFA()
nfa1.input("3;A;{C};{a,b,&};A,&,A;A,a,B")


nfa2 = NFA()
nfa2.input("3;A;{C};{a,b,&};A,&,A;B,&,C")

nfa3 = NFA()
nfa3.input("3;A;{C};{a,b};A,a,B")

