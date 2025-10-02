## Creator Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
###################

# Import libraries
import subprocess
import re
import time

# Access data for iLO
PASSWORD="PASSWORT"
USERNAME="USERNAME"
ILOIP="XXX.XXX.XXX.XXX"
# Encryption routine for SSH connection
SSHOPTS="SSHOPTS"

# Fan Test
cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {20}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {40}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {60}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {80}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {100}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {120}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {140}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {160}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {180}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {200}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {220}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {240}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {255}'"
subprocess.call(cmd, shell=True)

time.sleep(5)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {240}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {220}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {200}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {180}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {160}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {140}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {120}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {100}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {80}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {60}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {40}'"
subprocess.call(cmd, shell=True)

time.sleep(1)

cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {0-7} max {20}'"
subprocess.call(cmd, shell=True)