class Player:
    def __init__(self, id, x=0, y=0):
        self.id = id
        self.colour = ((id-1)*50, (id-1)*50, (id-1)*50)
        self.width = self.height = 50
        self.x = 0 if not x else x
        self.y = (id-1)*self.height if not y else y
