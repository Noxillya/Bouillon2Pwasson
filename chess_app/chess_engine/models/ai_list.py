from chess_engine.models.ai_algorithm.randomAI import RandomAI
from chess_engine.models.ai_algorithm.bouillon2pwasson import Bouillon2Pwasson
from chess_engine.models.base import AI

AI_LIST: dict[str, type[AI]] = {
    "random": RandomAI,
    "b2p": Bouillon2Pwasson,
}