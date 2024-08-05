import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog

'''This script reads the oscilloscope data originally measured by the DRV425EVM
and converts the voltage measurements to magnetic field measurements. For
brevity, I refer to the DRV425EVM as simply "425."
'''

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
	return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def calcB_425(csv_path, R_shunt=100, G=4, Gfg=12.2, channel=2):
    '''Evaluate the oscilloscope data from the DRV425EVM to convert voltages
    to magnetic fields. Note that this program assumes the usage of a
    Tektronix MSO24 oscilloscope with firmware version 2.2.6.1052, exporting
    data with "ALL" selected as the source.

    Inputs:
        - csv_path: The path to the oscilloscope data CSV file. Leave blank
                    to open a file dialog
        - R_shunt: The shunt resistor value in Ohms
        - G: The gain of the DRV425EVM in V/V
        - Gfg: The gain of the DRV425EVM in mA/mT
        - ch: The channel number to read from the oscilloscope data
    '''

    # TODO: Be able to process and plot all three channels!

    # Read the CSV file into a Pandas DataFrame
    if csv_path:
        print(f'Reading data from {csv_path}')       
    else:
        csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        print(f'Reading data from {csv_path}')

    global scope_data
    scope_data = pd.read_csv(csv_path, skiprows=13)

    # Rename the columns to be more descriptive
    scope_data.rename(columns={'TIME': 't', 'CH1': 'V1', 'CH2': 'V2', 'CH3': 'V3'}, inplace=True)
    scope_data.drop(columns=['CH4'], inplace=True)

    # TODO: Get rid of this var!
    global ch
    ch = channel

    # Note that the exported waveform from the MSO24 does not include vertical
    # offset information. If your oscilloscope does, you should subtract it
    # from the voltage output column here. Here is an example of how to do it
    # with the Tektronix TDS2022B:

    # Subtract vertical offset
    # vertical_offset = pd.to_numeric(scope_data[1][9])
    # scope_data.insert(6, column='V_out - Offset (V)', \
    #                   value=scope_data['V_out (V)'] - vertical_offset)

    # Populate DataFrame with the final B field based on formula 1 from
    # the DRV425EVM datasheet: B = (V_out) / (R_shunt * G * Gfg)
    # Note that this assumes the reference voltage was subtracted from the
    # output voltage.
    scope_data.insert(2, column='B1', value = scope_data['V1'] / (R_shunt * G * Gfg))
    scope_data.insert(4, column='B2', value = scope_data['V2'] / (R_shunt * G * Gfg))
    scope_data.insert(6, column='B3', value = scope_data['V3'] / (R_shunt * G * Gfg))

    # Populate DataFrame with 425 values
    # For the most part, G and Gfg should not change
    scope_data.insert(7, column='R_shunt', value = None)
    scope_data.at[0, 'R_shunt'] = R_shunt
    scope_data.insert(8, column='G', value = None)
    scope_data.at[0, 'G'] = G
    scope_data.insert(9, column='Gfg', value = None)
    scope_data.at[0, 'Gfg'] = Gfg
    print(scope_data.head())

    # TODO: Implement this:
    # Save the modified DataFrame to a new CSV file
    # Final units are:
        # t: Seconds
        # V1, V2, V3: Volts
        # B1, B2, B3: Teslas
        # R_shunt: Ohms
        # G: V/V
        # Gfg: mA/mT
    output_file_path = normalize_path(f'{os.path.dirname(csv_path)}/b_field_{os.path.basename(csv_path)}')
    scope_data.to_csv(output_file_path, index=False, header=True)
    print(f'Data saved to {output_file_path}')

def plot_425():
    # Plot the B (T) vs. Time (s) oscilloscope data

    # Apply custom parameters
    custom_params = {
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.spines.right": True,
        "axes.spines.top": True,
        "grid.linestyle": '-',
        "grid.alpha": 0.5,
        "grid.linewidth": 0.5,
        "grid.color": 'black',
        "axes.edgecolor": 'black',
        "axes.linewidth": 0.75
    }

    plt.rcParams.update(custom_params)

    # TODO: Make it so that channels are plotted with different colors
    # Plot data
    fig, ax = plt.subplots()
    ax.plot(scope_data['TIME'], scope_data['B'])

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('B (T)')
    ax.grid(True)
    plt.show()

if __name__ == '__main__':
    # calcB_425(csv_path=r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MS024\001\Tek000_nogating_allchannels_000_ALL.csv', R_shunt=100, G=4, Gfg=12.2, channel=2)
    calcB_425(csv_path=r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MS024\001\tektest_000_ALL.csv', R_shunt=100, G=4, Gfg=12.2, channel=2)
    # calcB_425(csv_path='', R_shunt=100, G=4, Gfg=12.2, channel=2)
    # plot_425()