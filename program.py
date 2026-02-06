import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from Position import Position

CIRCLE = "circle"
SQUARE = "square"

SHAPE = SQUARE

CIRCLE_X_LENGTH = 3
CIRCLE_Y_LENGTH = 1
CIRCLE_RADIUS = 2
SQUARE_X_LENGTH = 2
SQUARE_Y_LENGTH = 4

GENERATIONS = 300
NUMBER_OF_CHARGES = 15
POPULATION_SIZE = 100
ELITE_COUNT = int(POPULATION_SIZE * 0.1)
MUTATION_RATE = 0.2
MUTATION_SCALE = 0.05

def inside_conductor(position: Position) -> bool:
    """
    checks whether the coordinates are inside the conductor
    
    :param position: position which we want to check
    :type position: Position
    :return: true if the coordinates are inside the conductor, false otherwise
    :rtype: bool
    """
    if SHAPE == CIRCLE:
        return (position.x / CIRCLE_X_LENGTH)**2 + (position.y / CIRCLE_Y_LENGTH)**2 - CIRCLE_RADIUS**2 <= 0
    if SHAPE == SQUARE:
        return abs(position.x) < SQUARE_X_LENGTH / 2 and abs(position.y) < SQUARE_Y_LENGTH / 2

def random_point_inside() -> Position:
    """
    generates a random point inside the shape
    
    :return: random point inside our shape
    :rtype: Position
    """
    while True:
        x = random.uniform(-CIRCLE_RADIUS, CIRCLE_RADIUS)
        y = random.uniform(-CIRCLE_RADIUS, CIRCLE_RADIUS)
        position = Position(x, y)
        if inside_conductor(position):
            return position

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
    """
    creates POPULATION_SIZE configurations with NUMBER_OF_CHARGES of charges in each of them
    
    :return: list of configurations with charges and their position inside them
    :rtype: list[Position]
    """
    return [[random_point_inside() for charge in range(NUMBER_OF_CHARGES)] for entity in range(POPULATION_SIZE)]

def evolve(population: list[Position]) -> list[Position]:
    """
    secures ELITE_COUNT best configuration, and forces the rest to mutate to hopefully achieve better results
    
    :param population: current configuration of charges
    :type population: list[Position]
    :return: evolved configuration of charges
    :rtype: list[Position]
    """
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

def crossover(parent_1: list[Position], parent_2: list[Position]) -> list[Position]:
    """
    takes a random set of charges from both parents and merges them to form a child
    
    :param parent_1: first list of charges
    :type parent_1: list[Position]
    :param parent_2: second list of charges
    :type parent_2: list[Position]
    :return: list of charges positions, having some elements from the first and second parent
    :rtype: list[Position]
    """
    cut = random.randint(1, NUMBER_OF_CHARGES - 1)
    child = parent_1[:cut] + parent_2[cut:]
    return child

def mutate(configuration: list[Position]) -> list[Position]:
    """
    randomly changes the position of charges
    
    :param configuration: list of charge configurations
    :type configuration: list[Position]
    :return: list of charges with their positions slightly changed
    :rtype: list[Position]
    """
    new_configuration: list[Position] = []

    for position in configuration:
        if random.random() > MUTATION_RATE:     # higher mutation rate makes this less probable
            new_configuration.append(position)
            continue

        while True:
            new_position = position.copy()
            new_position.x += random.gauss(0, MUTATION_SCALE)
            new_position.y += random.gauss(0, MUTATION_SCALE)
            if inside_conductor(new_position):
                position = new_position.copy()
                break
                
        new_configuration.append(position)
    
    return new_configuration

def visualize(configuration: list[Position], conductor_radius=CIRCLE_RADIUS, show_ids=False):
    fig, ax = plt.subplots(figsize=(6, 6))

    if SHAPE == CIRCLE:
        t = np.linspace(0, 2*np.pi, 100)
        plt.plot( CIRCLE_X_LENGTH * CIRCLE_RADIUS * np.cos(t) , CIRCLE_Y_LENGTH * CIRCLE_RADIUS * np.sin(t) )
        ax.set_xlim(-CIRCLE_X_LENGTH * CIRCLE_RADIUS * 1.25, CIRCLE_X_LENGTH * CIRCLE_RADIUS * 1.25)
        ax.set_ylim(-CIRCLE_Y_LENGTH * CIRCLE_RADIUS * 1.25, CIRCLE_Y_LENGTH * CIRCLE_RADIUS * 1.25)
    if SHAPE == SQUARE:
        ax.add_patch(Rectangle((-SQUARE_X_LENGTH / 2, -SQUARE_Y_LENGTH / 2), 
                                SQUARE_X_LENGTH, 
                                SQUARE_Y_LENGTH, 
                                fill = False))
        ax.set_xlim(-SQUARE_X_LENGTH * 0.75, SQUARE_X_LENGTH * 0.75)
        ax.set_ylim(-SQUARE_Y_LENGTH * 0.75, SQUARE_Y_LENGTH * 0.75)

    xs = [position.x for position in configuration]
    ys = [position.y for position in configuration]

    ax.scatter(xs, ys, color='red', s=40, zorder=3)

    if show_ids:
        for i, (x, y) in enumerate(configuration):
            ax.text(x, y, f"{i}", fontsize=10,
                    ha='center', va='center',
                    color='white', weight='bold')
    
    ax.set_aspect('equal')

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Konfiguracja ładunków - minimum energii")

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
