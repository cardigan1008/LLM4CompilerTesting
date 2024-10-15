from dataclasses import dataclass
import random

from constants import FEATURES, PROMPT_CODE, PROMPT_GENERATE, PROMPT_INPUT, STYLES

@dataclass
class BaseTemplate:
    template: str

    def format(self, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")


@dataclass
class TextTemplate(BaseTemplate):
    def format(self, **kwargs):
        return self.template.format(**kwargs)


@dataclass
class CodeTemplate(BaseTemplate):
    code_snippet: str = ""

    def format(self, **kwargs):
        if "code_snippet" in kwargs:
            self.code_snippet = kwargs["code_snippet"]
        return f"{super().template.format(**kwargs)}\n\nCode Snippet:\n{self.code_snippet}"


class Templates:
    features = FEATURES
    styles = STYLES
    templates = {
        "Generate": TextTemplate(PROMPT_GENERATE),
        "Input": TextTemplate(PROMPT_INPUT),
        "CodeSnippet": CodeTemplate(PROMPT_CODE),
    }

    @classmethod
    def random_feature(cls):
        return random.choice(cls.features)

    @classmethod
    def random_style(cls):
        return random.choice(cls.styles)

    @classmethod
    def format(cls, name, **kwargs):
        if name == "Generate":
            if "feature" not in kwargs:
                kwargs["feature"] = cls.random_feature()
            if "style" not in kwargs:
                kwargs["style"] = cls.random_style()
            return cls.templates[name].format(**kwargs)
        elif name == "CodeSnippet":
            if "code_snippet" not in kwargs:
                raise ValueError("Code snippet must be provided for CodeSnippet template.")
            return cls.templates[name].format(**kwargs)
        return cls.templates[name].format(**kwargs)
