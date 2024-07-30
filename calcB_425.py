import pandas as pd
import os
import pint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

'''This script reads the oscilloscope data originally measured by the DRV425EVM
and converts the voltage measurements to magnetic field measurements. For
brevity, I refer to the DRV425EVM as simply "425."
'''

# Define the unit registry
ureg = pint.UnitRegistry(auto_reduce_dimensions=True)

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
	return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def calcB_425(csv_path, R_shunt=100, G=4, Gfg=12.2, atten=10, channel=2):
    '''Evaluate the oscilloscope data from the DRV425EVM to convert voltages
    to magnetic fields. Note that this program assumes the usage of a
    Tektronix MSO24 oscilloscope with firmware version 2.2.6.1052, exporting
    data with "ALL" selected as the source.

    Inputs:
        - csv_path: The path to the oscilloscope data CSV file
        - R_shunt: The shunt resistor value in Ohms
        - G: The gain of the DRV425EVM in V/V
        - Gfg: The gain of the DRV425EVM in mA/mT
        - atten: The oscilloscope attenuation factor
        - ch: The channel number to read from the oscilloscope data
    '''

    # TODO: Be able to process and plot all three channels!

    # Read the CSV file
    csv_path = normalize_path(csv_path)
    global scope_data
    scope_data = pd.read_csv(csv_path, skiprows=13)

    global ch
    ch = channel
    # Note that the exported waveform from the MSO24 does not include vertical
    # offset information. If your oscilloscope does, you should subtract it
    # from the voltage output column here. Here is an example of how to do it
    # with the Tektronix TDS2022B:

    # Subtract vertical offset
        # B10 corresponds to [1, 9] in 0-based index
    # vertical_offset = pd.to_numeric(scope_data[1][9])
    # scope_data.insert(6, column='V_out - Offset (V)', \
    #                   value=scope_data['V_out (V)'] - vertical_offset)

    # Divide by attenuation
    scope_data.iloc[:, 1] = scope_data.iloc[:, 1] / atten

    # TODO: Figure out a better way to put in R, G, and Gfg into the output csv
    # Populate C1:E1 with editable 425 values
    # For the most part, G and Gfg should not change

    # scope_data.at[2, 0] = 'R_shunt (Ohms)'
    # scope_data.at[2, 1] = R_shunt.magnitude
    # scope_data.at[3, 0] = 'G (V/V)'
    # scope_data.at[3, 1] = G.magnitude
    # scope_data.at[4, 0] = 'Gfg (mA/mT)'
    # scope_data.at[4, 1] = Gfg.magnitude

    # Populate column C with the final B field based on formula 1 from
    # the DRV425EVM datasheet: B = (V_out) / (R_shunt * G * Gfg)
    scope_data.insert(2, column='B', value= scope_data[f'CH{ch}'] / (R_shunt * G * Gfg))
    print(scope_data.head())

    # TODO: Implement this:
    # Save the modified DataFrame to a new CSV file
    # output_file_path = normalize_path(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\ALL0005\OUT_F0005CH1.csv')

    # scope_data.to_csv(output_file_path, index=False, header=False)
    # print(f'Data saved to {output_file_path}')


def plot_425():
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
    ax = sns.relplot(data=scope_data, x='TIME', y=f'CH{ch}', kind='line')
    ax.set(xlabel='Time (s)', ylabel='B (T)')


if __name__ == '__main__':
    calcB_425(csv_path=r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MS024\001\Tek000_nogating_allchannels_000_ALL.csv', R_shunt=100, G=4, Gfg=12.2, atten=10, channel=2)
    plot_425()