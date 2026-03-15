parentheses_map = {'<': '>', '{': '}', '[': ']', '(': ')', '!': '!'}

class State:
    error_occurred = False
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
    class Action:
        PUSH = 1
        POP = 2
        NO_ACTION = 3
    
    def __init__(self, from_state, to_state, input_symbol, action=Action.NO_ACTION):
        self.from_state = from_state
        self.to_state = to_state
        self.input_symbol = input_symbol
        self.action = action
    
    def perform_action(self, stack):
        if self.action == Transition.Action.PUSH:
            if self.input_symbol in parentheses_map.keys() or self.input_symbol == '!':
                stack.append(self.input_symbol)
            else:
                print(f"Error: Invalid input symbol '{self.input_symbol}' for PUSH action.")
                self.from_state.error_occurred = True
                # raise ValueError("Invalid input symbol for PUSH action.")
        elif self.action == Transition.Action.POP:
            if stack and parentheses_map.get(stack[-1]) == self.input_symbol:
                stack.pop()
            else:
                # print(stack)
                print(f"Error: Mismatched parentheses. Expected '{parentheses_map.get(stack[-1])}' but got '{self.input_symbol}'." if stack else f"Error: No opening parenthesis to match '{self.input_symbol}'.")
                self.from_state.error_occurred = True
                # raise ValueError("Mismatched parentheses or empty stack.")
        

class TransitionManager:
    stack = []
    error_occurred = False
    def __init__(self):
        self.transitions = []
        self.stack = []

    def add_transition(self, transition):
        self.transitions.append(transition)
    
    def clear_stack(self):
        self.stack = []
    
    def is_stack_empty(self):
        return len(self.stack) == 0

    def handle_transition(self, current_state, input_symbol):
        # if current_state.error_occurred:
        #     print("Error occurred in previous transitions. Rejecting input.")
        #     return current_state
        for transition in self.transitions:
            if transition.from_state == current_state and transition.input_symbol == input_symbol:
                transition.perform_action(self.stack)
                # print(transition.action)
                # print(self.stack)
                return transition.to_state
            else:
                # print(f"No transition found for state '{current_state.name}' with input '{input_symbol}'")
                current_state.error_occurred = True

        return current_state 
    
class Q0(State):
    def handle_input(self, input_symbol):
        if input_symbol == '!':
            return Q1()
        else:
            print("Input must start with '!'")
            return self

class Q1(State):
    def handle_input(self, input_symbol):
        if input_symbol == 'x' or input_symbol in parentheses_map.keys() or input_symbol in parentheses_map.values():
            return self
        elif input_symbol == '!':
            return Q2()
        else:
            print("Invalid character. Expected 'x' or an opening bracket.")
            return self

class Q2(State):
    def handle_input(self, input_symbol):
        # if input_symbol == '!':
        #     return self
        # else:
        #     print("")
        #     return self
        print("in q2")
        pass

def reset_states(states):
    for state in states:
        state.error_occurred = False

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]
   

def main():
    q0 = Q0("q0")
    q1 = Q1("q1")
    q2 = Q2("q2", True)
    states = [q0, q1, q2]

    fsm = TransitionManager()

    # q0 to q1
    fsm.add_transition(Transition(q0, q1, '!', Transition.Action.PUSH))
    
    # q1 to q1
    fsm.add_transition(Transition(q1, q1, 'x', Transition.Action.NO_ACTION))
    fsm.add_transition(Transition(q1, q1, '<', Transition.Action.PUSH))
    fsm.add_transition(Transition(q1, q1, '{', Transition.Action.PUSH))
    fsm.add_transition(Transition(q1, q1, '[', Transition.Action.PUSH))
    fsm.add_transition(Transition(q1, q1, '(', Transition.Action.PUSH))
    
    fsm.add_transition(Transition(q1, q1, '>', Transition.Action.POP))
    fsm.add_transition(Transition(q1, q1, '}', Transition.Action.POP))
    fsm.add_transition(Transition(q1, q1, ']', Transition.Action.POP))
    fsm.add_transition(Transition(q1, q1, ')', Transition.Action.POP))
    
    fsm.add_transition(Transition(q1, q2, '!', Transition.Action.POP))
    
    current_state = q0


    lines = read_input_file('input.txt')

    for line in lines:
        user_input = line.strip()
        # print(f"Processing input: {user_input}")
    
        
        for char in user_input:
            if current_state.error_occurred:
                print("Error occurred in previous transitions. Rejecting input.")
                print(f"Processed symbols up to error: '{user_input[:user_input.index(char)]}'")
                break
            # print(f"Current state: {current_state.name}, Input: '{char}'")
            current_state = fsm.handle_transition(current_state, char)

        if current_state.is_final_state() and fsm.is_stack_empty():
            print(f"Input: {user_input} accepted.\n")
        else:
            print(f"Input: {user_input} rejected.")
        
        current_state = q0
        fsm.clear_stack()
        reset_states(states)


if __name__ == "__main__":
    main()