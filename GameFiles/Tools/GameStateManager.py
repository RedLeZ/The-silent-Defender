class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.previous_state = None
        self.state_change_requested = False
        self.new_state_name = None

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def change_state(self, state_name):
        self.state_change_requested = True
        self.new_state_name = state_name
    
    def handle_events(self, event):
        if self.current_state:
            self.current_state.handle_events(event)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)
        if self.state_change_requested:
            self._change_state(self.new_state_name)
            self.state_change_requested = False
    
    def _change_state(self, state_name):
        if state_name in self.states:
            new_state = self.states[state_name]
            if self.current_state is not None and self.current_state != new_state:
                self.current_state.end()
            self.previous_state = self.current_state
            self.current_state = new_state
            if self.previous_state != self.current_state:
                self.current_state.start()

    def get_previous_state(self):
        return self.previous_state

    def is_endless_state(self):
        return self.current_state == "Endless"

    def draw(self, surface):
        if self.current_state:
            self.current_state.draw(surface)
