# LENS-slice
### A post-processing solution to adapt gcode for use with LENS printers

#### What is LENS?
LENS is an additive manufacturing process developed by [Optomec](https://www.optomec.com/3d-printed-metals/lens-printers/). The process rapidly and cheaply produces metal parts by jetting metal powder into a high-power laser beam, creating a weld bead on the part below. By comparison to more conventional powder-bed methods, LENS offers the advantage of high speed and low cost. Due to the use of powder jets, there is far less unused metal powder than in powder-bed processes, drastically reducing cost of operation. Also, without the need to interrupt metal sintering for heating periods on every layer, the print head can deposit material nearly non-stop, decreasing print time. In this regard, the machine behaves far more like a traditional FDM printer than any other process.

So what's the tradeoff? For several reasons, the parts produced by this machine do not rival DMLS parts in quality. Firstly, jetting the powder onto the part is not a perfectly controlled process, and leads to continuous weld beads, opposed to homogenous layers. This is analogous to the disparity in quality between FDM parts and SLS parts, where the former process deposits continuous beads of molten plastic, and the latter process cure the entire layer nearly instantly. Secondly, the toolchain provided for running prints on the Optomec [LENS 450](https://www.optomec.com/3d-printed-metals/lens-printers/low-cost-metal-3d-printer/) is extremely limited. The machine is intended for research, not production. As such, it is run using the hobby-grade CNC control software [Mach4](http://www.machsupport.com/software/mach4/), and has very limited gcode generation software that does not allow for complex toolpaths and print geometry.

Thus, I have created a script to adapt gcode files generated from FDM printer slicing software (I am using [Slic3r](http://slic3r.org/download)) to provide the correct toolpaths for the LENS printer. It is possible that the slicing software could be modified to provide the appropriate commands, but post-processing toolpaths for existing printers is a simpler approach to get the machine up and running. The current implementation is a Python 3 script that parses a gcode file outputted from Slic3r and edits it to have the appropriate gcodes to turn the laser on and off at the appropriate times as the X, Y, and Z stages move. 





#### Configuring Slic3r
__TODO:__ Provide numbers and detailed instructions

1. Download [Slic3r](http://slic3r.org/download)
2. Configure bed size to 80mm x 80mm.
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
7. Being careful not to crash the print head, try jogging the X,Y (arrow keys), and z (page up, page down) axes. __If you hit a limit switch, cycle the E-Stop button and then press the reset button__
8. Jog the head to the back right corner of the work area and zero the X and Y axis by pressing the "Zero X", "Zero Y" buttons in the top left of Mach4Mill.
10. Lower the Z axis using the calibration tool, and zero the z axis with the "Zero Z" button in Mach4Mill.
11. Navigate to File->Open Gcode File in Mach4Mill.
12. In the file-type dropdown, select "All files". Navigate to your file and open it.
13. If loaded correctly, you should see the tool path being traced in the blue graphics window.
14. Ensure that the machine is still enables, and press the green "Cycle Start Gcode" in Mach4Mill.

#### Calibration

The LENS450 does not come with any sort of calibartion routine or reccomended print settings that would work for custom gcode. To understand what effect different print parameters (laser power, liner feed rate, and powder depostion rate) have on print quality and dimensions, I have design a test printing script that allows the user to vary the print parameters during the course of the print to get a sense of what dimesions to expect for the layer height and the width of the print bead.

