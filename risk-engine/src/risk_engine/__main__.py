import sys
from risk_engine.game_engine import GameEngine

game = GameEngine(len(sys.argv) > 1 and sys.argv[1] == "--print-recording-interactive")
game.start()