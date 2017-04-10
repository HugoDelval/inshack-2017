#!/usr/bin/python3
import os
from multiprocessing import Pool, TimeoutError
import subprocess
import time

timeout = 240

def get_chall_name(challenge):
    challenge_name = challenge.split("-")[:-1]
    while challenge_name[-1] == "":
        challenge_name = challenge_name[:-1]
    return "-".join(challenge_name)


def get_challenges_paths():
    challenges = []
    parent_dir = "/challenges"
    for category in os.listdir(parent_dir):
        category_path = parent_dir + "/" + category
        if os.path.isdir(category_path):
            for challenge in os.listdir(category_path):
                challenge_path = category_path + "/" + challenge
                if os.path.isdir(challenge_path):
                    challenge_name = get_chall_name(challenge)
                    challenges.append((challenge_name, challenge_path))
    return challenges


def exploit(chall_name, path):
    exploitable = False
    try:
        p = subprocess.run([path + "/exploit/exploit.py"], stdout=subprocess.PIPE, timeout=timeout)
        if p.returncode == 0 and p.stdout == b"True\n":
            exploitable = True
    except Exception as e:
        print("Got an exception while trying to exploit " + chall_name + ": \n" + str(e) + "\n")
    return chall_name, exploitable


def exploit_challenges():
    challenges = get_challenges_paths()
    status = {n: False for n,_ in challenges}
    start = time.time()
    results = []
    with Pool(processes=len(challenges)) as pool:
        multiple_results = [pool.apply_async(exploit, (name,path,)) for name, path in challenges]
        for res in multiple_results:
            try:
                results.append(res.get(timeout=timeout+1))
            except TimeoutError:
                print("Got a timeout.")
    duration = time.time() - start
    print("All challenges exploited in " + str(duration) + " sec.")
    for chall_name, exploitable in results:
        status[chall_name] = exploitable
    return status

def dump_in_file(status):
    import json
    with open("/app/status.json", 'w') as f:
        json.dump(status, f)


if __name__ == "__main__":
    status = exploit_challenges()
    dump_in_file(status)
