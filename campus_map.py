import json
import heapq


CSE_LOCATIONS = {
    "CSE_Lab",
    "CSE_Reflxon",
    "CSE_Seminar"
}

TOWER_ENTRIES = {
    "Tower2_Front",
    "Tower2_Rear"
}


class CampusMap:

    def __init__(self, filename="campus.json"):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.locations = data["locations"]
        self.graph = {node: [] for node in self.locations}

        for edge in data["connections"]:
            first = edge["from"]
            second = edge["to"]
            weight = edge["weight"]

            self.graph[first].append((second, weight))
            self.graph[second].append((first, weight))

    def get_locations(self):
        return list(self.locations.keys())

    def get_name(self, node):
        return self.locations[node]

    def neighbors(self, node):
        return self.graph[node]

    def heuristic(self, start, goal):
        """
        Estimate used by both agents.

        It calculates the shortest weighted distance in
        the campus graph without applying the CSE restriction.
        """

        distances = {
            node: float("inf")
            for node in self.graph
        }

        distances[start] = 0
        queue = [(0, start)]

        while queue:

            distance, current = heapq.heappop(queue)

            if current == goal:
                return distance

            if distance > distances[current]:
                continue

            for neighbor, weight in self.graph[current]:

                new_distance = distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

                    heapq.heappush(
                        queue,
                        (new_distance, neighbor)
                    )

        return float("inf")

    def allowed_move(self, current, next_node, state):

        if state == "CSE":

            return (
                next_node in CSE_LOCATIONS
                or next_node == "LiftArea"
            )

        if state == "LEAVING_CSE":

            return next_node in TOWER_ENTRIES

        if next_node in CSE_LOCATIONS:

            return current == "LiftArea"

        return True

    def update_state(self, current, next_node, state):

        if (
            current == "LiftArea"
            and next_node in CSE_LOCATIONS
        ):
            return "CSE"

        if (
            state == "CSE"
            and next_node == "LiftArea"
        ):
            return "LEAVING_CSE"

        if (
            state == "LEAVING_CSE"
            and next_node in TOWER_ENTRIES
        ):
            return "NORMAL"

        return state