import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import os
from globals import *
import logging

def compute_B(input_folder, Vshunt_loss, err_scale_digitization):
    Vs_raw, Vshunt_raw = get_data(input_folder, Vshunt_loss, err_scale_digitization)
    Vs = format_data(Vs_raw[0], Vs_raw[1])
    Vshunt = format_data(Vshunt_raw[0], Vshunt_raw[1])
    Icoil = Vshunt[1] * shunt_ratio  # Gain factor Vs --> Is

    flux_s = my_integrate(Vs[0], Vs[1])
    B_s = flux_s / (N_s * S)
    logging.info(
        f"B_s = {(max(B_s)-min(B_s))/2 * 1000 : .2f} mT"
    )
    
def my_integrate(x, y):
    Y = np.zeros(len(x))
    for i in range(1, len(x)):
        Y[i] = Y[0] + np.trapz(y[0:i], x=x[0:i])
    Y = rm_offset(Y)
    return Y


def format_data(x, y):
    # returns clean array
    x_array = np.linspace(min(x), max(x), resol)
    y_fct = interp1d(x, y)
    return [x_array, y_fct(x_array)]


def get_data(input_folder, Vshunt_loss, err_scale_digitization):
    # returns physical quantities
    Vs, Vshunt = get_raw_data(input_folder, err_scale_digitization)
    # Gain correction
    Vs[1] *= Vs_gain  # because of multiplier (gain)
    Vshunt[1] /= Vshunt_loss
    condition_shunt_gain = ("120" in input_folder) or ("160" in input_folder)
    if (condition_shunt_gain and Vshunt_loss == 500) or (
        not condition_shunt_gain and Vshunt_loss == 200
    ):
        print("check shunt gain")
    return Vs, Vshunt


def get_raw_data(input_folder, err_scale_digitization):
    # returns signals from osciolloscopes
    Vs = get_data_from_csv(os.path.join(input_folder, "V_s.txt"))
    Vshunt = get_data_from_csv(os.path.join(input_folder, "V_shunt.txt"))

    # Center curves
    Vs[1] = rm_offset(Vs[1])
    Vshunt[1] = rm_offset(Vshunt[1])

    # Digitization correction
    Vs[1] /= err_scale_digitization  # because digitization with wrong scale 1V --> 5mV

    # From ms to s
    Vs[0] /= 1000
    Vshunt[0] /= 1000

    return Vs, Vshunt


# Return an array with all data data from csv
def get_data_from_csv(data_path, separator=separator, header=header):
    # initialize output
    data = []

    # store data
    f = open(data_path, "r")  # r stand for reading only
    rows = f.readlines()[header:]
    f.close()

    # get data
    for row in rows:
        split_row = row.split(separator)
        # check input file
        if len(split_row) < 2:
            raise IOError(
                f"Check whether input data have the following properties:\n"
                f"\tseparator: {separator}\n"
                f"\theader: {header}"
            )
        else:
            # Clean \n at end of line
            if "\n" in split_row[-1]:
                split_row[-1] = split_row[-1].replace("\n", "")
            # Make float
            data.append([float(elem.replace(",", ".")) for elem in split_row])

    return np.array(data).T

def rm_offset(y):
    y_center = (abs(max(y)) - abs(min(y))) / 2
    y -= y_center
    return y