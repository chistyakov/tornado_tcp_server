from core.primitives import OnlineSourceStatistics


class OnlineStatistics:
    def __init__(self):
        self.registry = {}

    def __setitem__(self, source_name: str, value: OnlineSourceStatistics):
        self.registry[source_name] = value

    def __getitem__(self, item):
        return self.registry[item]

    def values(self):
        return self.registry.values()
