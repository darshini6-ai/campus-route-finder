class CampusGraph:
    def __init__(self):
        self.graph = {}

    def add_location(self, name):
        if name not in self.graph:
            self.graph[name] = []

    def add_connection(self, location1, location2):
        if location1 not in self.graph:
            self.add_location(location1)

        if location2 not in self.graph:
            self.add_location(location2)

        self.graph[location1].append(location2)
        self.graph[location2].append(location1)

    def get_locations(self):
        return list(self.graph.keys())

    def get_neighbors(self, location):
        return self.graph.get(location, [])
