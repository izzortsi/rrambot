from PyInquirer import prompt
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError


class NumberValidator(Validator):

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))




questions = [
    {
        'type': 'list',
        'name': 'user_option',
        'message': 'Welcome to simple calculator',
        'choices': ["sum","difference","product", "divide"]
    },

    {
        'type': "input",
        "name": "a",
        "message": "Enter the first number",
        "validate": NumberValidator,
        "filter": lambda val: int(val)
    },

    {
        'type': "input",
        "name": "b",
        "message": "Enter the second number",
        "validate": NumberValidator,
        "filter": lambda val: int(val)
    },

    {
        'type': "input",
        "name": "is_exiting",
        "message": "Want to exit now?",
        "validate": NumberValidator,
        "filter": lambda val: int(val)
    }
]

exit_question = [
    {
        'type': "input",
        "name": "is_exiting",
        "message": "Want to exit now?",
        "validate": NumberValidator,
        "filter": lambda val: int(val)
    }
]


def add(a, b):
    print(a + b)

def difference(a, b):
    print(a - b)

def product(a, b):
    print(a * b)


def divide(a, b):
    print(a / b)


def main():
    #answers = prompt(questions, style=custom_style_2)
    #a = answers.get("a")
    #b = answers.get("b")
    #if answers.get("user_option") == "sum":
        #add(a, b)
    #elif answers.get("user_option") == "difference":
        #difference(a, b)
    #elif answers.get("user_option") == "product":
        #product(a, b)
    #elif answers.get("user_option") == "divide":
        #divide(a, b)
    loop = MainLoop()
    loop.loop()

class MainLoop:

    def __init__(self):

        exit_answer = prompt(exit_question, style=custom_style_2)
        self.is_exiting = exit_answer.get(is_exiting)



    def loop(self):

        while self.is_exiting == 0:
            exit_answer = prompt(exit_question, style=custom_style_2)
            self.is_exiting = exit_answer.get(is_exiting)


if __name__ == "__main__":
    main()

