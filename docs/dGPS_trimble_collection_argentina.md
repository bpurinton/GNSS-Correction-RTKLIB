---
title: "*dGPS data collection with Trimble Pro XRS device and conversion to RINEX*"
subtitle: "NW Argentina Trimble Rover Units"
date: "March 2019"
author: "*Written by Ben Purinton ([purinton@uni-potsdam.de](purinton@uni-potsdam.de)), inspired by dGPS manual of Bodo Bookhagen ([bodo.bookhagen@uni-potsdam.de](bodo.bookhagen@uni-potsdam.de))*"
titlepage: true
titlepage-rule-height: 2
toc-own-page: true 
listings-disable-line-numbers: true
footer-left: Ben Purinton ([purinton@uni-potsdam.de](purinton@uni-potsdam.de))
logo: "figs/TrimbleCover.jpg"
logo-width: 400
---

# dGPS Data collection with the Trimble Pro XRS Pathfinder (L1) backpack

## Introduction

The Trimble Pro XRS units (Fig. \ref{Fig:trimble_pro_xrs_dgps}) and the TSC-1 receivers (Fig. \ref{Fig:trimble_tsc1_receiver}) are robust
and sturdy and rely on the GPS L1 and P signal (no L2 signal) and
provide centi- to decimeter accuracy. We either mount these units on the
top of the car with a magnet, or carry them in a backpack for off-road
measurements. The basic steps are outlined in this document:

1.  Setup the unit and collect data, making sure to set the antenna
    height

2.  Download the dGPS data from the units and covert them to SSF using
    Trimble Data Transfer Utility (free program:
    <http://www.trimble.com/datatransfer/>) and then RINEX files using
    Trimble Pathfinder Office (email <ben.purinton@gmail.com> if this
    program is not available to you)

3.  Correct the data in RTKLIB (free program: <http://www.rtklib.com/>)

    *   **See second manual *dGPS Correction with RTKLIB***

![Trimble Pro XRS unit, the brains of the operation.\label{Fig:trimble_pro_xrs_dgps}](figs/trimble_pro_xrs_dgps.jpg)

![TSC-1 reciever, the interface with the Pro XRS.\label{Fig:trimble_tsc1_receiver}](figs/trimble_tsc1_receiver.jpg)


## Setup: Problems and Solutions

When carried in the backpack, these units use lead-acid sealed 12V
batteries (Fig. \ref{Fig:lead_acid_battery}). When mounted in the car we exchange the power
adapter from the clamps used on these batteries to the car outlet
adapter. Please note that the dGPS units occasionally do not work
properly (low battery or cannot connect to dGPS warnings). In this case,
the problem (and solution) is:

1. The lead-acid battery is low in charge (check the battery with a multi-meter and charge it if needed)

2. The clamps connecting the battery to the units are not tight (tape the clamps to the prongs on the battery)

3. One or more of the cables connecting everything are broken or not
 tight (try switching the cables around and making sure they are
 connected tightly)

4. The batteries in the back of the hand-held units (Fig. \ref{Fig:trimble_tsc1_receiver_battery}) are loose
 or old (try switching the batteries around or exchanging them)

**Note:** One or more of these steps usually work to get the unit working, but it may take some time to find the problem, so don’t get frustrated.

![Lead-acid batteries used with the Trimble Pro XRS receivers in the backpack, using the clamps. For car mounting, remove the clamps and plug units directly into car.\label{Fig:lead_acid_battery}](figs/lead_acid_battery.jpg)

![Batteries
in the back of the Pro XRS handheld units. These may need to be checked
if the units are not working.\label{Fig:trimble_tsc1_receiver_battery}](figs/trimble_tsc1_receiver_battery.jpg)

## Collecting Data

Once we have the unit setup in the car or in the backpack, we are ready
to log data. Follow the instructions in Figure \ref{Fig:trimble_data_collect_1}-\ref{Fig:trimble_data_collect_4}.

![Turn on
the TSC-1 and wait for the GPS to connect. You will need at least 5
satellites to begin collection data. NOTE that you have to set the
antenna height in Configuration->GPS rover options->Antenna.
Measure the height from the ground to the bottom of the antenna. In GPS
rover options, you can also set the logging interval for the point data.
Usually we use a 1-2 second interval.\label{Fig:trimble_data_collect_1}](figs/trimble_data_collect_1.jpg)

![Navigate to Data Collection and
create a new file. Either sort files by date (R031516 for Rover,
March-15-2016) or by data element (terrace 1). Once this file is created
we will log our data for the day in it. We can re-open the file with
Open existing file, in case we turn the device off, but want to add more
points to the file.\label{Fig:trimble_data_collect_2}](figs/trimble_data_collect_2.jpg)

![Make sure to store the data on the
PC card (and not the TSC-1 memory).\label{Fig:trimble_data_collect_3}](figs/trimble_data_collect_3.jpg)

![You want
to generate point data and automatically log the data every 2 seconds
(or so). When you are done logging the data press Enter to store the
points in the file you created. Now it is safe to power off the device
and take the data off onto a computer for further processing.\label{Fig:trimble_data_collect_4}](figs/trimble_data_collect_4.jpg)

# Downloading data from Trimble Pro XRS

## Install Data Transfer Utility and Pathfinder Office

Install and open the Data Transfer Utility from Trimble (free program:
<http://www.trimble.com/datatransfer/>). This program will transfer the
data from the CF card in the TSC-1 unit to an SSF format, which can be
converted to RINEX files in Trimble Pathfinder Office (email
<purinton@uni-potsdam.com> if this program is not available to you).

## Downloading data from TSC-1 with Asset Surveyor (5.2x) – PCMCIA or CF card

Use the following steps to transfer data from the CF card to the
computer for the TSC-1 (Figure \ref{Fig:trimble_data_collect_5}-\ref{Fig:trimble_data_collect_8}).

![Open the
TSC-1.\label{Fig:trimble_data_collect_5}](figs/trimble_data_collect_5.jpg)

![Remove the PCMCIA/CF card from the
TSC-1 (look for the up label).\label{Fig:trimble_data_collect_6}](figs/trimble_data_collect_6.jpg)

![Remove
the CF (Compact Flash) card.\label{Fig:trimble_data_collect_7}](figs/trimble_data_collect_7.jpg)

![Use the
USB card reader with a CF slot to transfer all the files for the day to
a folder on the computer.\label{Fig:trimble_data_collect_8}](figs/trimble_data_collect_8.jpg)

# Converting data to SSF and RINEX

Now that we have the files for the day, we can change them to SSF format
with the Data Transfer Utility and then to RINEX in Pathfinder Office.
RINEX files include observations (.obs) and navigation (.nav). Follow
the steps in Figure \ref{Fig:trimble_data_transfer_1}-\ref{Fig:trimble_data_transfer_6}).

![Open the Data Transfer Utility,
select Devices>New. Create a New Device as a GIS Folder.\label{Fig:trimble_data_transfer_1}](figs/trimble_data_transfer_1.jpg)

![In the next step, select the folder where you transferred the
daily data to. \label{Fig:trimble_data_transfer_2}](figs/trimble_data_transfer_2.jpg)

![Select Asset Surveyor and version 5.2. Then finish on the
next screen.\label{Fig:trimble_data_transfer_3}](figs/trimble_data_transfer_3.jpg)

![Now we have a new device in the menu. We connect to the
device with the green check-mark. Then we use Add to select the data
files. We choose the Destination somewhere that we want the SSF files to
go. After we select the files and the destination, we use Transfer All
to convert the files to SSF. Now we can convert from SSF to RINEX in
Pathfinder Office.\label{Fig:trimble_data_transfer_4}](figs/trimble_data_transfer_4.jpg)

![Open Pathfinder Office and go to Utilities>Other>SSF to
RINEX. Select the SSF file we want to convert and choose a destination
folder where the RINEX files will go. Now click OK.\label{Fig:trimble_data_transfer_5}](figs/trimble_data_transfer_5.jpg)

![In this step we need to fill in
information about the data collection. The most important information is
the Observer (who took the data) and the Antenna Height. The Antenna
Height should be automatically read from the SSF file, but make sure the
height is correct. Once we press OK here, the SSF files will be
converted to RINEX files in the destination folder and we are ready to
correct the data in RTKLIB: **See second manual *dGPS Correction with
RTKLIB***.\label{Fig:trimble_data_transfer_6}](figs/trimble_data_transfer_6.jpg)

