import random
import matplotlib.pyplot as plt
from Position import Position

CIRCLE_RADIUS = 1
POPULATION_SIZE = 100
GENERATIONS = 300
NUMBER_OF_CHARGES = 15
ELITE_COUNT = int(POPULATION_SIZE * 0.1)
MUTATION_RATE = 0.2
MUTATION_SCALE = 0.05

def inside_conductor(x, y) -> float:
    return x*x + y*y <= CIRCLE_RADIUS**2

def random_point_inside() -> Position:
    while True:
        x = random.uniform(-CIRCLE_RADIUS, CIRCLE_RADIUS)
        y = random.uniform(-CIRCLE_RADIUS, CIRCLE_RADIUS)
        if inside_conductor(x, y):
            return Position(x, y)

def energy(configuration: list[Position]) -> float:
    """
    Calculates the total energy of the charge arrangement
    
    :param configuration: list of charges and their positions in space
    :type configuration: list
    :return: the total energy of the configuration
    :rtype: float
    """
    total_energy = 0
    for i in range(len(configuration)):
        for j in range(i + 1, len(configuration)):
            position_1: Position = configuration[i]
            position_2: Position = configuration[j]
            distance = Position.distance(position_1, position_2)
            if distance < 1e-9:
                total_energy += 1 / 1e-9
                continue
            
            total_energy += 1 / distance
    return total_energy

def initialize_population() -> list[Position]:
    return [[random_point_inside() for charge in range(NUMBER_OF_CHARGES)] for entity in range(POPULATION_SIZE)]

def evolve(population: list[Position]) -> list[Position]:
    scored = [(energy(configuration), configuration) for configuration in population]
    scored.sort(key=lambda x: x[0])

    new_population = [configuration for (energy, configuration) in scored[:ELITE_COUNT]]
    
    while len(new_population) < POPULATION_SIZE:
        parent_1 = random.choice(scored[:POPULATION_SIZE // 2])[1]
        parent_2 = random.choice(scored[:POPULATION_SIZE // 2])[1]
        child = crossover(parent_1, parent_2)
        child = mutate(child)
        new_population.append(child)

    return new_population

def crossover(parent_1, parent_2) -> list[Position]:
    cut = random.randint(1, NUMBER_OF_CHARGES - 1)
    child = parent_1[:cut] + parent_2[cut:]
    return child

def mutate(configuration: list[Position]) -> list[Position]:
    new_configuration: list[Position] = []

    for position in configuration:
        if random.random() > MUTATION_RATE:     # higher mutation rate makes this less probable
            new_configuration.append(position)
            continue

        while True:
            x = position.x
            y = position.y
            x += random.gauss(0, MUTATION_SCALE)
            y += random.gauss(0, MUTATION_SCALE)
            if inside_conductor(x, y):
                position = Position(x, y)
                break
                
        new_configuration.append(position)
    
    return new_configuration

def visualize(configuration: list[Position], conductor_radius=CIRCLE_RADIUS, show_ids=False):
    """
    configuration = [(x1,y1), (x2,y2), ...]
    """

    fig, ax = plt.subplots(figsize=(6, 6))

    # =========================
    # PRZEWODNIK (KOŁO)
    # =========================
    circle = plt.Circle((0, 0),
                        conductor_radius,
                        color='black',
                        fill=False,
                        linewidth=2)
    ax.add_artist(circle)

    # =========================
    # ŁADUNKI
    # =========================
    xs = [position.x for position in configuration]
    ys = [position.y for position in configuration]

    ax.scatter(xs, ys, color='red', s=80, zorder=3)

    # Numeracja (opcjonalna)
    if show_ids:
        for i, (x, y) in enumerate(configuration):
            ax.text(x, y, f"{i}", fontsize=10,
                    ha='center', va='center',
                    color='white', weight='bold')

    # =========================
    # FORMATOWANIE
    # =========================
    ax.set_aspect('equal')
    ax.set_xlim(-CIRCLE_RADIUS * 1.25, CIRCLE_RADIUS * 1.25)
    ax.set_ylim(-CIRCLE_RADIUS * 1.25, CIRCLE_RADIUS * 1.25)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Konfiguracja ładunków – minimum energii")

    ax.grid(True, linestyle='--', alpha=0.4)

    plt.show()

def main():
    population: list[Position] = initialize_population()

    for generation in range(GENERATIONS):
        population = evolve(population)
    
    best_config = min(population, key=energy)

    print("\nNajlepsza konfiguracja:")
    for p in best_config:
        print(p)
    print("Energia:", energy(best_config))

    visualize(best_config)


if __name__ == '__main__':
    main()
