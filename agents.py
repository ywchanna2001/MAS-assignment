from mesa import Agent
import random

class AnimalAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        #move randomly
        self.random_move()

    def random_move(self):
        if self.pos is None:
            return  # Skip movement if the agent is not on the grid
        # Get all possible neighboring cells
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        # Pick a random new position
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)



class PatrolAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Check if there are any hunters in the forest
        hunters_present = any(isinstance(agent, HunterAgent) for agent in self.model.schedule.agents)
        
        if hunters_present:
            # Try to arrest hunters if possible
            if self.try_arrest_hunter():
                return  # Stop the step if a hunter was arrested
            # Chase the nearest hunter
            self.chase_hunter()
        else:
            # Move randomly if no hunters are present
            self.random_move()

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

    def try_arrest_hunter(self):
        """
        Arrest the hunter if present at the same location.
        Returns True if a hunter is arrested, otherwise False.
        """
        # Check if there are hunters at the same position
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, HunterAgent):
                # Arrest the hunter by removing them from the grid and schedule
                self.model.grid.remove_agent(agent)
                self.model.schedule.remove(agent)
                print(f"Hunter {agent.unique_id} arrested by Patrol {self.unique_id}!")
                return True  # Hunter arrested
        return False  # No hunter arrested

    def random_move(self):
        if self.pos is None:
            return  # Skip movement if the agent is not on the grid
        # Get all possible neighboring cells
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        # Pick a random new position
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

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
        if  pos2 is None:
            return float('inf')  # If either position is None, treat distance as infinite
        else:
            x1, y1 = pos1
            x2, y2 = pos2
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


    
class HunterAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Check if there are any animal in the forest
        animals_present = any(isinstance(agent, AnimalAgent) and agent.pos is not None for agent in self.model.schedule.agents)

        if animals_present:
                # Try to hunt animals if possible
                if self.try_hunt_animals():
                    return  # Stop the step if a animal was hunted
                # Chase the nearest animal
                self.move_towards_animal()

        else:
            # Move randomly if no hunters are present
            self.random_move()

    def move_towards_animal(self):
        # Find the closetst animal
        closest_animal = None
        closest_distance = float('inf')

        # Find the closest animal
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

    
    def random_move(self):
        if self.pos is None:
            return  # Skip movement if the agent is not on the grid
        # Get all possible neighboring cells
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        # Pick a random new position
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    
    
    def try_hunt_animals(self):
        """
        Hunt the animal if present at the same location.
        Returns True if an animal is hunted, otherwise False.
        """
        if self.pos is None:
            return False  # Agent is not on the grid, so skip hunting

        # Check for animals at the same position
        if self.pos is not None:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            # Process cellmates

        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        for agent in cellmates:
            if isinstance(agent, AnimalAgent):
                # Remove the animal from the grid and schedule
                self.model.grid.remove_agent(agent)
                self.model.schedule.remove(agent)
                print(f"Animal {agent.unique_id} hunted by Hunter {self.unique_id}!")
                return True  # Animal hunted
        return False  # No animal found

    
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
        if pos2 is None or pos1 is None:
            return float('inf')  # Treat missing positions as infinitely distant
        else:
            x1, y1 = pos1
            x2, y2 = pos2
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    
class FoodAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class WaterAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

