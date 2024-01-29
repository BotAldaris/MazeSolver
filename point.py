class Point:
    def __init__(self,x=0,y=0) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"    