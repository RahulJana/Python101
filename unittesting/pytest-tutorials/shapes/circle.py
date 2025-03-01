import rootutils

root_dir = rootutils.setup_root(".",
                                indicator=".test-pytest-root",
                                pythonpath=True)

import math
from shapes.shape import Shape

class Circle(Shape):

    def __init__(self, radius):
        if radius < 1:
            raise ValueError("The radius must be greater than 0.")
        self.radius = radius
        print(f"radius is: {self.radius}")

    def area(self):
        print("area:")
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        print("perimeter:")
        return math.pi * self.radius * 2

if __name__ == '__main__':
    c1 = Circle(radius=5)
    print(c1.area())
    print(c1.perimeter())
    
    
    c2 = Circle(radius=10)
    print(c2.area())
    print(c2.perimeter())