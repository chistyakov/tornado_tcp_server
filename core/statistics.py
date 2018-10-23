from core.primitives import SourceStatistics


class SourceStatisticsRegistry:
    def __init__(self):
        self.registry = {}

    def __setitem__(self, source_name: str, stat: SourceStatistics):
        self.registry[source_name] = stat

    def __getitem__(self, item):
        return self.registry[item]

    def values(self):
        return self.registry.values()
