from mesa import Agent

class BaseAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class AnimalAgent(BaseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0
        self.thirst = 0

    def step(self):
        self.hunger += 1
        self.thirst += 1
        if self.thirst > 10:
            self.seek_water()
        elif self.hunger > 10:
            self.seek_food()
        else:
            self.random_move()

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def seek_water(self):
        water_cells = self.model.get_resource_locations("water")
        if water_cells:
            new_position = self.random.choice(water_cells)
            self.model.grid.move_agent(self, new_position)

    def seek_food(self):
        food_cells = self.model.get_resource_locations("food")
        if food_cells:
            new_position = self.random.choice(food_cells)
            self.model.grid.move_agent(self, new_position)

class PatrolAgent(BaseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.random_move()
        threats = self.model.get_threats_nearby(self.pos)
        if threats:
            self.report_threat(threats)

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def report_threat(self, threats):
        for threat in threats:
            print(f"Threat detected at {threat.pos} by Patrol Agent {self.unique_id}")

class ThreatAgent(BaseAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.random_move()

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
