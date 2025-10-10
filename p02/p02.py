import argparse

class DFA:
    def __init__(self, transitions, start_state, accept_states):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.check_correctness()

    def run(self, input_string, trace=False):
        current_state = self.start_state
        if trace:
            print(f"Starting DFA trace for input: {input_string}")
        for (i,symbol) in enumerate(input_string):
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
                if trace:
                    print(f"{current_state}: {input_string[i:]}")
            else:
                return False  
        if trace:
            print(f"{current_state}")
        return current_state in self.accept_states
    
    def check_correctness(self):
        alphabet = set()
        all_states = set()
        for (state, symbol) in self.transitions.keys():
            alphabet.add(symbol)
            all_states.add(state)

        for state in all_states:
            for symbol in alphabet:
                if (state, symbol) not in self.transitions:
                    raise ValueError(f"DFA is incomplete: missing transition for state {state} on symbol '{symbol}'")
       

class NFA:
    def __init__(self, transitions, start_state, accept_states):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def run(self, input_string, trace=False):
        current_states = {self.start_state}
        if trace:
            print(f"Starting NFA trace for input: {input_string}")
        for (i,symbol) in enumerate(input_string):
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
            current_states = next_states
            if trace:
                print(f"{current_states} : {input_string[i:]}")
            if not current_states:
                return False  # No valid transitions, reject the input
        if trace:
            print(f"{current_states}")
        return any(state in self.accept_states for state in current_states)
    

def parse_dfa(file_path):
    transitions = {}
    accept_states = set()
    start_state = 'q0'
    with open(file_path, 'r') as file:
        # if first line is only one state, it's the start state
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                state_from, symbol, state_to = parts
                transitions[(state_from, symbol)] = state_to
            elif len(parts) == 1:
                accept_states.add(parts[0])

    return DFA(transitions, 'q0', accept_states)

def parse_nfa(file_path):
    transitions = {}
    accept_states = set()

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                state_from, symbol, state_to = parts
                if (state_from, symbol) not in transitions:
                    transitions[(state_from, symbol)] = set()
                transitions[(state_from, symbol)].add(state_to)
            elif len(parts) == 1:
                accept_states.add(parts[0])

    return NFA(transitions, 'q0', accept_states)


def main():
    parser = argparse.ArgumentParser(
        description="DFA/NFA Simulator\n\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        'automaton_file', 
        type=str, 
        help="Path to the file containing the automaton definition.\n"
             "Default (DFA) format is one transition or accept state per line:\n"
             "qA 0 qB (Transition from qA to qB on '0')\n"
             "qB (Accept state)\n The start state is always 'q0'."
    )
    parser.add_argument(
        'input_string', 
        type=str, 
        help="The input string to test (e.g., '0101')."
    )
    
  
    parser.add_argument(
        '-n', '--nfa', 
        action='store_true',
        help="Treat the input file as an NFA."
    )
    parser.add_argument(
        '-t', '--trace', 
        action='store_true',
        help="Enable tracing of the simulation."
    )

    args = parser.parse_args()

    # 1. Parse the automaton
    if args.nfa:
        print(f"Loading NFA from {args.automaton_file}...")
        automaton = parse_nfa(args.automaton_file)
    else:
        print(f"Loading DFA from {args.automaton_file}...")
        automaton = parse_dfa(args.automaton_file)

    # 2. Run the simulation and get result
    is_accepted = automaton.run(args.input_string, trace=args.trace)

    # 3. Print final result (required output is always ACCEPT/REJECT)
    if is_accepted:
        print("ACCEPT")
    else:
        print("REJECT")


if __name__ == "__main__":
    main()