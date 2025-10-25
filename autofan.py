## Creator Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
#################################################################################################################

# Import libraries
import subprocess
import re
import time

# Access data for iLO and IPMI
PASSWORD="PASSWORT"
USERNAME="USERNAME"
ILOIP="XXX.XXX.XXX.XXX"
IPMIUSER="IPMIUSER"
IPMIPW="IPMIPW"
# Encryption routine for SSH connection
SSHOPTS="SSHOPTS"

#IPMI Sensor Names
Chipset="XX-Chipset"
HDMax="XX-HD Max"
HDController="XX-HD Controller"
ILOZone="XX-ILO Zone"
Batteryzone="XX-Battery Zone"
VRP1="XX-VRP1"
VRP2="XX-VRP2"
StorageBatt="XX-Storage Batt"
HDCntlrZone="XX-HD Cntlr Zone "


# Temperature limits in degrees Celsius
TEMP_01=30
TEMP_02=40
TEMP_03=45
TEMP_04=47
TEMP_05=49
TEMP_06=51
TEMP_07=53
TEMP_08=55
TEMP_09=60
TEMP_10=64
TEMP_11=68		## all fans

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


# Read IPMI temperature 
def get_sensor_data():
    command = ['ipmitool', '-I', 'lanplus', '-H', ILOIP, '-U', IPMIUSER, '-P', IPMIPW, 'sensor']
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Fehler beim Ausführen des ipmitool-Befehls: {result.stderr}")
        return None
    
    # Regex for extracting temperature values
    pattern = r"\| (\d+-\S+) \| (\d+\.\d+|\d+) \| degrees C \| ok    "
    matches = re.findall(pattern, result.stdout)
    
    # Save temperature values in a dictionary
    temperatures = {match[0]: float(match[1]) for match in matches}
    
    return temperatures

# Request and process data from ipmitool
temperatures = get_sensor_data()
if temperatures:
    # Dictionary for the assignment of sensor names to variable names
    sensor_vars = {
        'Chipset': 'Chipset_TEMP',
        'HDMax': 'HD_Max_TEMP',
        'HDController': 'HD_Controller_TEMP',
        'ILOZone': 'ILO_Zone_TEMP',
        'Batteryzone': 'Battery_Zone_TEMP',
        'VRP1': 'VRP1_TEMP',
        'VRP2': 'VRP2_TEMP',
        'StorageBatt': 'Storage_Batt_TEMP',
        'HDCntlrZone': 'HD_Cntlr_Zone'
    }
    
    for sensor, var_name in sensor_vars.items():
        if sensor in temperatures:
            temp = temperatures[sensor]
            print(f"Die Temperatur von {sensor} beträgt {temp} degrees C")
            
            # Assign the temperature to a variable named after the sensor
            globals()[var_name] = temp
            print(f"Variablen {var_name}: {globals()[var_name]}")
else:
    print("Keine Sensordaten gefunden.")

# Set Temp in Variabl
if all(sensor in globals() for sensor in ['Chipset_TEMP', 'HD_Max_TEMP', 'ILO_Zone_TEMP', 'Battery_Zone_TEMP', 'VRP1_TEMP', 'VRP2_TEMP', 'Storage_Batt_TEMP', 'HD_Cntlr_Zone']):
    chipset_temp = globals()['Chipset_TEMP']
    hdmax_temp = globals()['HD_Max_TEMP']
    HDController_temp = globals()['HD_Controller_TEMP']
    ilozone_temp = globals()['ILO_Zone_TEMP']
    Batteryzone_temp = globals()['Batter_Zonr_TEMP']
    VRP1_temp = globals()['VRP1_TEMP']
    VRP2_temp = globals()['VRP2_TEMP']
    StorageBatt_temp = ()['Storage_Batt_TEMP']
    HDCntlrZone_temp = ()['HD_Cntlr_Zone']

# Print Temp 
print=("CPU 1:", temp_1, "°C")		                    #CPU 1 Temp print
print=("CPU 2:", temp_2, "°C")		                    #CPU 2 Temp print
print=("Chipset", ":", Chipset, "°C")                   #Chipset Temp print
print=("HD Max", ":", HDMax, "°C")                      #HD Max Temp print
print=("HD Controller", ":", HDController, "°C")        #HD Controller Temp print
print=("ILO Zone", ":", ILOZone, "°C")                  #ILO Zone Temp print
print=("Battery Zone", ":", Batteryzone, "°C")          #Battery Zone Temp print
print=("VRP1", ":", VRP1, "°C")                         #VRP1 Temp print
print=("VRP2", ":", VRP2, "°C")                         #VRP2 Temp print
print=("Storage Batt", ":", StorageBatt, "°C")          #Storage Batt Temp print
print=("HD Cntlr Zone", ":", HDCntlrZone, "°C")         #HD Cntlr Zone Temp print


# If the temperature of CPU 2 cannot be read, it is set to half the temperature of CPU 1
if temp_2 is None and temp_1 is not None:
    temp_2 = temp_1 / 2

# If CPU Temp is greater than or equal to CPUTEMP_11, CPU Temp is set to CPU Temp
if temp_1 > TEMP_11:
    temp_2 = temp_1

if temp_2 > TEMP_11:
    temp_1 = temp_2


# Setting fan speed via SSH commands to iLO

# Additional cooling if chipset temperature is too high and CPU 1 temperature is low
if chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_11 and temp_1 <= TEMP_11:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_10 and temp_1 <= TEMP_10:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_09 and temp_1 <= TEMP_09:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_08 and temp_1 <= TEMP_08:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_07 and temp_1 <= TEMP_07:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_06 and temp_1 <= TEMP_06:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_05 and temp_1 <= TEMP_05:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_04 and temp_1 <= TEMP_04:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_03 and temp_1 <= TEMP_03:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_02 and temp_1 <= TEMP_02:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}"
        subprocess.call(cmd, shell=True)

elif chipset_temp is not None and temp_1 is not None and chipset_temp >= TEMP_01 and temp_1 <= TEMP_01:
    for i in range(5, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}"
        subprocess.call(cmd, shell=True)

else:
    for i in range(5, 7):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}"
        subprocess.call(cmd, shell=True)

# Additional cooling if HD Controller temperature is too high and CPU 1 temperature is low
if HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_11 and temp_1 <= TEMP_11:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_10 and temp_1 <= TEMP_10:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_09 and temp_1 <= TEMP_09:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_08 and temp_1 <= TEMP_08:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_07 and temp_1 <= TEMP_07:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_06 and temp_1 <= TEMP_06:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_05 and temp_1 <= TEMP_05:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_04 and temp_1 <= TEMP_04:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_03 and temp_1 <= TEMP_03:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_02 and temp_1 <= TEMP_02:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif HDController_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_01 and temp_1 <= TEMP_01:
    for i in range(3, 5):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(3, 5):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)

# Additional cooling if HD Max temperature is too high and CPU 1 temperature is low
if hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_11 and temp_1 <= TEMP_11:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_10 and temp_1 <= TEMP_10:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_09 and temp_1 <= TEMP_09:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_08 and temp_1 <= TEMP_08:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_07 and temp_1 <= TEMP_07:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_06 and temp_1 <= TEMP_06:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_05 and temp_1 <= TEMP_05:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_04 and temp_1 <= TEMP_04:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_03 and temp_1 <= TEMP_03:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_02 and temp_1 <= TEMP_02:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif hdmax_temp is not None and temp_1 is not None and hdmax_temp >= TEMP_01 and temp_1 <= TEMP_01:
    for i in range(0, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(0, 7):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)

# Additional cooling if ILO Zone temperature is too high and CPU 1 temperature is low
if ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_11 and temp_1 <= TEMP_11:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_10 and temp_1 <= TEMP_10:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_09 and temp_1 <= TEMP_09:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_08 and temp_1 <= TEMP_08:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_07 and temp_1 <= TEMP_07:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_06 and temp_1 <= TEMP_06:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_05 and temp_1 <= TEMP_05:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_04 and temp_1 <= TEMP_04:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_03 and temp_1 <= TEMP_03:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_02 and temp_1 <= TEMP_02:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif ilozone_temp is not None and temp_1 is not None and ilozone_temp >= TEMP_01 and temp_1 <= TEMP_01:
    for i in range(3, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(3, 6):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)

# Additional cooling if Battery Zone temperature is too high and CPU 1 temperature is low
if Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_11 and temp_1 <= TEMP_11:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_10 and temp_1 <= TEMP_10:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_09 and temp_1 <= TEMP_09:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_08 and temp_1 <= TEMP_08:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_07 and temp_1 <= TEMP_07:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_06 and temp_1 <= TEMP_06:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_05 and temp_1 <= TEMP_05:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_04 and temp_1 <= TEMP_04:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_03 and temp_1 <= TEMP_03:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_02 and temp_1 <= TEMP_02:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif Batteryzone_temp is not None and temp_1 is not None and Batteryzone_temp >= TEMP_01 and temp_1 <= TEMP_01:
    for i in range(2, 4):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(2, 4):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)

# Additional cooling if VRP1 temperature is too high and CPU 1 temperature is low
if VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_11 and temp_1 <= TEMP_11:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_10 and temp_1 <= TEMP_10:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_09 and temp_1 <= TEMP_09:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_08 and temp_1 <= TEMP_08:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_07 and temp_1 <= TEMP_07:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_06 and temp_1 <= TEMP_06:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_05 and temp_1 <= TEMP_05:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_04 and temp_1 <= TEMP_04:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_03 and temp_1 <= TEMP_03:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_02 and temp_1 <= TEMP_02:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif VRP1_temp is not None and temp_1 is not None and VRP1_temp >= TEMP_01 and temp_1 <= TEMP_01:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(4, 6):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)

# Additional cooling if VRP2 temperature is too high and CPU 2 temperature is low
if VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_11 and temp_2 <= TEMP_11:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_10 and temp_2 <= TEMP_10:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_09 and temp_2 <= TEMP_09:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_08 and temp_2 <= TEMP_08:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_07 and temp_2 <= TEMP_07:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_06 and temp_2 <= TEMP_06:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_05 and temp_2 <= TEMP_05:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_04 and temp_2 <= TEMP_04:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_03 and temp_2 <= TEMP_03:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_02 and temp_2 <= TEMP_02:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif VRP2_temp is not None and temp_2 is not None and VRP2_temp >= TEMP_01 and temp_2 <= TEMP_01:
    for i in range(0, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(0, 6):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)

# Additonal cooling if Storage Batt temperature is too high and CPU 1 temperature is low
if StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_11 and temp_1 <= TEMP_11:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_10 and temp_1 <= TEMP_10:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_09 and temp_1 <= TEMP_09:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_08 and temp_1 <= TEMP_08:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_07 and temp_1 <= TEMP_07:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_06 and temp_1 <= TEMP_06:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_05 and temp_1 <= TEMP_05:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_04 and temp_1 <= TEMP_04:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_03 and temp_1 <= TEMP_03:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_02 and temp_1 <= TEMP_02:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif StorageBatt_temp is not None and temp_1 is not None and StorageBatt_temp >= TEMP_01 and temp_1 <= TEMP_01:
    for i in range(4, 6):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(4, 6):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)

# Additonal cooling if HD Cntrl Zone temperature is too high and CPU 1 temperature is low
if HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_11 and temp_1 <= TEMP_11:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_10 and temp_1 <= TEMP_10:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_09 and temp_1 <= TEMP_09:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_08 and temp_1 <= TEMP_08:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_07 and temp_1 <= TEMP_07:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_06 and temp_1 <= TEMP_06:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_05 and temp_1 <= TEMP_05:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_04 and temp_1 <= TEMP_04:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_03 and temp_1 <= TEMP_03:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_02 and temp_1 <= TEMP_02:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif HDCntlrZone_temp is not None and temp_1 is not None and HDCntlrZone_temp >= TEMP_01 and temp_1 <= TEMP_01:
    for i in range(4, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(4, 7):
        cmd = f"ssshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan ü {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)


# CPU 1
if temp_1 > TEMP_11:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_10:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_09:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_08:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)   

elif temp_1 > TEMP_07:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_06:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_05:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_04:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_03:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_02:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif temp_1 > TEMP_01:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(3, 7):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)

# CPU 2
if temp_2 > TEMP_11:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_11}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_10:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS}{USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_10}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_09:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_09}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_08:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_08}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_07:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_07}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_06:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_06}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_05:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_05}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_04:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_04}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_03:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_03}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_02:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_02}'"
        subprocess.call(cmd, shell=True)

elif temp_2 > TEMP_01:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_01}'"
        subprocess.call(cmd, shell=True)

else:
    for i in range(0, 3):
        cmd = f"sshpass -p {PASSWORD} ssh {SSHOPTS} {USERNAME}@{ILOIP} 'fan p {i} max {FANSPEED_00}'"
        subprocess.call(cmd, shell=True)