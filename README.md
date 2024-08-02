These scripts read oscilloscope data from the Texas Instruments [DRV425EVM](https://www.ti.com/tool/DRV425EVM) and the magnetic sciences [MC90R](https://magneticsciences.com/mc90r/) and convert measured voltages to magnetic fields in Teslas. For brevity, I refer to the DRV425EVM as simply "425." Described below are the processes followed for these two sensors. Note that this process assumes the use of an Tektronix [MSO24](https://www.tek.com/en/datasheet/2-series-mso-mixed-signal-oscilloscope-datasheet) oscilloscope.

# DRV425EVM
1. Scope data is read in as a Pandas dataframe, Values of $R_{shunt}$, $G$, and $Gfg$ are fed in by the user.
2. [WIP!]
3.
4.
5. The name of the column containing voltage is changed.../// New column titled "V_out - Offset (V)" is inserted with the un-offset voltages in Volts..
6. Another new column is populated with the magnetic field data in Teslas. The new column is called "B".
7. The modified Pandas dataframe is output to a new CSV is output under the name "OUT_[name of input file].csv" in the same location as the input data.

In future versions, the user will be prompted with a file explorer window to choose a file, and a pop-up window will allow one to input values for $R_{shunt}$, $G$, and $Gfg$.

# MC90R
Note that calibration data for the MC90R is provided on an individual basis. One may need to edit the "mc90r_calibration.csv" file to match the calibration data on their own sensor.

1. Same step 1. as the DRV425EVM.
2. [WIP!]


