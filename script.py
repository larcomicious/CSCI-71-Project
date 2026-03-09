parentheses_map = {'<': '>', '{': '}', '[': ']', '(': ')'}

class State:
    def __init__(self, name, final_state=False):
        self.name = name
        self.final_state = final_state

    def __eq__(self, other):
        return self.name == other.name
    
    def is_final_state(self):
        return self.final_state

    def handle_input(self, input_symbol):
        pass
    
class Transition:
    def __init__(self, from_state, to_state, input_symbol):
        self.from_state = from_state
        self.to_state = to_state
        self.input_symbol = input_symbol

class Q0(State):
    def handle_input(self, input_symbol):
        if input_symbol == '!':
            return Q1()
        else:
            print("Input must start with '!'")
            return self

class Q1(State):
    def handle_input(self, input_symbol):
        if input_symbol == '!':
            return self
        elif input_symbol == 'x' or input_symbol in parentheses_map.keys():
            return Q2()
        else:
            print("Invalid character. Expected 'x' or an opening bracket.")
            return self

class Q2(State):
    def handle_input(self, input_symbol):
        if input_symbol == 'x' or input_symbol in parentheses_map.keys():
            return self
        elif input_symbol in parentheses_map.values():
            return Q3()
        else:
            print("Invalid character. Expected an opening bracket or 'x'.")
            return self

class Q3(State):
    def handle_input(self, input_symbol):
        if input_symbol == 'x' or input_symbol in parentheses_map.values():
            return self
        elif input_symbol in parentheses_map.keys():
            return Q2()
        elif input_symbol == '!':
            return Q4()
        else:
            print("Input must end with '!'")
            return self

class Q4(State):
    def handle_input(self, input_symbol):
        if input_symbol == '':
            return Q1()
        else:
            print("Input must end with '!'")
            return self

class TransitionManager:
    def __init__(self):
        self.transitions = []

    def add_transition(self, transition):
        self.transitions.append(transition)
    
    def handle_transition(self, current_state, input_symbol):
        for transition in self.transitions:
            if transition.from_state == current_state and transition.input_symbol == input_symbol:
                return transition.to_state
        return current_state 


def main():
    q0 = Q0("q0")
    q1 = Q1("q1")
    q2 = Q2("q2")
    q3 = Q3("q3")
    q4 = Q4("q4", True)

    fsm = TransitionManager()

    fsm.add_transition(Transition(q0, q1, '!'))
    
    # q1 to q1
    fsm.add_transition(Transition(q1, q1, '!'))

    # q1 to q2
    fsm.add_transition(Transition(q1, q2, 'x'))
    for opening_bracket in parentheses_map.keys():
        fsm.add_transition(Transition(q1, q2, opening_bracket))
    
    # q2 to q2
    fsm.add_transition(Transition(q2, q2, 'x'))
    for opening_bracket in parentheses_map.keys():
        fsm.add_transition(Transition(q2, q2, opening_bracket))

    # q2 to q3
    for closing_bracket in parentheses_map.values():
        fsm.add_transition(Transition(q2, q3, closing_bracket))

    # q3 to q3
    fsm.add_transition(Transition(q3, q3, 'x'))
    for closing_bracket in parentheses_map.values():
        fsm.add_transition(Transition(q3, q3, closing_bracket))
    
    # q3 to q4
    fsm.add_transition(Transition(q3, q4, '!'))

    # q4 to q1
    fsm.add_transition(Transition(q4, q1, ''))

    current_state = q0

    with open('input.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        user_input = line.strip()
        print(f"Processing input: {user_input}")
    
        
        for char in user_input:
            current_state = fsm.handle_transition(current_state, char)
            # print(f"Current state: {current_state.name}, Input: '{char}'")
        
        if current_state.is_final_state():
            print("String accepted.")
        else:
            print("String rejected.")
        
        current_state = q0


if __name__ == "__main__":
    main()