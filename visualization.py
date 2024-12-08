from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import MultiAgentModel
from agents import AnimalAgent, PatrolAgent, HunterAgent, FoodAgent, WaterAgent

def agent_portrayal(agent):
    if isinstance(agent, FoodAgent):
        return {"Shape": "rect", "Color": "lightgreen", "Filled": True, "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, WaterAgent):
        return {"Shape": "rect", "Color": "lightblue", "Filled": True, "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, AnimalAgent):
        return {"Shape": "circle", "Color": "black", "Filled": True, "Layer": 1, "r": 0.9}
    elif isinstance(agent, PatrolAgent):
        return {"Shape": "circle", "Color": "orange", "Filled": True, "Layer": 2, "r": 0.9}
    elif isinstance(agent, HunterAgent):
        return {"Shape": "circle", "Color": "red", "Filled": True, "Layer": 3, "r": 0.9}
    return {}

grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
server = ModularServer(
    MultiAgentModel,
    [grid],
    "Multi-Agent System Simulation",
    {"width": 50, "height": 50, "num_animals": 100, "num_patrols": 5, "num_hunters": 50},
)


server.port = 8532
