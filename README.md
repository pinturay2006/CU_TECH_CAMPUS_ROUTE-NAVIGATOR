# AI Campus Route Navigator — CU Technology Campus
**Course:** AI/ML Laboratory | B.Tech. 5th Semester  
**Assignment:** Assignment X_03  
**Institution:** University of Calcutta (Technology Campus)

---

## 📌 Problem Overview & Mission

The goal of this project is to construct an intelligent campus navigation system for the **CU Technology Campus** using graph modeling and heuristic search algorithms. Given the official campus satellite layout, the physical environment is mapped into a weighted graph with specific real-world topological constraints.

Two distinct AI routing agents are implemented and evaluated:
1. **`PATHFINDER`** — **Greedy Best-First Search** ($f(n) = h(n)$)
2. **`ORBIT`** — **A\* Search** ($f(n) = g(n) + h(n)$)

### ❓ The Core Research Question
> *"Does the path that looks closest to the destination also produce the best route?"*

By deploying both agents on various campus navigation queries, this project investigates how local heuristic greediness compares to optimal cost-plus-heuristic exploration, specifically when navigating constrained topological zones (such as departmental access corridors).

---

## 🗺️ Campus Graph & Node Representation

All nodes strictly correspond to physical landmarks identified on the satellite map. Per assignment instructions, no imaginary or extraneous nodes have been introduced.

### Campus Nodes (21 Locations)
| Node Code | Location Name on Campus Map | Category |
| :--- | :--- | :--- |
| `G1` | Entry Gate 1 (G1) | Campus Gate |
| `G2` | Entry Gate 2 (G2) | Campus Gate |
| `G3` | Entry Gate 2 (G3) | Campus Gate |
| `G4` | Entry Gate 2 (G1 / G4) | Campus Gate |
| `Canteen` | Canteen, CU Technology Campus | Common Facility |
| `Reception` | Reception of Calcutta University | Administrative |
| `PowerArea` | Power Area | Utility |
| `Playground` | Playground of Technology Campus | Outdoor Area |
| `Parking` | Parking Area | Exterior Infrastructure |
| `Tower2_Front`| Tower 2 Front Entry | Building Entry Point |
| `Tower2_Rear` | Tower 2 Rear Entry | Building Entry Point |
| `Library` | Library | Academic Facility |
| `GardenArea` | Garden Area Technology Campus | Outdoor Area |
| `Auditorium` | Auditorium Hall | Event / Common Facility |
| `CRNN` | CRNN Centre (Nano Technology) | Research Centre |
| `NewBuilding1`| New Building 1 | Academic Building |
| `NewBuilding2`| New Building 2 (Workshop Building) | Academic / Workshop |
| `LiftArea` | Lift Area | Tower 2 Transit Hub |
| `CSE_Lab` | CSE Laboratory | Restricted CSE Zone |
| `CSE_Reflxon`| CSE Reflexon Room | Restricted CSE Zone |
| `CSE_Seminar`| CSE AKC Seminar Hall | Restricted CSE Zone |

---

## 🔒 Special CSE Routing Constraint (Part 7)

The Computer Science and Engineering (CSE) zone consists of:
- `CSE Laboratory`
- `CSE_AKC Seminar Hall`
- `CSE Reflexon Room`

### Architectural Rules
1. **Entry Protocol:** To access any CSE location, an agent coming from outside **must** follow:
   $$\text{Tower 2 Front/Rear Entry} \longrightarrow \text{Lift Area} \longrightarrow \text{CSE Locations}$$
2. **Isolation Invariant:** Once `Lift Area` has been crossed during entry, **only CSE-labelled locations may be visited** until the agent returns to the `Lift Area`. (e.g., transitions like `Lift Area` $\rightarrow$ `CSE Laboratory` $\rightarrow$ `GardenArea` are strictly invalid).
3. **Exit Protocol:** Leaving the CSE zone requires executing the reverse traversal:
   $$\text{CSE Locations} \longrightarrow \text{Lift Area} \longrightarrow \text{Tower 2 Front/Rear Entry} \longrightarrow \text{Other Campus Locations}$$
   *(Note: Direct exterior transitions from `Lift Area` to other locations like `Library` are forbidden when exiting from the CSE zone).*

### State-Space Modeling
To enforce this constraint in standard graph search without cycle bugs, each search state is modeled as a tuple:
$$\text{state} = (\text{node},\, \text{zone\_state})$$
Where $\text{zone\_state} \in \{\text{"NORMAL"}, \text{"CSE"}, \text{"LEAVING\_CSE"}\}$. The valid transitions are governed by `allowed_move()` and `update_state()` inside `campus_map.py`.

---

## 🧠 Heuristic & Search Formulations

### Heuristic Function: $h(n)$
Both agents share the same heuristic function $h(n)$, which estimates the remaining distance from candidate node $n$ to destination $g$.
- In `CampusMap.heuristic()`, $h(n)$ is computed as the unconstrained shortest path distance across the campus graph using Dijkstra's algorithm.
- **Admissibility & Consistency:** Because the unconstrained graph distance relaxation removes restrictions (such as CSE airlock gates), $h(n) \le h^*(n)$ always holds true. Hence, $h(n)$ is admissible and monotonic (consistent).

### Agents
1. **`PATHFINDER` (Greedy Best-First Search):**
   $$f(n) = h(n)$$
   Picks the frontier node that appears locally closest to the target. It is computationally lightweight but susceptible to local optima and sub-optimal global paths.
2. **`ORBIT` (A\* Search):**
   $$f(n) = g(n) + h(n)$$
   Balances the exact cost accumulated so far $g(n)$ with the estimated remaining distance $h(n)$. Guaranteed to return the shortest path when $h(n)$ is admissible.

---

## 🏗️ Project Architecture & OOP Structure

The codebase is organized into modular, decoupled components following Object-Oriented Programming (OOP) principles:

```
campus-navigator/
│
├── campus.json        # Decoupled campus graph data (nodes, walkable edges, edge weights)
├── campus_map.py     # CampusMap model (graph loader, Dijkstra heuristic, CSE validation)
├── search.py         # SearchEngine & SearchResult (Greedy BFS & A* algorithms)
├── agents.py         # Pathfinder and Orbit agent classes
├── main.py           # Interactive CLI for campus route querying
├── experiment.py     # Automated batch experiment benchmarking runner
├── results.csv       # Benchmark outputs & statistical measurements
├── screenshot/       # Visual execution proof of terminal runs
└── README.md         # Comprehensive project documentation
```

### Module Responsibilities
- **[campus.json](file:///e:/CU_TECH_CAMPUS_ROUTE-NAVIGATOR/campus.json):** Pure JSON storage defining node names and bidirectional walkable edges with metric weights (meters).
- **[campus_map.py](file:///e:/CU_TECH_CAMPUS_ROUTE-NAVIGATOR/campus_map.py):** Implements `CampusMap`. Handles graph representation, neighbor lookup, heuristic calculation, and state transition logic (`allowed_move`, `update_state`).
- **[search.py](file:///e:/CU_TECH_CAMPUS_ROUTE-NAVIGATOR/search.py):** Implements `SearchEngine` with priority-queue based search (`heapq`), state-tracking `(node, zone)`, and encapsulating outcome in `SearchResult`.
- **[agents.py](file:///e:/CU_TECH_CAMPUS_ROUTE-NAVIGATOR/agents.py):** Contains `Pathfinder` and `Orbit` agent classes interfacing with the search engine.
- **[experiment.py](file:///e:/CU_TECH_CAMPUS_ROUTE-NAVIGATOR/experiment.py):** Runs multi-route comparative experiments and writes performance metrics to `results.csv`.
- **[main.py](file:///e:/CU_TECH_CAMPUS_ROUTE-NAVIGATOR/main.py):** Interactive, user-friendly terminal interface featuring numbered menus, validation against identical source-destinations, and clean route outputs.

---

## 🚀 Installation & Running

### Requirements
- Python 3.8+
- Standard Library only (`json`, `heapq`, `time`, `csv`) — **No external dependencies or libraries required.**

### 1. Interactive Route Navigation
Run the interactive CLI:
```bash
python main.py
```
- Select the starting location number from the menu.
- Select the destination location number.
- Observe the comparative output showing both `PATHFINDER` and `ORBIT` routes, path costs, node counts, and runtimes.

### 2. Running Automated Benchmarks & Exporting to CSV
Run the automated experimentation suite:
```bash
python experiment.py
```
- Enter the number of trials and select locations.
- Results are recorded in `results.csv`.

---

## 📊 Experimental Results & Comparison (Part 8)

The table below summarizes empirical findings across multiple source-destination queries (including standard campus traversals and constrained CSE entries/exits):

| Query (Source $\rightarrow$ Destination) | Agent | Route Found | Path Cost (m) | Nodes Explored | Execution Time (s) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Reception $\rightarrow$ Library** | **PATHFINDER** | Reception $\rightarrow$ PowerArea $\rightarrow$ Playground $\rightarrow$ Parking $\rightarrow$ Tower2_Rear $\rightarrow$ Library | **27 m** | 6 | ~0.000218 s |
| | **ORBIT (A\*)** | Reception $\rightarrow$ PowerArea $\rightarrow$ Playground $\rightarrow$ Tower2_Front $\rightarrow$ LiftArea $\rightarrow$ Library | **25 m** | 6 | ~0.000191 s |
| **Library $\rightarrow$ Canteen** | **PATHFINDER** | Library $\rightarrow$ Tower2_Rear $\rightarrow$ Parking $\rightarrow$ Playground $\rightarrow$ PowerArea $\rightarrow$ Reception $\rightarrow$ Canteen | **31 m** | 7 | ~0.000202 s |
| | **ORBIT (A\*)** | Library $\rightarrow$ LiftArea $\rightarrow$ Tower2_Front $\rightarrow$ Playground $\rightarrow$ PowerArea $\rightarrow$ Reception $\rightarrow$ Canteen | **29 m** | 7 | ~0.000238 s |
| **Gate 1 $\rightarrow$ Library** | **PATHFINDER** | G1 $\rightarrow$ Canteen $\rightarrow$ Reception $\rightarrow$ PowerArea $\rightarrow$ Playground $\rightarrow$ Parking $\rightarrow$ Tower2_Rear $\rightarrow$ Library | **35 m** | 8 | ~0.000286 s |
| | **ORBIT (A\*)** | G1 $\rightarrow$ Canteen $\rightarrow$ Reception $\rightarrow$ PowerArea $\rightarrow$ Playground $\rightarrow$ Tower2_Front $\rightarrow$ LiftArea $\rightarrow$ Library | **33 m** | 8 | ~0.000252 s |
| **Canteen $\rightarrow$ New Building 2** | **PATHFINDER** | Canteen $\rightarrow$ G1 $\rightarrow$ Auditorium $\rightarrow$ NewBuilding2 | **21 m** | 4 | ~0.000102 s |
| | **ORBIT (A\*)** | Canteen $\rightarrow$ G1 $\rightarrow$ Auditorium $\rightarrow$ NewBuilding2 | **21 m** | 4 | ~0.000095 s |
| **Gate 1 $\rightarrow$ CSE Laboratory** | **PATHFINDER** | G1 $\rightarrow$ Canteen $\rightarrow$ Reception $\rightarrow$ PowerArea $\rightarrow$ Playground $\rightarrow$ Tower2_Front $\rightarrow$ LiftArea $\rightarrow$ CSE_Lab | **43 m** | 8 | ~0.000307 s |
| | **ORBIT (A\*)** | G1 $\rightarrow$ Canteen $\rightarrow$ Reception $\rightarrow$ PowerArea $\rightarrow$ Playground $\rightarrow$ Tower2_Front $\rightarrow$ LiftArea $\rightarrow$ CSE_Lab | **43 m** | 8 | ~0.000328 s |
| **Auditorium $\rightarrow$ CSE Seminar Hall** | **PATHFINDER** | Auditorium $\rightarrow$ CRNN $\rightarrow$ Reception $\rightarrow$ PowerArea $\rightarrow$ Playground $\rightarrow$ Tower2_Front $\rightarrow$ LiftArea $\rightarrow$ CSE_Lab $\rightarrow$ CSE_Seminar | **53 m** | 9 | ~0.000395 s |
| | **ORBIT (A\*)** | Auditorium $\rightarrow$ CRNN $\rightarrow$ Reception $\rightarrow$ PowerArea $\rightarrow$ Playground $\rightarrow$ Tower2_Front $\rightarrow$ LiftArea $\rightarrow$ CSE_Lab $\rightarrow$ CSE_Seminar | **53 m** | 9 | ~0.000367 s |
| **CSE Laboratory $\rightarrow$ Library** | **PATHFINDER** | CSE_Lab $\rightarrow$ LiftArea $\rightarrow$ Tower2_Rear $\rightarrow$ Library *(Enforces CSE exit rule)* | **25 m** | 4 | ~0.000078 s |
| | **ORBIT (A\*)** | CSE_Lab $\rightarrow$ LiftArea $\rightarrow$ Tower2_Rear $\rightarrow$ Library *(Enforces CSE exit rule)* | **25 m** | 4 | ~0.000070 s |

---

## 💡 Key Observations & Assignment Evaluation Questions (Part 9)

### 1. Does Greedy Best-First Search always find the shortest route?
**No.** Greedy Best-First Search (`PATHFINDER`) considers only $f(n) = h(n)$. It eagerly expands nodes that appear geometrically or heuristically closest to the goal, completely ignoring the cost $g(n)$ accumulated to reach that node.  
*Empirical Proof:* In the route from **Reception to Library**:
- `PATHFINDER` selects the `Parking Area` $\rightarrow$ `Tower 2 Rear Entry` path, yielding a total cost of **27 m**.
- `ORBIT` accounts for $g(n)$ and selects `Tower 2 Front Entry` $\rightarrow$ `Lift Area`, finding the true optimal path of **25 m**.

### 2. How does A\* use the distance already travelled?
A\* incorporates $g(n)$ directly into its node evaluation function: $f(n) = g(n) + h(n)$.
- $g(n)$ acts as a natural penalizing term against candidate paths that have already accumulated heavy walking distances.
- If a neighboring node has an attractive (low) remaining estimate $h(n)$ but took an excessively long distance $g(n)$ to reach, A\* deprioritizes it in the min-heap frontier, ensuring search focuses on paths with lower total prospective cost.

### 3. When do the two agents choose different paths?
The agents diverge when **a locally appealing step leads to higher accumulated edge weights**.
- For instance, when travelling to `Library`, expanding towards `Tower2_Rear` has an edge weight of 6m, while going through `Tower2_Front` $\rightarrow$ `LiftArea` $\rightarrow$ `Library` requires an edge of 10m then 2m. Greedy Best-First jumps at the local edge without realizing that passing through `LiftArea` unlocks a 2m shortcut into the Library, making the total path shorter.
- When all alternative routes have uniform or proportional edge weights, both agents produce the identical path.

### 4. How does the heuristic affect their behaviour?
- **For PATHFINDER:** The heuristic is the sole driving factor. If the heuristic landscape has local minima or valleys, Greedy Best-First can be misled down dead ends or suboptimal branches.
- **For ORBIT:** The heuristic acts as a pruning guide. Because our Dijkstra-based unconstrained heuristic is admissible ($h(n) \le h^*(n)$), A\* prunes suboptimal search spaces while mathematically guaranteeing the shortest path upon goal expansion.

### 5. What happens when the CSE constraint restricts possible routes?
The CSE constraint alters the permissible topology into a state machine:
- Exterior campus nodes cannot connect directly to CSE facilities; agents are forced to funnel through `Tower 2 Front/Rear Entry` $\rightarrow$ `Lift Area`.
- While exiting CSE facilities, direct connections to adjacent facilities (e.g., `Lift Area` $\rightarrow$ `Library` (2m)) cannot be taken immediately without first stepping out via `Tower 2 Front/Rear Entry`.
- This constraint increases the effective path length and alters the search tree depth, demonstrating how domain rules reshape graph traversal.

---

## 📷 Execution Screenshots

The following terminal screenshots demonstrate the system running in real-time:

### 1. General Campus Query (`Entry Gate 1` $\rightarrow$ `Library`)
Demonstrating cost divergence: PATHFINDER finds 35 m while ORBIT finds the optimal 33 m route.
![Query 1](screenshot/output1.png)

### 2. CSE Zone Access (`Canteen` $\rightarrow$ `CSE AKC Seminar Hall`)
Demonstrating proper protocol entry through `Tower 2 Front Entry` $\rightarrow$ `Lift Area` $\rightarrow$ `CSE Laboratory` $\rightarrow$ `CSE Seminar Hall`.
![Query 2](screenshot/output2.png)

### 3. Transit Hub Traversal (`Entry Gate 1` $\rightarrow$ `Lift Area`)
Demonstrating optimal node expansion to the Tower 2 Lift Transit Area.
![Query 3](screenshot/output3.png)

---

## 🛡️ Adherence to Assignment Rules

| Assignment Requirement | Status | Implementation Details |
| :--- | :---: | :--- |
| Use only nodes shown on provided map | ✅ Complete | Exactly 21 map locations defined in `campus.json`. |
| Do not create new locations/nodes | ✅ Complete | Zero synthetic nodes added; map integrity preserved. |
| Construct own graph & reasonable weights | ✅ Complete | Custom adjacency list with realistic metric walking weights. |
| Implement Greedy Best-First Search | ✅ Complete | `Pathfinder` class with $f(n) = h(n)$ using min-heap. |
| Implement A\* Search | ✅ Complete | `Orbit` class with $f(n) = g(n) + h(n)$. |
| Implement a Heuristic function | ✅ Complete | Admissible & consistent unconstrained graph distance. |
| Implement CSE-zone constraint | ✅ Complete | State-space tracking: `NORMAL` $\rightarrow$ `CSE` $\rightarrow$ `LEAVING_CSE`. |
| Use file handling for campus graph | ✅ Complete | Separated into `campus.json`. |
| Record experimental results to CSV | ✅ Complete | `experiment.py` logs structured metrics to `results.csv`. |
| OOP modular design | ✅ Complete | Clean separation: `CampusMap`, `SearchEngine`, `SearchResult`, `Pathfinder`, `Orbit`. |
| No external pathfinding libraries | ✅ Complete | 100% built from scratch using Python standard library. |

---

## 👥 Authors & Academic Credits
- **Course:** AI/ML Laboratory (B.Tech. 5th Semester)
- **Department:** Computer Science and Engineering
- **University:** University of Calcutta (Technology Campus)
