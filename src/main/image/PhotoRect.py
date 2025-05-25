
class PhotoRect:
    start_x:int = 0
    start_y:int = 0
    end_x:int = 0
    end_y:int = 0

    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def __str__(self):
        return f"{self.start_x},{self.start_y}~{self.end_x},{self.end_y}"

    def __repr__(self):
        return f"(start_x,start_y) ~ (end_x, end_y): ({self.start_x},{self.start_y})~({self.end_x},{self.end_y})"

    def getWidth(self):
        return self.end_x - self.start_x

    def getHeight(self):
        return self.end_y - self.start_y

    def copy(self):
        return PhotoRect(self.start_x, self.start_y, self.end_x, self.end_y)

    def multiply(self, value:float):
        self.start_x = int(self.start_x * value)
        self.start_y = int(self.start_y * value)
        self.end_x = int(self.end_x * value)
        self.end_y = int(self.end_y * value)