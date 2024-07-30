import pandas as pd
import os
import pint
import seaborn as sns

# Define the unit registry
ureg = pint.UnitRegistry(auto_reduce_dimensions=True)

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
	return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def calcB_mc90r(csv_path, atten=10, channel=2):
    # Read the oscilloscope data file and MC90R calibration data
    # Read the CSV file
    csv_path = normalize_path(csv_path)
    global scope_data
    scope_data = pd.read_csv(csv_path, skiprows=13)
    
    calibration_path = normalize_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc90r_calibration_teslas.csv'))
    calibration_data = pd.read_csv(calibration_path)

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
    calcB_mc90r(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MSO24\001\Tek000_nogating_000.csv', atten=10, ch=2)