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

def calcB_425(csv_path, R_shunt=100, G=4, Gfg=12.2):
    # Evaluate the oscilloscope data from the DRV425EVM to convert voltages
    # to magnetic fields

    # Read the CSV file
    csv_path = normalize_path(csv_path)
    global scope_data
    scope_data = pd.read_csv(csv_path, header=None)
    scope_data.rename(columns={3: "Time (s)", 4: "V_out (V)"}, inplace=True)

    # Subtract the vertical offset
    vertical_offset = pd.to_numeric(scope_data[1][9])  # B10 corresponds to 1, 9 in 0-based index
    scope_data.insert(6, column='V_out - Offset (V)', value=scope_data['V_out (V)'] - vertical_offset)

    # Populate G1:I1 with editable 425 values
    # For the most part, G and Gfg should not change
    R_shunt = R_shunt * ureg.ohm
    G = G * ureg.V / ureg.V
    Gfg = Gfg * ureg.mA / ureg.mT

    scope_data.at[19, 0] = 'R_shunt (Ohms)'
    scope_data.at[19, 1] = R_shunt.magnitude
    scope_data.at[20, 0] = 'G (V/V)'
    scope_data.at[20, 1] = G.magnitude
    scope_data.at[21, 0] = 'Gfg (mA/mT)'
    scope_data.at[21, 1] = Gfg.magnitude

    print(f"{R_shunt}\n{G}\n{Gfg}")

    # Populate column J with the final B field based on formula 1 from
    # the DRV425EVM datasheet: B = (V_out - Offset) / (R_shunt * G * Gfg)
    # Headers: 0, 1, 2, Time (s), V_out (V), 5, V_out - Offset (V), B (T)
    scope_data.insert(7, column='B (T)', value=scope_data['V_out - Offset (V)'] / (R_shunt * G * Gfg))

    # Save the modified DataFrame to a new CSV file
    output_file_path = normalize_path(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\ALL0005\OUT_F0005CH1.csv')
    # output_file_path = normalize_path('D:\ALL0005\OUT_F0005CH1.csv')

    scope_data.to_csv(output_file_path, index=False, header=False)
    print(f'Data saved to {output_file_path}')


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
    sns.relplot(data=scope_data, x='Time (s)', y='B (T)', kind='line')

if __name__ == '__main__':
    calcB_425(csv_path=r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\ALL0005\F0005CH1.CSV', R_shunt=100, G=4, Gfg=12.2)
    plot_425()