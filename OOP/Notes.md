# self Keyword:

link: <https://www.youtube.com/watch?v=oaiQ5hYKHTE>

```python
class Employee:
    def set_salary(self, value: int):
        self.salary = value

e = Employee()
e.set_salary(value = 25000)
print(e.salary)
```

Output:

```Output
25000
```

`def set_salary(self, value: str)` has two parameter `self` and `value` ; But when we are calling this function we are calling it with only one parameter `e.set_salary(value = "25000")`. In the class `set_salary` is an attribute(It is an attribute that holds a function object). `e` is a class instance, so when we call `e.set_salary()`; python takes its instance and searches for its class (here `class Employee`), after finding that python searches for that specific method `set_salary`. At this point of time there is a pointer to the instance `e` and a pointer to the function object `set_salary` and both the pointer object is packed inside a `method object`. Python calls the method object with an argument `25000`, and a new argument list is returned `["e", 25000]`. Now python calls the `set_salary()` method object with new argument list. When a caller, calls a class method; Python maps this `method call` to a `function call` in an `object`. And automatically adds its instance as its first argument(`self`). That is the reason we say self is the instance itself, cause python passed it on our behalf.

---

