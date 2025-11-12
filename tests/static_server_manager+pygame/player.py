class Player:
    def __init__(self, id, x=0, y=0):
        # If the players id is one, then add 1 to it because otherwise the colour becomes black when subtracting 1
        self.id = id if id != 1 else id+1

        self.colour = ((self.id-1)*50, (self.id-1)*50, (self.id-1)*50)
        self.width = self.height = 50
        self.x = 0 if not x else x
        self.y = (self.id-1)*self.height if not y else y
