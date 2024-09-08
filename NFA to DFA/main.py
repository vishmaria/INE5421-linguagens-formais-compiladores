from nfa import NFA  # assuming nfa.py is the file containing your NFA class

def main():
    
    nfa = NFA()

    print("Test Case 1:")
    nfa.input("3;A;{C};{0,1,&};A,&,B;B,0,C;A,1,C;C,1,C")

    print(nfa.determinize())  
    
if __name__ == "__main__":
    main()
