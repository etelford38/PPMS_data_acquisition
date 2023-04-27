# PPMS_data_acquisition
Python software for simultaneously interfacing with a PPMS and external measurement hardware.
Written by Maelle Kapfer (mak2294@columbia.edu) and modified by Jordan Pack (j.pack@columbia.edu), Evan Telford (ejt2133@columbia.edu), and Christie Koay (csk2172@columbia.edu).

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

3.  Once you have entered the information for your instruments, click “Test Connections”. This will make sure that the program is communicating properly with the instruments you have loaded. 

4.  Once “test connections” is successful, you can close the pop-up by clicking “CLOSE”.

# Running a Measurement
The measurement program is really useful for connecting the external hardware with the PPMS. However, it does not have the same sequence-writing capabilities that MultiVu does. It is generally easier to sweep temperature and magnetic field with MultiVu. If you are doing a temperature-dependent Hall or magnetoresistance measurement that requires sweeping field at different temperature points for example, it is easier to write the temperature and field sweep sequence in MultiVu, run it in MultiVu, and then have the measurement program continuously measure as the temperature/field sweep sequence runs in MultiVu. 

1.  Run the program “PPMS_Measurements_Program.py” by selecting the appropriate tab and clicking the aquamarine play button on the top toolbar. A large pop-up should appear on the screen.

2.  The measurement program has a number of elements that are used to collect and save your data:
    - Top left box: used to designate whether or not to save your data (by checking the box), your data file name, and the location where your data will be saved.
    - Middle left box: control functions for select instruments. Depending on the instrument, you can use this box to control your instrument’s output and measurement parameters. Instruments controlled with this box include lock-ins, Keithley 6221/2182A, Keithley 6517B, and the PPMS temperature and magnetic field.
    - Bottom left box: used to determine what populates the main plot. You can control which data is plotted by checking or unchecking the tick boxes next to the corresponding variable, the color and line style of the trace for each variable, and you can change the independent variable (x-axis).
    - Top middle box: a space to leave notes for your future self. These notes will be saved in the header of your data file.
    - Middle middle box: the main plot that is populated by your data. By right-clicking on the plot, you can modify some plot parameters.
    - Top right box: a second set of control functions for select instruments. Depending on the instrument, you can use this box to control your instrument’s output and measurement parameters. Instruments controlled with this box include the Keithley 2450.
    - Middle right box: used to set up measurements that involve sweeping a single independent variable. You can select the variable you want to sweep in the “Instr to sweep” box and the corresponding start and stop values. You can also set the number of points used in the sweep (# points), the time delay between each new data point (Wait time (s)), the number of individual sweeps to perform (repeat), the sweep direction (raster vs. unidirectional), and the number of points used to ramp back to the starting value. To start the sweep, simply click “Start Loop” after selecting all of your parameters. 
    - Bottom right box: sets the data acquisition sample time and has buttons for starting and stopping a measurement.

Note: the loop can be started before OR after your start recording the measurement. If you start the loop before you start recording measurements, the loop will actually start as soon as you start recording.

For most use cases, the Python data acquisition software is intended to be a passive measurement program (i.e. it simply records data without controlling external parameters). This means a typical measurement sequence would look something like this:
1.  Load the instruments that would like to use using “PPMS_Load_Instruments.py”.
2.  Run the measurement progam “PPMS_Measurements_Program.py”.
3.  Setup your file-saving information (data file name and save path) and add any desired notes.
4.  Setup any initial measurement equipment parameters (such as output voltages/current, compliances, measurement ranges, etc…).
5.  Start recording your data with the Python measurement program.
6.  Write a sequence in MutliVu to perform the desired temperature/field sequence.
7.  The measurement program will record data while MultiVu is performing it’s sequence.
8.  After the MultiVu sequence is complete, stop recording data on the Python measurement program.
9.  Load and analyze your data with the Python data analysis software.
