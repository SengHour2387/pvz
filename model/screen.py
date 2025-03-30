class Window:
    class position:
        x = 0
        y = 0

    class size:
        x = 1300
        y = 700


class Eviron:
    class position:
        startx = 1300 - 1152
        starty = 700 - 520

        endx = 1300
        endy = 700

    def setEnviLocX(self,preferLocX):
        return (1300 - 1152) + preferLocX

    def setEnviLocY(self,preferLocY):
        return (700 - 520) + preferLocY
