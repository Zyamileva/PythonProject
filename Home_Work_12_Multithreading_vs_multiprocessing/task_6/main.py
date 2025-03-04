import concurrent.futures
import logging
import random


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Organism:
    """Simulates a single life cycle of the organism.

    Increases energy through 'eating', decreases energy through normal expenditure, and reproduces if enough energy is available.

    Returns:
        A new Organism instance if reproduction occurs, the current instance if it survives, or None if it dies (energy drops to 0 or below).
    """

    def __init__(self, energy=100):
        self.energy = energy

    def live_cycle(self):
        """Simulates a single life cycle of the organism.

        Args:
            self (Organism): The organism instance.

        Returns:
            A new Organism instance if reproduction occurs, the current instance if it survives, or None if it dies (energy drops to 0 or below).
        """

        self.energy += random.randint(30, 40)  # Еда
        self.energy -= random.randint(1, 5)  # Расходы энергии
        if self.energy > 150:  # Размножение
            self.energy -= 90
            return Organism()
        return None if self.energy <= 0 else self


def simulate(organism: Organism):
    """Simulates a single life cycle of an organism.

    Args:
        organism: The organism object to simulate.

    Returns:
        The result of the organism's life cycle, which can be a new organism, the original organism, or None.
    """

    return organism.live_cycle()


population = [Organism() for _ in range(10)]

for generation in range(5):  # 5 поколений
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(simulate, population))

    # Обновление популяции
    population = [org for org in results if org]

    logging.info(f"Поколение {generation + 1}: {len(population)} организмов")
