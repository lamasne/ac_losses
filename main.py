from fcts import *
from tests import *
import logging
import run_params
import globals 

for idx_folder in run_params.idx_folders:
    input_folder = globals.input_folders[idx_folder]
    filename = input_folder.split("/")[-1]
    logging.info(f"Computing for:{filename} -----------")

    voltage = int(filename[:3])
    err_scale_digitization = 100 if voltage >= 120 else 200
    Vshunt_loss = 200 if voltage >= 120 else 500

    test_input_data(filename, input_folder, Vshunt_loss, err_scale_digitization)
    test_integration(filename, input_folder, Vshunt_loss, err_scale_digitization)
    compute_B(input_folder, Vshunt_loss, err_scale_digitization)
    test_hysteresis(filename, input_folder, Vshunt_loss, err_scale_digitization)

plt.show()

