import os
import sys
import logging
from run_params import is_ICMAB

# Meta params
workspaces = [
    r'C:\Users\nlamas\Desktop\workspace\ac_losses', # ICMAB
    r"C:\Users\Lamas\workspace\WORK\ac_losses", # home
]
workspace = workspaces[0] if is_ICMAB else workspaces[1]

# Log config
logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format = '%(message)s',
    handlers = [
        logging.FileHandler(filename=os.path.join(workspace, "outputs/log.txt")),
        logging.StreamHandler(stream=sys.stdout)
    ]
)

input_folders = [
    os.path.join(workspace, "inputs/040 V - No SC"),
    os.path.join(workspace, "inputs/080 V - No SC"),
    os.path.join(workspace, "inputs/120 V - No SC"),
    os.path.join(workspace, "inputs/120 V - SC"),
]

separator = ", "
header = 0
resol = 1000

S = 12.2 * 39.4 * 1e-6  # m^2 -- superficie bobina sensor
N_s = 11  # numero de vueltas sensor

shunt_ratio = 200 / 0.06  # A/V
Vs_gain = 10



