import rootutils

root_dir = rootutils.setup_root(".",
                                indicator=".test-pytest-root",
                                pythonpath=True)
import math

from shapes.circle import Circle
import pytest

# pytestmark = pytest.mark.circle

class TestCircle:

    def setup_method(self, method):
        print(f"setting up methdo: {method}\n")
        # self.circle = Circle(radius=5)
    
    def teardown_method(self, method):
        print(f"tearing down method: {method}\n")
        # del self.circle

    def test_radius(self):
        
    def test_one(self):
        assert True
    
    def test_two(self):
        assert True
    
    # def test_area(self, circle):
    #     assert circle.area() == math.pi * circle.radius**2

    # def test_negative_radius(self):
    #     with pytest.raises(ValueError):
    #         Circle(radius=-5)
