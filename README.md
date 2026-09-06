Queensland University of Technology IFB/ITD102 Unit "Introduction to Computer Systems"

Assessment Task 3 Submission by Reigner Casangcapan (2025)
Project submission worked out accordingly and implementation of technologies was feature complete.

Unit/Course outcomes and overview:
This project comprises of designing/constructing/configuring a small novel computer system using a mixture of computer technologies.
Implementing different aspects of computer systems (hardware, software and networks) including their structure, operation and security.
Configuring/managing computer systems to perform specific tasks and troubleshoot IT problems.
Using information literacy skills to conduct/explain computer systems research and design/build basic computer systems using variety of 
technology tools, techniques and resources. Raspberry Pi Model 3A+ (rPi) was used for this unit. 


"Networked IoT Reaction Time System"

Features:
- rPi Model 3A+
- rPi Sense HAT V2
- rPi Dual-Access GPIO Extension Board
- 3pc Heatsink Kit for rPi
- M2 Screws 
- M2 Nuts 
- Copper Column (F/M)
- Tactile Button Switch (6mm)
- Jumper Wires 20cm Ribbon (M/M)
- 1/4 Watt 1% Resistors
- 40-pin rPi GPIO Breakout
- 40-pin rPi GPIO Ribbon Cable
- Solderless Breadboard - 830 Tie Point (ZY-102)
Note: number of items used have not been written down.

Stack: Python3, SQLite3, Flask, HTML/CSS

This project aims to measure the reaction time of the user and display real-time data of results onto a locally hosted website through 
the rPi and SQLite3 was used to store data of each of the user scores. 

Thank you to Geoff - great tutor. This assessment was ideally for a two or three person group but I wanted to work on it alone. I had bought
all the hardware personally. The Sense HAT for the rPi includes an 8x8 LED display and a tactile 5-way switch and a myriad of other sensors.
To add complexity, my tutor had asked me to implement external hardware - hence the breadboard with its own tactile switch. Of course, this meant 
having to find a way to connect the HAT with the rPi and the breadboard. The Dual-Access GPIO Extension Board solved this issue - having a 40 Pin Female
to sit atop the rPi and the Dual-Access 40 Pin Male for the HAT to sit parallel to the rPi and the secondary male 40 Pin for the female GPIO Ribbon Cable.
The ribbon cable connects to the GPIO Breakout Board which is firmly sitting on the Solderless Breadboard. From here, the M/M jumper wires connect from the 
breakout board to the tactile switch on the breadboard. The Copper Columns helps support the Sense HAT as it sits directly atop the rPi - acting as spacers. 
Due to the hardware extensiveness, a heatsink kit was included to support cooling. This concludes all the hardware involved. 
A python3 script is involved in creating the game.py script and server.py script to create the game and an SQLite3 database to store the game data. 
Flask/HTML/CSS is implemented for the website.



