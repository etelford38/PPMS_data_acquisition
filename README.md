# PPMS_data_acquisition
Python software for simultaneously interfacing with a PPMS and external measurement hardware.

# Starting Spyder
Note: the data acquisition program runs using Python and the Spyder IDE in tandem with MultiVu.

1.  Open MultiVu in non-administrator mode (just click on the task-bar icon). This is important for proper communication between the Python code and the MutliVu software.
2.  Click the task-bar icon bar that looks like a command terminal called “Anaconda Prompt”. This opens a terminal window that allows you to access conda environments and run Python programs.
3.  Type “spyder” and hit enter:
4.  Open the script for the measurement program "PPMS_Measurement _Program.py".
5.  Open the script for loading instruments "PPMS_Load_Instruments.py".

# Loading Instruments

1.  Run “PPMS_Load_Instruments.py” by clicking on the tab, and then hitting the aquamarine play button on the top toolbar. A small pop-up titled “RoyLab - Load Instruments” should appear on the screen after a few seconds.

2.  To load the instruments you want to use:
  - check the box on the left side
  - select the instrument you want to load from the drop-down menu. 
  - name this instrument something useful for you to refer to.
  - enter its GPIB address. The GPIB address can be found by clicking “See available resources” on the bottom left corner of the window. This will open another pop-up that will show the instruments connected to the bus, as well as their GPIB addresses. 
  - use the drop-down menu on the right side to select the variables you want to record. 
  - repeat this process for every instrument you are planning on using. 

  Note: This pop-up starts with enough lines for five instruments. If you are using more than five instruments, you can add additional lines by clicking “Add Instrument”.

Note: If the desired instruments do not appear under “See available resources”, double check that the BUS is on and that all the desired instruments are turned on and connected to the BUS with GPIB cables.	

Second Note: The Dynacool PPMS has no GPIB address. When you add it, you can leave the GPIB address section blank.

Seeing available resources:


Selecting an instrument in the first row:


Selecting the Dynacool (no GPIB address required):


Once you have entered the information for your instruments, click “Test Connections”. This will make sure that the program is communicating properly with the instruments you have loaded. 

Testing connections with no errors. In this example, a lock-in and the Dynacool were connected. The Spyder console tells you it found the PPMS server and the lock-in and connected to them.

Testing connections with errors. In this example, a lock-in and the Dynacool were connected.
The console tells you it successfully connected to the lock-in but failed to find the PPMS server and connect to it. This is likely due to conflicting server connection requests. Restart the kernel and rerun load instruments and test connections:


Once “test connections” is successful, you can close the pop-up by clicking “CLOSE”.

The pop-up window closed after successful connection testing:

Running a Measurement
The measurement program is really useful for connecting the external hardware with the PPMS. However, it does not have the same sequence-writing capabilities that MultiVu does. It is generally easier to sweep temperature and magnetic field with MultiVu. If you are doing a temperature-dependent Hall or magnetoresistance measurement that requires sweeping field at different temperature points for example, it is easier to write the temperature and field sweep sequence in MultiVu, run it in MultiVu, and then have the measurement program continuously measure as the temperature/field sweep sequence runs in MultiVu. 

Run the program “PPMS_Measurements_Program.py” by selecting the appropriate tab and clicking the aquamarine play button on the top toolbar. A large pop-up should appear on the screen.

A picture of the opened measurement program GUI:

The measurement program has a number of elements that are used to collect and save your data:
Top left box: used to designate whether or not to save your data (by checking the box), your data file name, and the location where your data will be saved.
Middle left box: control functions for select instruments. Depending on the instrument, you can use this box to control your instrument’s output and measurement parameters. Instruments controlled with this box include lock-ins, Keithley 6221/2182A, Keithley 6517B, and the PPMS temperature and magnetic field.
Bottom left box: used to determine what populates the main plot. You can control which data is plotted by checking or unchecking the tick boxes next to the corresponding variable, the color and line style of the trace for each variable, and you can change the independent variable (x-axis).
Top middle box: a space to leave notes for your future self. These notes will be saved in the header of your data file.
Middle middle box: the main plot that is populated by your data. By right-clicking on the plot, you can modify some plot parameters.
Top right box: a second set of control functions for select instruments. Depending on the instrument, you can use this box to control your instrument’s output and measurement parameters. Instruments controlled with this box include the Keithley 2450.
Middle right box: used to set up measurements that involve sweeping a single independent variable. You can select the variable you want to sweep in the “Instr to sweep” box and the corresponding start and stop values. You can also set the number of points used in the sweep (# points), the time delay between each new data point (Wait time (s)), the number of individual sweeps to perform (repeat), the sweep direction (raster vs. unidirectional), and the number of points used to ramp back to the starting value. To start the sweep, simply click “Start Loop” after selecting all of your parameters. 

For example, if I want to perform an IV sweep, I would choose the following parameters:
Instr to sweep: “Keithley 2450”
Start: -1
Stop: +1
# points: 101
Wait time (s): 0.3
Repeat: 2
Sweep direction: “Raster”
# points down: N/A

Note: this is will perform two rastered IV curves with the Keithley 2450 starting at -1V, ending at 1V, with 101 points and a 0.3 second wait time between each point.

Second Note: the loop can be started before OR after your start recording the measurement. If you start the loop before you start recording measurements, the loop will actually start as soon as you start recording.

Bottom right box: sets the data acquisition sample time and has buttons for starting and stopping a measurement.

Expanded measurement program showing all the GUI components:

For most use cases, the Python data acquisition software is intended to be a passive measurement program (i.e. it simply records data without controlling external parameters). This means a typical measurement sequence would look something like this:
Load the instruments that would like to use using “PPMS_Load_Instruments.py”.
Run the measurement progam “PPMS_Measurements_Program.py”.
Setup your file-saving information (data file name and save path) and add any desired notes.
Setup any initial measurement equipment parameters (such as output voltages/current, compliances, measurement ranges, etc…).
Start recording your data with the Python measurement program.
Write a sequence in MutliVu to perform the desired temperature/field sequence.
The measurement program will record data while MultiVu is performing it’s sequence.
After the MultiVu sequence is complete, stop recording data on the Python measurement program.
Load and analyze your data with the Python data analysis software.

Note: some example screenshots of using the measurement program are given below:

Screenshot of the measurement program with a save path, save file name, and notes filled out:



A sample data file saved by the measurement program. It can be opened by the Python data analysis software:


The measurement program running in tandem with MultiVu:


The measurement program plotting temperature versus time demonstrating that it’s following the MultiVu sequence:



The measurement program plotting magnetic field versus time demonstrating that it’s following the MultiVu sequence:




Showcasing the full capabilities of the program by loading and measuring all possible equipment on th PPMS rack:

Loading instruments:


Running the measurement program:


The measurement program while running:
