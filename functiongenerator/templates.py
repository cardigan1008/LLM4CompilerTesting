from dataclasses import dataclass
import random

from constants import FEATURES, PROMPT_GENERATE, PROMPT_INPUT, STYLES


@dataclass
class Template:
    template: str

    def format(self, **kwargs):
        return self.template.format(**kwargs)


class Templates:
    features = FEATURES
    styles = STYLES
    templates = {
        "Generate": Template(PROMPT_GENERATE),
        "Input": Template(PROMPT_INPUT),
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
        return cls.templates[name].format(**kwargs)
