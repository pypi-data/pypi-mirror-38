from lhub_integ import util


class action:
    actions = {}

    def __init__(self, f):
        # See https://www.python.org/dev/peps/pep-3155/
        if f.__name__ != f.__qualname__:
            util.exit_with_instantiation_errors(
                code="invalid_action", errors=["actions must be top level functions"]
            )

        entrypoint = f"{f.__module__}.{f.__name__}"
        self.actions[entrypoint] = f
        self.f = f

    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)

    @classmethod
    def all(cls):
        return cls.actions
