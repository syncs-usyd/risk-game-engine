# Risk Game Engine

This repository contains the game engine for SYNCS Bot Battle 2024. This year, we're playing the <em><a href="https://store.steampowered.com/app/1128810/RISK_Global_Domination/">Risk: Global Domination</a></em>. If you've never heard of it, the game is free to play on Steam and is really fun!

# Core Components

`engine`
The engine Python module is where everything to do with the game engine exists. It contains the game state, input handlers, output helpers and config.

`submissionhelper`
The submissionhelper Python module is an API to make communicating with the game engine easier for submissions. It provides the BotBattle class, which has helper methods for getting game information and playing moves. It also has helpful info classes for the various game information the engine provides.


