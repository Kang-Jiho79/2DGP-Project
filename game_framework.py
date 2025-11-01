running = None
stack = None

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()

def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()

def pop_mode():
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    if (len(stack) > 0):
        stack[-1].resume()