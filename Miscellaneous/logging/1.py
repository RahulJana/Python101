import logging
from employee import Employee

logging.basicConfig(filename="1.log",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

# print("DEBUG: ", logging.DEBUG)
# print("INFO: ", logging.INFO)
# print("WARNING: ", logging.WARNING)
# print("ERROR: ", logging.ERROR)
# print("CRITICAL: ", logging.CRITICAL)


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":

    num_1 = 10
    num_2 = 5

    logging.debug(add(num_1, num_2))
    logging.debug(subtract(num_1, num_2))
    logging.debug(multiply(num_1, num_2))
    logging.debug(divide(num_1, num_2))

    #  Creating employees
    emp1 = Employee("RAHUL", "JANA")
    emp2 = Employee("sosuke", "aizen")
