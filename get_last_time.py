from sys import argv
from sys import exit as exit_
from paramiko import SSHClient, AutoAddPolicy

server = argv[1]

# PARAMS
port = 22
login = "admin"
passwords = ["qwerty-bc", "intel"]
timeout = 100

acceptTime = 24 # time (in hours) accepted for not-recording
returns = {
    "TimeGood": 0,
    "TimeBad": 1,
    "ConnFailed": 2,
    "ExecError": 3,
}

# WORK
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())

for idx, s in enumerate(passwords):
    try:
        ssh.connect(hostname=server, username=login, password=s, port=port, timeout=timeout)
    except:
        if idx == len(passwords) - 1:
            print(returns["ConnFailed"])
            exit_()
        else:
            continue
    else:
        break

try:
    stdin, stdout, stderr = ssh.exec_command("printPart")

    data = stdout.read().decode()
    data = data[data.index("lastWriteTime") : data.index("wrFiles")]
    data = data.split()

    date1 = data[0].split(":")[1]
    date1 = date1.split("-")
    date1 = [int(s) for s in date1]

    time1 = data[1]
    time1 = time1.split(":")
    time1 = [int(s) for s in time1]

    stdin, stdout, stderr = ssh.exec_command("date -I")
    data = stdout.read().decode().split("-")
    date2 = [int(s) for s in data]

    stdin, stdout, stderr = ssh.exec_command("date")
    data = stdout.read().decode().split()
    time2 = data[3].split(":")
    time2 = [int(s) for s in time2]
except:
    print(returns["ExecError"])
    exit_()
finally:
    ssh.close()

if len(date1) + len(date2) + len(time1) + len(time2) != 12:
    print(returns["ExecError"])
    exit_()

if (date1[0] < 0) or not (1 <= date1[1] <= 12) or not (1 <= date1[2] <= 31):
    print(returns["ExecError"])
    exit_()
if not (0 <= time1[0] <= 23) or not (0 <= time1[1] <= 59) or not (0 <= time1[2] <= 59):
    print(returns["ExecError"])
    exit_()
if (date2[0] < 2019) or not (1 <= date2[1] <= 12) or not (1 <= date2[2] <= 31):
    print(returns["ExecError"])
    exit_()
if not (0 <= time2[0] <= 23) or not (0 <= time2[1] <= 59) or not (0 <= time2[2] <= 59):
    print(returns["ExecError"])
    exit_()

difference = [a - date1[idx] for idx, a in enumerate(date2)]
difference.append(time2[0] - time1[0])
difference[0] = difference[0] * 12 * 30 * 24
difference[1] = difference[1] * 30 * 24
difference[2] = difference[2] * 24

result = sum(difference)
if result > acceptTime:
    print(returns["TimeBad"])
    exit_()
else:
    print(returns["TimeGood"])
    exit_()

input()