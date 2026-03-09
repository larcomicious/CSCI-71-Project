class State:
    def __init__(self, name):
        self.name = name
    
class Transition:
    def __init__(self, from_state, to_state, input_symbol, action):
        self.from_state = from_state
        self.to_state = to_state
        self.input_symbol = input_symbol
        self.action = action

parentheses_map = {'>': '<', '}': '{', ']': '[', ')': '('}

def is_balanced(input_string):
    stack = []
    
    if len(input_string) < 1:
        return False
    elif input_string[0] != '!':
        return False
    elif input_string[-1] != '!':
        return False

    for char in input_string[1:]:
        if char in parentheses_map.values():
            stack.append(char)
        elif char in parentheses_map.keys():
            if not stack or stack[-1] != parentheses_map[char]:
                return False
            stack.pop()
        elif char == "x":
            continue
        else:
            return False
    
    return len(stack) == 0

def main():
    input_string = '!xx[x({xx})[xxx]x]<xxx>x!'

    print(is_balanced(input_string))

if __name__ == "__main__":
    main()