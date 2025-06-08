import logging

logger = logging.getLogger(__name__)

logging.basicConfig(filename="employee.log",
                    level=logging.INFO,
                    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s ")


class Employee:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

        logger.info(f"Created Employee: {self.full_name} - {self.email}")

    @property
    def email(self):
        return f"{self.first_name.lower()}.{self.last_name.lower()}@company.com"

    @property
    def full_name(self):
        return f"{self.first_name[0].upper()}{self.first_name[1:].lower()} {self.last_name[0].upper()}{self.last_name[1:].lower()}"


if __name__ == "__main__":
    emp1 = Employee("joHn", "dOe")
    emp2 = Employee("jAne", "dOe")
