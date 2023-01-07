class State:
    def __init__(self) -> None:
        self.valprev = 0
        self.index = 0
    def reset(self):
        self.valprev = 0
        self.index = 0