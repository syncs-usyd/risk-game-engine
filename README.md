# Risk Game Engine

This repository contains the game engine for SYNCS Bot Battle 2024. This year, we're playing Risk: Global Domination.

# Repository Structure

`example_submissions`
This folder contains examples that you can use to help design your own bot.

`risk-shared`
The risk-shared package contains python code and classes that are used in both the `risk-engine` and `risk-helper` packages.

`risk-engine`
The risk-engine package contains the game engine which is used to run matches and determine the winner of a match by simulating the game.

`risk-helper`
The risk-helper package contains a helper library you can use to greatly simplify interactions with the game engine.

# Guide

This guide will explain how to create your own submission and run simulations on your own computer, this guide is designed for Linux, WSL2, or MacOS.

1. Run `chmod u+x setup_env.sh`, this will give execute permissions to the script so that you can run it.
2. Run `./setup_env.sh`, this will install the `risk-engine`, `risk-shared` and `risk-helper` packages.
3. Make a copy of an example submission such as `example_submissions/simple.py` and place it somewhere you want (we will assume you have placed it at `./my_submission.py`). Make any modifications to this file that you want to design your bot.
4. To simulate a match, use the `match_simulator.py` script. For example we could run `python3 match_simulator.py --submissions 4:example_submissions/simple.py 1:my_submission.py --engine` to simulate a match between our submission and four of the simple example submissions.

Now you can simulate matches on your own device. We will briefly explain the new folders that are created when you run the `match_simulator.py` script. The folders `submission0` to `submission4` contain the code for each player in the simulated game, as well as two special files (FIFO pipes) that are used to communicate to and from the engine (these are `to_engine.pipe` and `from_engine.pipe`). 
The `input` folder contains `catalog.json`. The `output` folder contains the results of the game, `results.json` describes who won if the game was successful, otherwise it may describe who was banned or why the match was cancelled. The `game.json` file contains the game recording, which is the same data displayed on the website in the match history page. The `visualiser_backwards_differential.json` and `visualiser_forwards_differential.json` are used to generate the map visualisation on the website. The `submission_x.err` and `submission_x.log` are the STDERR and STDOUT of each submission respectively.