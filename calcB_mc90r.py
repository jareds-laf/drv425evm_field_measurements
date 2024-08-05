import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
	return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def calcB_mc90r(csv_path_in, channel=1):
    """Evaluate the oscilloscope data from the MC90R to convert voltages to
    magnetic fields. Note that this program assumes the usage of a Tektronix
    MSO24 oscilloscope with firmware version 2.2.6.1052, exporting data with
    "ALL" selected as the source.

    Inputs:
        - csv_path_in: The path to the oscilloscope data CSV file. Leave blank
                       to open a file dialog
        - channel: The channel number to read from the oscilloscope data
    """

    # Read the oscilloscope data into a Pandas DataFrame
    if csv_path_in:
        print(f'Reading data from {csv_path_in}')       
    else:
        csv_path_in = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        print(f'Reading data from {csv_path_in}')

    """Defining global variables. csv_path is defined separately from
    csv_path_in to allow for global access of the path to the CSV file.
    """
    global csv_path
    global ch
    global scope_data

    csv_path = csv_path_in    
    ch = channel
    scope_data = pd.read_csv(csv_path, skiprows=13)

    # Read the calibration data into a Pandas DataFrame
    calibration_path = normalize_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc90r_calibration_teslas.csv'))
    calibration_data = pd.read_csv(calibration_path)

    print(calibration_data.head())
    #TODO: Interp!
    x = 1

    """Note that the exported waveform from the MSO24 does not include vertical
    offset information. If your oscilloscope does, you should subtract it
    from the voltage output column here. Here is an example of how to do it
    with the Tektronix TDS2022B:
    """

    # Subtract vertical offset
    # vertical_offset = pd.to_numeric(scope_data[1][9])
    # scope_data.insert(6, column='V_out - Offset (V)', \
    #                   value=scope_data['V_out (V)'] - vertical_offset)

    # Convert Vo to field using the calibration data
    target_freq = 2.0
    bv_ratio = calibration_data.loc[calibration_data['Freq (kHz)']==target_freq]['Field/Vo (mT/mV)'].values[0]

    scope_data.insert(7, column='B (T)', value=scope_data['V_out - Offset (V)'] * bv_ratio)
    print(scope_data.head())

    # Save the modified DataFrame to a new CSV file
    output_file_path = normalize_path(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MSO24\OUT_F0006CH2.csv')
    # output_file_path = normalize_path('D:\ALL0005\OUT_F0005CH1.csv')

    # scope_data.to_csv(output_file_path, index=False, header=False)
    # print(f'Data saved to {output_file_path}')

def plot_mc90r():
    # Plot the B (T) vs. Time (s) oscilloscope data
    custom_params = {"axes.spines.left": True, "axes.spines.bottom": True,\
                    "axes.spines.right": False, "axes.spines.top": False,\
                    "grid.linestyle": '-',\
                    "grid.alpha": 0.5,\
                    "grid.linewidth": 0.5,\
                    "grid.color": 'black',\
                    "axes.edgecolor": 'black',\
                    "axes.linewidth": 0.75}
    
    sns.set_theme(style="whitegrid", rc=custom_params)
    sns.relplot(data=scope_data, x='Time (s)', y='B (T)', kind='line')

if __name__ == '__main__':
    calcB_mc90r(csv_path_in=r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MS024\001\tektest_000_ALL.csv', channel=1)
    # calcB_mc90r(csv_path_in='', channel=1)