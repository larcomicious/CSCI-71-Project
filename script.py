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
                # print(f"Error: Invalid input symbol '{self.input_symbol}' for PUSH action.")
                self.from_state.error_occurred = True
                # raise ValueError("Invalid input symbol for PUSH action.")
        elif self.action == Transition.Action.POP:
            if stack and parentheses_map.get(stack[-1]) == self.input_symbol:
                stack.pop()
            else:
                # print(stack)
                # print(f"Error: Mismatched parentheses. Expected '{parentheses_map.get(stack[-1])}' but got '{self.input_symbol}'." if stack else f"Error: No opening parenthesis to match '{self.input_symbol}'.")
                self.from_state.error_occurred = True
                # raise ValueError("Mismatched parentheses or empty stack.")
        

class TransitionManager:
    error_occurred = False
    def __init__(self):
        self.transitions = []
        self.stack = ['Z']

    def add_transition(self, transition):
        self.transitions.append(transition)
    
    def clear_stack(self):
        self.stack = ['Z']
    
    def is_stack_empty(self):
        return len(self.stack) == 1 and self.stack[0] == 'Z'

    def handle_transition(self, current_state, input_string):
        print(f"ID: ({current_state.name}, {input_string}, {''.join(reversed(self.stack))})")

        current_input_symbol = input_string[0] if input_string else ''
        # if current_state.error_occurred:
        #     print("Error occurred in previous transitions. Rejecting input.")
        #     return current_state
        for transition in self.transitions:
            if transition.from_state == current_state and transition.input_symbol == current_input_symbol:
                transition.perform_action(self.stack)
                return transition.to_state
                
        current_state.error_occurred = True
        return current_state 

fsm = TransitionManager()

q0 = State("q0")
q1 = State("q1")
q2 = State("q2", True)
states = [q0, q1, q2]

current_state = q0

def setup_transitions():
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
    
    # q1 to q2
    fsm.add_transition(Transition(q1, q2, '!', Transition.Action.POP))
    

def reset_states(states):
    for state in states:
        state.error_occurred = False

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def is_balanced(input_string):
    class ErrorTypes:
        NO_ERROR = 0
        TRANSITION_ERROR = 1
        NOT_IN_FINAL_STATE = 2

    # reset logic
    current_state = q0
    fsm.clear_stack()
    reset_states(states)

    # error flags
    type_of_error = ErrorTypes.NO_ERROR
    failed_at_position = "" 
    remaining_unprocessed_input = ""
    state_at_error = None

    print(f"Processing {input_string}")
    for i in range(len(input_string)):
        if current_state.error_occurred:
            type_of_error = ErrorTypes.TRANSITION_ERROR
            failed_at_position = i
            remaining_unprocessed_input = input_string[i-1:]
            
            break
        
        current_state = fsm.handle_transition(current_state, input_string[i:])
    
    if not current_state.is_final_state() and type_of_error == ErrorTypes.NO_ERROR:
        type_of_error = ErrorTypes.NOT_IN_FINAL_STATE
        state_at_error = current_state.name
    
    # if not fsm.is_stack_empty():
    #     type_of_error = ErrorTypes.STACK_NOT_EMPTY
    #     remaining_unprocessed_input = ''.join(reversed(fsm.stack))
    
    if type_of_error == ErrorTypes.TRANSITION_ERROR:
        print(f"Invalid string. Failed at position {failed_at_position}.")
        print(f"Remaining unprocessed input string: {remaining_unprocessed_input}")
        return False
    elif type_of_error == ErrorTypes.NOT_IN_FINAL_STATE:
        print(f"ID: ({current_state.name}, E, {''.join(reversed(fsm.stack))})")
        print(f"Invalid string. {state_at_error} is not a final state.")
        return False

    if not current_state.error_occurred and current_state.is_final_state() and fsm.is_stack_empty():
        print(f"ID: ({current_state.name}, E, {''.join(reversed(fsm.stack))})")
        print(f"{current_state.name} is a final state.")
        
        return True
    
    return False
    
        

def main1():
    setup_transitions()
    
    lines = read_input_file('input.txt')

    for line in lines:
        input_string = line.strip()

        if is_balanced(input_string):
            print(f"{input_string} is valid and has balanced brackets.")

def main2():
    pass

if __name__ == "__main__":
    main1()
    main2()