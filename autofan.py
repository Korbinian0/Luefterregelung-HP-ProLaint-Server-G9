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

# CPU temperature limits in degrees Celsius
CPUTEMP_01=30
CPUTEMP_02=40
CPUTEMP_03=45
CPUTEMP_04=47
CPUTEMP_05=49
CPUTEMP_06=51
CPUTEMP_07=53
CPUTEMP_08=55
CPUTEMP_09=60
CPUTEMP_10=64
CPUTEMP_11=68		## all fans

# Fan speeds in speed steps
FANSPEED_00="1"     ## minimum fanspeed
FANSPEED_01="24"
FANSPEED_02="44"
FANSPEED_03="55"
FANSPEED_04="65"
FANSPEED_05="80"
FANSPEED_06="100"
FANSPEED_07="120"
FANSPEED_08="140"
FANSPEED_09="180"
FANSPEED_10="225"
FANSPEED_11="255"	## all fans

# read the CPU-temperatures
result = subprocess.check_output(["sensors"], universal_newlines=True)
match = re.search(r"Core 0:\s+\+\d+\.\d+°C", result)
if match:
            temp_1_str = match.group(0)
            temp_1 = float(temp_1_str.split(":")[1].strip()[:-2])



def get_package_temp(sensor_id, package_id):
    """
    Reads the temperature of the specified package from sensors output.
    """
    try:
        result = subprocess.check_output(["sensors"], universal_newlines=True)
        # Search for the specific sensor and package
        sensor_pattern = rf"{sensor_id}\n(?:.*\n)*?Package id {package_id}:\s+\+(\d+\.\d+)°C"
        match = re.search(sensor_pattern, result)
        if match:
            return float(match.group(1))
        else:
            print(f"Temperature for {sensor_id} package id {package_id} not found.")
            return None
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing sensors: {e}")
        return None

temp_1 = get_package_temp("coretemp-isa-0000", 0)
temp_2 = get_package_temp("coretemp-isa-0001", 1)


# Print Temp 
print=("CPU 1:", temp_1, "°C")		#CPU 1 Temp print
print=("CPU 2:", temp_2, "°C")		#CPU 2 Temp print


# If the temperature of CPU 2 cannot be read, it is set to half the temperature of CPU 1
if temp_2 is None and temp_1 is not None:
    temp_2 = temp_1 / 2

# If CPU Temp is greater than or equal to CPUTEMP_11, CPU Temp is set to CPU Temp
if temp_1 > CPUTEMP_11:
    temp_2 = temp_1

if temp_2 > CPUTEMP_11:
    temp_1 = temp_2


# Setting fan speed via SSH commands to iLO

# CPU 1
if temp_1 > CPUTEMP_11:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_10:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_09:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_08:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_07:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_06:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_05:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_04:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_03:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_02:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > CPUTEMP_01:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)


# CPU 2
if temp_2 > CPUTEMP_11:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_10:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS}{USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_09:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_08:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_07:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_06:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_05:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_04:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_03:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_02:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > CPUTEMP_01:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)



