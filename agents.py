from mesa import Agent
import random

class AnimalAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        #move randomly
        self.random_move()

    def random_move(self):
        # Get all possible neighboring cells
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        # Pick a random new position
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)



class PatrolAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Chase the nearest hunter
        self.chase_hunter()
        
    def chase_hunter(self):
        # Find the closest hunter
        closest_hunter = None
        closest_distance = float('inf')

        for agent in self.model.schedule.agents:
            if isinstance(agent, HunterAgent):
                distance = self.get_distance(self.pos, agent.pos)
                if distance < closest_distance:
                    closest_hunter = agent
                    closest_distance = distance

        # Move one step closer to the closest hunter
        if closest_hunter:
            next_step = self.get_closer_position(self.pos, closest_hunter.pos)
            self.model.grid.move_agent(self, next_step)

    def get_closer_position(self, current_pos, target_pos):
        """Get the next step closer to the target position."""
        current_x, current_y = current_pos
        target_x, target_y = target_pos
        dx = target_x - current_x
        dy = target_y - current_y

        new_x = current_x + (1 if dx > 0 else -1 if dx < 0 else 0)
        new_y = current_y + (1 if dy > 0 else -1 if dy < 0 else 0)

        return new_x, new_y
    
    def get_distance(self, pos1, pos2):
        """
        Calculate the Euclidean distance between two positions.

        Parameters:
        - pos1: Tuple[int, int], the (x, y) position of the first agent.
        - pos2: Tuple[int, int], the (x, y) position of the second agent.

        Returns:
        - float: The Euclidean distance between pos1 and pos2.
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    

class HunterAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Move towards the nearest animal
        self.move_towards_animal()

    def move_towards_animal(self):
        # Find the closest animal
        closest_animal = None
        closest_distance = float('inf')

        for agent in self.model.schedule.agents:
            if isinstance(agent, AnimalAgent):
                distance = self.get_distance(self.pos, agent.pos)
                if distance < closest_distance:
                    closest_animal = agent
                    closest_distance = distance

     # Move one step closer to the closest animal
        if closest_animal:
            next_step = self.get_closer_position(self.pos, closest_animal.pos)
            self.model.grid.move_agent(self, next_step)

    def get_closer_position(self, current_pos, target_pos):
        """Get the next step closer to the target position."""
        current_x, current_y = current_pos
        target_x, target_y = target_pos
        dx = target_x - current_x
        dy = target_y - current_y

        new_x = current_x + (1 if dx > 0 else -1 if dx < 0 else 0)
        new_y = current_y + (1 if dy > 0 else -1 if dy < 0 else 0)

        return new_x, new_y
    def get_distance(self, pos1, pos2):
        """
        Calculate the Euclidean distance between two positions.

        Parameters:
        - pos1: Tuple[int, int], the (x, y) position of the first agent.
        - pos2: Tuple[int, int], the (x, y) position of the second agent.

        Returns:
        - float: The Euclidean distance between pos1 and pos2.
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    


class FoodAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class WaterAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

