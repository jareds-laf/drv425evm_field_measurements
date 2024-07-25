import pandas as pd
import os
import pint

# Define the unit registry
ureg = pint.UnitRegistry(auto_reduce_dimensions=True)

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
	return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

# Read the oscilloscope data file and MC90R calibration data
csv_path = normalize_path(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\ALL0006\F0006CH2.CSV')
scope_data = pd.read_csv(csv_path, header=None)
scope_data.rename(columns={3: "Time (s)", 4: "V_out (V)"}, inplace=True)

calibration_path = normalize_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc90r_calibration.csv'))
calibration_data = pd.read_csv(calibration_path)

# Subtract the vertical offset
vertical_offset = pd.to_numeric(scope_data[1][9])  # B10 corresponds to 1, 9 in 0-based index
scope_data.insert(6, column='V_out - Offset (V)', value=scope_data['V_out (V)'] - vertical_offset)

# Convert Vo to field using the calibration data
print(calibration_data.head())
# print(calibration_data['Vo/Field (mV/mG)'] * ureg.mG)


scope_data.insert(7, column='B (T)', value=0.0)

# Save the modified DataFrame to a new CSV file
output_file_path = normalize_path(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\ALL0005\OUT_F0005CH1.csv')
# output_file_path = normalize_path('D:\ALL0005\OUT_F0005CH1.csv')

# scope_data.to_csv(output_file_path, index=False, header=False)
# print(f'Data saved to {output_file_path}')