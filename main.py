from fcts import *
from tests import *
import logging
import run_params
import globals 

def run1():

    for idx_folder in run_params.idx_folders:
        input_folder = globals.input_folders[idx_folder]
        filename = input_folder.split("/")[-1]
        logging.info(f"Computing for:{filename} -----------")

        voltage = int(filename[:3])
        err_scale_digitization = get_err_scale_digitization(voltage)
        Vshunt_loss = get_Vshunt_loss(voltage)

        test_input_data(filename, input_folder, Vshunt_loss, err_scale_digitization)
        test_integration(filename, input_folder, Vshunt_loss, err_scale_digitization)
        test_B(filename, input_folder, Vshunt_loss, err_scale_digitization)

    plt.show()

def run2(desired_voltage:int):
    my_input_folders = []
    for input_folder in globals.input_folders:
        filename = input_folder.split("/")[-1]
        voltage = int(filename[:3])
        if voltage == desired_voltage:
            my_input_folders.append(input_folder)
    if len(my_input_folders) >= 2:
        for input_folder in my_input_folders:
            if '- No SC' in input_folder:
                input_folder_No_SC = input_folder
            elif '- SC' in input_folder:
                input_folder_SC = input_folder

    err_scale_digitization = get_err_scale_digitization(voltage)
    Vshunt_loss = get_Vshunt_loss(voltage)

    test_M(voltage, input_folder_SC, input_folder_No_SC, Vshunt_loss, err_scale_digitization)

    plt.show()

run1()
run2(120)


