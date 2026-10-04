import heapq
import time


class SearchResult:

    def __init__(
        self,
        path,
        cost,
        explored,
        elapsed
    ):
        self.path = path
        self.cost = cost
        self.explored = explored
        self.elapsed = elapsed

    @property
    def found(self):
        return self.path is not None


class SearchEngine:

    def __init__(self, campus):
        self.campus = campus

    def run(self, source, destination, method):

        started = time.perf_counter()

        if source == destination:
            elapsed = time.perf_counter() - started
            return SearchResult(
                [source],
                0,
                1,
                elapsed
            )

        if source in {
            "CSE_Lab",
            "CSE_Reflxon",
            "CSE_Seminar"
        }:
            initial_state = "CSE"
        else:
            initial_state = "NORMAL"

        start_state = (source, initial_state)

        queue = []
        sequence = 0

        start_h = self.campus.heuristic(
            source,
            destination
        )

        heapq.heappush(
            queue,
            (start_h, sequence, start_state, 0, [source])
        )

        best_cost = {}
        explored = 0

        while queue:

            (
                priority,
                _,
                state,
                current_cost,
                path
            ) = heapq.heappop(queue)

            current, zone = state

            if (
                state in best_cost
                and current_cost >= best_cost[state]
            ):
                continue

            best_cost[state] = current_cost
            explored += 1

            if current == destination:

                elapsed = (
                    time.perf_counter() - started
                )

                return SearchResult(
                    path,
                    current_cost,
                    explored,
                    elapsed
                )

            for neighbor, weight in (
                self.campus.neighbors(current)
            ):

                if not self.campus.allowed_move(
                    current,
                    neighbor,
                    zone
                ):
                    continue

                next_zone = self.campus.update_state(
                    current,
                    neighbor,
                    zone
                )

                new_cost = current_cost + weight

                h = self.campus.heuristic(
                    neighbor,
                    destination
                )

                if method == "GREEDY":
                    score = h
                else:
                    score = new_cost + h

                sequence += 1

                heapq.heappush(
                    queue,
                    (
                        score,
                        sequence,
                        (neighbor, next_zone),
                        new_cost,
                        path + [neighbor]
                    )
                )

        elapsed = time.perf_counter() - started

        return SearchResult(
            None,
            float("inf"),
            explored,
            elapsed
        )