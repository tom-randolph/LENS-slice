# LENS-slice
### A post-processing solution to adapt gcode for use with LENS printers

#### Configuring Slic3r
__TODO:__ Provide numbers and detailed instructions

1. Download [Slic3r](http://slic3r.org/download)
2. Configure bed size.
3. Configure layer height.
4. Configure perimiters.
5. Configure Preamble/Postamble.

 

#### Using the Printer
1. Turn on the machine
2. Open Mach4Mill with MR7 profile (may be default).
3. Confirm that Galil communication is established (status bar on bottom left).
4. Press the reset button on the machine. The light should turn on blue.
5. Press the Enable button (blinking green) on Mach4Mill.
6. Take note of the print head location.
7. Being careful not to crash the print head, try jogging the x,y (arrow keys), and z (page up, page down) axes. __Note that hitting a limit switch will require you to power down and start from step 1.__
8. Jog the head to the back right corner of the work area and zero the x and y axis by pressing the "Zero X", "Zero Y" buttons in the top left of Mach4Mill.
10. Lower the z axis using the calibration tool, and zero the z axis with the "Zero Z" button in Mach4Mill.
11. Navigate to File->Open Gcode File in Mach4Mill.
12. In the file-type dropdown, select "All files". Navigate to your file and open it.
13. If loaded correctly, you should see the tool path being traced in the blue graphics window.
14. Ensure that the machine is still enables, and press the green "Cycle Start Gcode" in Mach4Mill.


