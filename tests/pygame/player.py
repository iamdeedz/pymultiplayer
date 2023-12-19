class Player:
    def __init__(self, id):
        self.colour = ((id-1)*50, (id-1)*50, (id-1)*50)
        self.width = self.height = 50
        self.x = 0
        self.y = (id-1)*self.height
