from campus_map import CampusMap
from search import SearchEngine
from agents import Pathfinder, Orbit


def show_locations(campus):
    print("\nCampus Locations")
    print("----------------")

    for number, code in enumerate(campus.get_locations(), 1):
        print(
            f"{number:2}. "
            f"{campus.get_name(code)} [{code}]"
        )


def choose_number(campus, prompt, used=None):
    locations = campus.get_locations()

    while True:
        value = input(prompt).strip()

        if value.lower() == "exit":
            return None

        if not value.isdigit():
            print("Please enter a valid location number.")
            continue

        number = int(value)

        if number < 1 or number > len(locations):
            print("That location number does not exist.")
            continue

        if used is not None and number == used:
            print("Source and destination must be different.")
            continue

        return number


def display_result(title, result, campus):
    print(f"\n{title}")
    print("-" * len(title))

    if not result.found:
        print("No valid route found.")
        print("Nodes explored:", result.explored)
        print(f"Execution time: {result.elapsed:.6f} s")
        return

    route = " -> ".join(
        campus.get_name(node)
        for node in result.path
    )

    print("Route:", route)
    print(f"Path cost: {result.cost} m")
    print("Nodes explored:", result.explored)
    print(f"Execution time: {result.elapsed:.6f} s")


def main():
    campus = CampusMap()
    engine = SearchEngine(campus)

    pathfinder = Pathfinder(engine)
    orbit = Orbit(engine)

    print("\nCU Technology Campus Route Navigator")
    print("Type 'exit' to close the program.")

    while True:

        # ONE MENU
        show_locations(campus)

        print(
            "\nSelect two different locations from the menu."
        )

        source_number = choose_number(
            campus,
            "Enter source number: "
        )

        if source_number is None:
            print("\nProgram ended.")
            return

        destination_number = choose_number(
            campus,
            "Enter destination number: ",
            used=source_number
        )

        if destination_number is None:
            print("\nProgram ended.")
            return

        locations = campus.get_locations()

        source = locations[source_number - 1]
        destination = locations[destination_number - 1]

        print("\nSelected route:")
        print(
            f"{campus.get_name(source)}"
            f" -> "
            f"{campus.get_name(destination)}"
        )

        # Run both agents
        pathfinder_result = pathfinder.navigate(
            source,
            destination
        )

        orbit_result = orbit.navigate(
            source,
            destination
        )

        # Different answers/results
        display_result(
            "PATHFINDER - Greedy Best-First Search",
            pathfinder_result,
            campus
        )

        display_result(
            "ORBIT - A* Search",
            orbit_result,
            campus
        )

        print(
            "\nSearch another route? (y/n): "
        )

        again = input("> ").strip().lower()

        if again != "y":
            print("\nProgram ended.")
            break


if __name__ == "__main__":
    main()