import json
import shutil
from signal import SIGKILL
import subprocess
import sys
import os
from typing import Tuple

NUM_PLAYERS = 5
PIPE_PERMISSIONS = 0o660
FILE_PERMISSIOSN = 0o664
DIRECTORY_PERMISSIONS = 0o775

def main():
    
    # python3 match_simulator.py --submissions 3:example_submissions/example.py 2:example_submissions/example2.py --engine
    
    commands = parse_cmd_args(sys.argv[1:])

    try:
        sources = [(int(x.split(":")[0]), x.split(":")[1]) for x in commands["--submissions"]]
    except ValueError:
        print_usage()

    if sum([x[0] for x in sources]) != NUM_PLAYERS:
        print(f"Total players in the match must be {NUM_PLAYERS}.")
        print_usage()

    setup_environments(sources)
    submission_pids = start_submissions()

    if "--engine" in commands:
        if len(commands["--engine"]) != 0:
            print_usage()
        start_engine()

    else:
        print("Once you have finished running the engine, press [Enter] to terminate any still-running submission processes.")
        input()
    
    for pid in submission_pids:
        print(f"[simulator]: terminating submission pid {pid}.")
        os.kill(pid, SIGKILL)

    print("[simulator] simulation complete.")


def parse_cmd_args(args: list[str]):
    commands = {}

    current_command = None
    for arg in args:
        if arg[:2] == "--":
            current_command = arg
            commands[current_command] = []
            continue
        
        if current_command == None:
            print_usage()

        commands[current_command].append(arg)

    for command in commands.keys():
        if command not in ["--submissions", "--engine"]:
            print_usage()

    return commands


def print_usage():
    print(
    "Usage: python3 match_simulator.py [options]\n"
    "   options:\n"
    "       --submissions {<count> | d}:<path> ...      Sets the source files for the submissions to run in this match. If <count> is specified, <count> copies\n"
    "                                                       of the submission will play in the match, else if 'd' is specified a single copy will play and it\n"
    "                                                       will not be automatically started.\n"
    "       --engine                                    If present, the simulator will start the engine. To run the match without this flag you need to manually\n"
    "                                                       start the engine (for example, while debugging it).\n"
    "\n"
    "   examples:\n"
    "       python3 match_simulator.py --submissions 5:example_submissions/complex.py --engine\n"
    "       python3 match_simulator.py --submissions 2:example_submissions/complex.py 3:my_submission.py --engine\n"
    "       python3 match_simulator.py --submissions 4:example_submissions/complex.py d:my_submission.py --engine\n")
    sys.exit(0)


def setup_environments(sources: list[Tuple[int, str]]):
    shutil.rmtree("output", ignore_errors=True)
    os.mkdir("output")
    shutil.rmtree("input", ignore_errors=True)
    os.mkdir("input")

    count = 0
    source = sources.pop(0)
    for player in range(NUM_PLAYERS):
        if count >= source[0]:
            count = 0
            source = sources.pop()

        clean_environment_for_player(player)
        setup_environment_for_player(player, source[1])

        count += 1

    catalog = [{ "team_id": i } for i in range(NUM_PLAYERS)]
    with open(f"input/catalog.json", "w") as f:
        f.write(json.dumps(catalog))



def start_submissions() -> list[int]:
    player_pids = []
    for player in range(NUM_PLAYERS):
        os.chdir(f"submission{player}")

        with open("io/submission.log", "w") as f_log, open("io/submission.err", "w") as f_err:
            process = subprocess.Popen(["python3", "submission.py"], stdout=f_log, stderr=f_err)
        
        player_pids.append(process.pid)
        print(f"[simulator]: started submission {player} (pid={process.pid}).")
        os.chdir("..")

    return player_pids


def start_engine():
    print("[simulator] started engine.")
    with open("output/engine.log", "w") as f_log, open("output/engine.err", "w") as f_err:
        process = subprocess.Popen(["python3", "-m", "risk_engine", "--print-recording-interactive"], stdout=subprocess.PIPE, stderr=f_err, text=True, universal_newlines=True, bufsize=1)

        while True:
            if process.stdout is not None:
                data = process.stdout.read(1)
                if not data:
                    break
                print(data, end="", flush=True)
                f_log.write(data)

    print("[simulator] engine terminated.")

def setup_environment_for_player(player: int, source: str):
    os.makedirs(f"submission{player}/io", mode=DIRECTORY_PERMISSIONS)
    os.mkfifo(f"submission{player}/io/to_engine.pipe", mode=PIPE_PERMISSIONS)
    os.mkfifo(f"submission{player}/io/from_engine.pipe", mode=PIPE_PERMISSIONS)
    shutil.copy(source, f"submission{player}/submission.py")


def clean_environment_for_player(player: int):
    shutil.rmtree(f"submission{player}", ignore_errors=True)


if __name__ == "__main__":
    main()