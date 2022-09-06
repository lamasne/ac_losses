import os
from fcts import *
from globals import *
import logging


def test_M(voltage, input_folder_SC, input_folder_no_SC, Vshunt_loss, err_scale_digitization):
    B = compute_B(input_folder_no_SC, Vshunt_loss, err_scale_digitization)
    M = compute_M(input_folder_SC, input_folder_no_SC, Vshunt_loss, err_scale_digitization)

    logging.info(
        f"M = {(max(M[1])-min(M[1]))/2 : .2f} H/m"
    )

    t, B_match, M_match = match_x(B, M)

    fig, axs = plt.subplots(2)
    axs[0].plot(t, M_match, "b")
    axs[0].set_xlabel("t (s)")
    axs[0].set_ylabel("M (H/m)", color="b")
    ax1 = axs[0].twinx()
    ax1.set_ylabel("B_s", color="r")
    ax1.plot(t, B_match, "r")

    axs[1].plot(B_match, M_match)
    axs[1].set_xlabel("B_s (T)")
    axs[1].set_ylabel("M (H/m)")

    fig.suptitle(f'Test M: {voltage} V', fontsize=16)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped


def test_B(filename, input_folder, Vshunt_loss, err_scale_digitization):
    Vs_real, Vshunt_real = get_data(input_folder, Vshunt_loss, err_scale_digitization)
    Vs = format_data(Vs_real[0], Vs_real[1])
    V_shunt = format_data(Vshunt_real[0], Vshunt_real[1])
    Icoil = V_shunt[1] * shunt_ratio  # Gain factor Vs --> Is
    flux_s = my_integrate(Vs[0], Vs[1])

    Bs = compute_B(input_folder, Vshunt_loss, err_scale_digitization)  
    logging.info(
        f"B_s = {(max(Bs[1])-min(Bs[1]))/2 * 1000 : .2f} mT"
    )

    fig, ax = plt.subplots()
    ax.plot(Icoil, Bs[1])
    ax.set_xlabel("I_coil (A)")
    ax.set_ylabel("B_s (T)")
    fig.suptitle('Test B: ' + filename, fontsize=16)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.savefig(
        os.path.join(workspace, "outputs/test_B_" + filename + ".png")
    )

def test_integration(filename, input_folder, Vshunt_loss, err_scale_digitization):
    Vs_real, Vshunt_real = get_data(input_folder, Vshunt_loss, err_scale_digitization)
    Vs = format_data(Vs_real[0], Vs_real[1])
    V_shunt = format_data(Vshunt_real[0], Vshunt_real[1])
    Icoil = V_shunt[1] * shunt_ratio  # Gain factor Vs --> Is
    flux_s = my_integrate(Vs[0], Vs[1])
    delta_t = Vs[0][1] - Vs[0][0]

    fig, axs = plt.subplots(2)

    axs[0].set_ylabel("flux_sensor (V)", color="g")
    axs[0].plot(flux_s[0], flux_s[1], "g-", label="flux_sensor")
    ax1 = axs[0].twinx()
    ax1.set_ylabel("d/dt(phi_s)", color="k")
    ax1.plot(Vs[0], Vs[1], "r", label="V_s")
    ax1.plot(Vs[0], np.gradient(flux_s[1], delta_t), "k--", label="d/dt(phi_s)")
    axs[0].legend(loc="upper left")
    ax1.legend(loc="upper right")

    axs[1].set_ylabel("I_coil (V)", color="b")
    axs[1].plot(V_shunt[0], Icoil, "b-", label="I_coil")
    ax2 = axs[1].twinx()
    ax2.set_ylabel("flux_sensor (V)", color="g")
    ax2.plot(flux_s[0], flux_s[1] * 1000, "g-", label="flux_sensor")
    axs[1].legend(loc="upper left")
    ax2.legend(loc="upper right")

    fig.suptitle('Test integration: ' + filename, fontsize=16)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    axs[1].set_xlabel("time (s)")
    plt.savefig(
        os.path.join(workspace, "outputs/test_integration_" + filename + ".png")
    )


def test_input_data(filename, input_folder, Vshunt_loss, err_scale_digitization):
    # Clean osciolloscope data
    Vs_raw, Vshunt_raw = get_raw_data(input_folder, err_scale_digitization)
    Vs = format_data(Vs_raw[0], Vs_raw[1])
    Vshunt = format_data(Vshunt_raw[0], Vshunt_raw[1])

    # real quantities
    Vs_real, Vshunt_real = get_data(input_folder, Vshunt_loss, err_scale_digitization)
    Icoil = Vshunt_real[1] * shunt_ratio  # Gain factor Vs --> Is

    # Log
    logging.info(f"I_coil = {(max(Icoil)-min(Icoil)) / 2 : .2f} A")
    logging.info(f"V_sensor: {(max(Vs[1])-min(Vs[1])) / 2 * 1000: .2f} mV")

    # Plots
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("time (s)")
    ax1.set_ylabel("V_sensor osciolloscope (V)", color="r")
    ax1.plot(Vs_raw[0], Vs_raw[1], "r*")
    ax1.plot(Vs[0], Vs[1], "r-")
    ax1.tick_params(axis="y", labelcolor="r")

    ax2 = ax1.twinx()
    ax2.set_ylabel("V_shunt osciolloscope (V)", color="b")
    ax2.plot(Vshunt_raw[0], Vshunt_raw[1], "b*")
    ax2.plot(Vshunt[0], Vshunt[1], "b-")
    ax2.tick_params(axis="y", labelcolor="b")

    fig.suptitle('Test input data: ' + filename, fontsize=16)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(os.path.join(workspace, "outputs/test_input_data_" + filename + ".png"))