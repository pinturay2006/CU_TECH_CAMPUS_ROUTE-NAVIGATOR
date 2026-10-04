class Pathfinder:

    def __init__(self, engine):
        self.engine = engine

    def navigate(self, source, destination):
        return self.engine.run(
            source,
            destination,
            "GREEDY"
        )


class Orbit:

    def __init__(self, engine):
        self.engine = engine

    def navigate(self, source, destination):
        return self.engine.run(
            source,
            destination,
            "ASTAR"
        )