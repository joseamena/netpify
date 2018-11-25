
class Step:
    def __init__(self, prompt, choices=None):
        self.prompt = prompt
        self.choices = choices
        self.substeps = []

    def select_option(self, choice):
        if self.choices is None:
            # For inputs that don't have choices
            # input will not be a number
            self.selected_choice = choice
            return True

        if choice < 0 or choice >= len(self.choices):
            return False


        self.selected_choice = self.choices[choice]
        return True

configuration = {}

step1 = Step("Enter name: ")
step2 = Step("Enter location descripton: ")
steps = [step1, step2]


def configure():
    for step in steps:
        choice = input(step.prompt)