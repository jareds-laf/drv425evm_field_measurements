import pandas as pd
import os

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
    return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

# Read the MC90R calibration data
calibration_path = normalize_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc90r_calibration.csv'))
print(calibration_path)
calibration_data = pd.read_csv(calibration_path)

print(calibration_data.head())

# Convert mV/mG to mV/mT
calibration_data.loc[:, 'Vo/Field (mV/mG)'] = calibration_data['Vo/Field (mV/mG)'] * 10**4

# Convert mG/mV to mT/mV
calibration_data.loc[:, 'Field/Vo (mG/mV)'] = calibration_data['Field/Vo (mG/mV)'] / 10**4


# Rename columns appropriately
calibration_data.rename(columns={'Freq (kHz)': 'freq', 'Vo/Field (mV/mG)': 'Vo/B', 'Field/Vo (mG/mV)': 'B/Vo'}, inplace=True)

print(calibration_data.head())

# Save the modified DataFrame to a new CSV file
output_file_path = normalize_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc90r_calibration_teslas.csv'))
print(f'Saving the calibration data to {output_file_path}')
calibration_data.to_csv(output_file_path, index=False, header=True)