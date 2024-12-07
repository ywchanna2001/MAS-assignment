from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import AnimalAgent, PatrolAgent, ThreatAgent

class ForestModel(Model):
    def __init__(self, width, height, num_animals, num_patrols, num_threats):
        super().__init__()  # Ensure the base class is initialized
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)

        # Add agents to the grid and schedule
        for i in range(num_animals):
            animal = AnimalAgent(i, self)
            self.grid.place_agent(animal, (self.random.randrange(width), self.random.randrange(height)))
            self.schedule.add(animal)

        for i in range(num_patrols):
            patrol = PatrolAgent(num_animals + i, self)
            self.grid.place_agent(patrol, (self.random.randrange(width), self.random.randrange(height)))
            self.schedule.add(patrol)

        for i in range(num_threats):
            threat = ThreatAgent(num_animals + num_patrols + i, self)
            self.grid.place_agent(threat, (self.random.randrange(width), self.random.randrange(height)))
            self.schedule.add(threat)

    def step(self):
        self.schedule.step()
