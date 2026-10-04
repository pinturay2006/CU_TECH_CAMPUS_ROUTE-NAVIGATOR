import csv

from campus_map import CampusMap
from search import SearchEngine
from agents import Pathfinder, Orbit


def select_location(campus, message):

    locations = campus.get_locations()

    while True:

        value = input(message).strip()

        if value.lower() == "exit":
            return None

        if not value.isdigit():
            print("Enter a valid number.")
            continue

        number = int(value)

        if 1 <= number <= len(locations):
            return locations[number - 1]

        print("Invalid location number.")


def show_locations(campus):

    print("\nCampus Locations")

    for number, code in enumerate(
        campus.get_locations(),
        1
    ):
        print(
            f"{number:2}. "
            f"{campus.get_name(code)} [{code}]"
        )


def run_experiments():

    campus = CampusMap()
    engine = SearchEngine(campus)

    pathfinder = Pathfinder(engine)
    orbit = Orbit(engine)

    while True:

        value = input(
            "\nHow many experiments do you want to run? "
        ).strip()

        if value.isdigit() and int(value) > 0:
            count = int(value)
            break

        print("Enter a positive number.")

    rows = []

    for number in range(1, count + 1):

        print(f"\nExperiment {number}")
        print("=" * 20)

        show_locations(campus)

        source = select_location(
            campus,
            "\nEnter source number: "
        )

        if source is None:
            print("Experiment cancelled.")
            return

        show_locations(campus)

        destination = select_location(
            campus,
            "\nEnter destination number: "
        )

        if destination is None:
            print("Experiment cancelled.")
            return

        results = [
            (
                "PATHFINDER",
                pathfinder.navigate(
                    source,
                    destination
                )
            ),
            (
                "ORBIT",
                orbit.navigate(
                    source,
                    destination
                )
            )
        ]

        for agent_name, result in results:

            if result.found:
                path = " -> ".join(result.path)
                cost = result.cost
            else:
                path = "No valid route"
                cost = ""

            rows.append({
                "Source": source,
                "Destination": destination,
                "Agent": agent_name,
                "Route": path,
                "Path Cost": cost,
                "Nodes Explored": result.explored,
                "Execution Time": (
                    f"{result.elapsed:.6f}"
                )
            })

    with open(
        "results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        columns = [
            "Source",
            "Destination",
            "Agent",
            "Route",
            "Path Cost",
            "Nodes Explored",
            "Execution Time"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=columns
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        "\nExperiments completed."
    )

    print(
        "Results saved in results.csv"
    )


if __name__ == "__main__":
    run_experiments()