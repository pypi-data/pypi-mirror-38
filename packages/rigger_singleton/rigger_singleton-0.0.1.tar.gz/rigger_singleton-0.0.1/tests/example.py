from rigger_singleton.singleton import singleton


@singleton
class Example:
    count = 0

    @classmethod
    def print_count(cls):
        print(cls.count)

    def __init__(self):
        Example.count += 1
        print("__init__")

