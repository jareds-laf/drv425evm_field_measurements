import pandas as pd
import os
import pint

# Define the unit registry
ureg = pint.UnitRegistry(auto_reduce_dimensions=True)

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
	return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

# Read the CSV file
csv_path = normalize_path(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\ALL0006\F0006CH2.CSV')
# csv_path = normalize_path('D:\ALL0006\F0006CH2.CSV')
scope_data = pd.read_csv(csv_path, header=None)
scope_data.rename(columns={3: "Time (s)", 4: "V_out (V)"}, inplace=True)

# Subtract the vertical offset
vertical_offset = pd.to_numeric(scope_data[1][9])  # B10 corresponds to 1, 9 in 0-based index
scope_data.insert(6, column='V_out - Offset (V)', value=scope_data['V_out (V)'] - vertical_offset)

# Populate G1:I1 with editable values
# For the most part, G and Gfg should not change
R_shunt = 100 * ureg.ohm
G = 4 * ureg.V / ureg.V
Gfg = 12.2 * ureg.mA / ureg.mT

scope_data.at[19, 0] = 'R_shunt (Ohms)'
scope_data.at[19, 1] = R_shunt.magnitude
scope_data.at[20, 0] = 'G (V/V)'
scope_data.at[20, 1] = G.magnitude
scope_data.at[21, 0] = 'Gfg (mA/mT)'
scope_data.at[21, 1] = Gfg.magnitude

print(f"{R_shunt}\n{G}\n{Gfg}")



# Save the modified DataFrame to a new CSV file
output_file_path = normalize_path(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\ALL0005\OUT_F0005CH1.csv')
# output_file_path = normalize_path('D:\ALL0005\OUT_F0005CH1.csv')

# scope_data.to_csv(output_file_path, index=False, header=False)
# print(f'Data saved to {output_file_path}')