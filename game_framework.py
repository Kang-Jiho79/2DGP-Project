running = None
stack = None

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()