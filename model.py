from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import AnimalAgent, PatrolAgent, HunterAgent, FoodAgent, WaterAgent

class MultiAgentModel(Model):
    def __init__(self, width, height, num_animals, num_patrols, num_hunters):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)

        # Randomly locate water agents(static)
        for _ in range(200):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            water = WaterAgent(self.next_id(), self)
            self.grid.place_agent(water, (x, y))
            self.schedule.add(water)

        # Randomly locate food agents(static)
        for _ in range(2000):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            food = FoodAgent(self.next_id(), self)
            self.grid.place_agent(food, (x, y))
            self.schedule.add(food)
              

        # Add Animal Agents
        for _ in range(num_animals):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            animal = AnimalAgent(self.next_id(), self)
            self.grid.place_agent(animal, (x, y))
            self.schedule.add(animal)

         # Add Patrol Agents
        for _ in range(num_patrols):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            patrol = PatrolAgent(self.next_id(), self)
            self.grid.place_agent(patrol, (x, y))
            self.schedule.add(patrol)
        
        # Add Hunter Agents
        for _ in range(num_hunters):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            hunter = HunterAgent(self.next_id(), self)
            self.grid.place_agent(hunter, (x, y))
            self.schedule.add(hunter)
    
    def random_position(self):
        """Get a random position within the grid."""
        return self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)


    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
