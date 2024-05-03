class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.previous_state = None

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def change_state(self, state_name):
        if state_name in self.states:
            self.previous_state = self.current_state
            self.current_state = self.states[state_name]

    def handle_events(self, event):
        if self.current_state:
            self.current_state.handle_events(event)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)
        
    def get_previous_state(self):
        return self.previous_state
    
    def draw(self, surface):
        if self.current_state:
            self.current_state.draw(surface)
