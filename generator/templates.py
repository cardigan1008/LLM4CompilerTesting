from dataclasses import dataclass


@dataclass
class Template:
    template: str

    def format(self, **kwargs):
        return self.template.format(**kwargs)


class Templates:
    def __init__(self):
        self.templates = {}

    def add_template(self, name: str, template_str: str):
        self.templates[name] = Template(template_str)

    def get(self, name):
        return self.templates[name]

    def format(self, name, **kwargs):
        return self.get(name).format(**kwargs)


generate_templates = Templates()

generate_templates.add_template(
    "FormAI",
    (
        "Please mutate the code by adding the feature {feature} in a {style} style. "
        "Instructions: "
        "a. Be creative! "
        "b. Do not say I am sorry. Always come up with some new code. "
        "c. Make sure the program compiles and runs without any errors. "
        "d. Please generate the mutated code snippet that starts with ```C and ends with ```."
    ),
)

generate_templates.add_template(
    "Creal",
    (
        "Please generate a C function that has over 20 lines of code by adding the feature {feature} in a {style} style. "
        "Instructions: "
        "a. It takes only numeric input types and has a numeric return type. "
        "b. It dose not contain any other function calls, espeically I/O functions like printf or scanf. "
        "c. It is pure, meaning it has deterministic outputs and has no side effects. "
        "d. Please generate the code snippet that starts with ```C and ends with ```. "
        "e. Be creative! "
    ),
)

generate_templates.add_template(
    "Input",
    (
        "For the provided function, please generate the input pairs that cover all the possible branches. "
        "Instructions: "
        "a. Wrap the input pairs in a list. For example: [[1], [2], [3]] "
        "b. Just give me the pairs without any explanation. "
    ),
)
