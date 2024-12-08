from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import ForestModel

def agent_portrayal(agent):
    portrayal = {"Layer": 1}  # Default layer for all agents
    if isinstance(agent, AnimalAgent):
        portrayal.update({"Shape": "circle", "Color": "green", "r": 0.5})
    elif isinstance(agent, PatrolAgent):
        portrayal.update({"Shape": "rect", "Color": "blue", "w": 0.5, "h": 0.5})
    elif isinstance(agent, ThreatAgent):
        portrayal.update({"Shape": "triangle", "Color": "red", "r": 0.5})
    return portrayal


grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(
    ForestModel,
    [grid],
    "Wildlife Conservation MAS",
    {"width": 20, "height": 20, "num_animals": 10, "num_patrols": 3, "num_threats": 2},
)
server.port = 8521
server.launch()
