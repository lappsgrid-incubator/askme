"""stop.py

Stopping AskMe components.

"""

import sys, subprocess

jps = subprocess.run(["jps"], capture_output=True)
processes = jps.stdout.decode().split('\n')

def kill_pid(pid: str, pname: str):
    print(f'killing {pid} {pname}')
    subprocess.run(['kill', pid])                                                                                                                                         

component = sys.argv[1] if len(sys.argv) > 1 else 'all'
for process in processes:
    if not process:
        continue
    pid, pname = process.split()
    for askme_process in ('elastic', 'query', 'ranking', 'web'):
        if pname.startswith(askme_process) and (component == 'all' or component in pname):
            kill_pid(pid, pname)
