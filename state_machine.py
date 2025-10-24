class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(('START', None))