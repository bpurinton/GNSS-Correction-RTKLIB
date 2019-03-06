---
title: "GNSS Collection and Post-Processing with RTKLIB"
date: "March 2019"
author: "Ben Purinton ([purinton@uni-potsdam.de](purinton@uni-potsdam.de))"
---

This repository contains information on the collection of differential GPS (dGPS) data using a Trimble Pro XRS receiver in [The First Manual](docs/dGPS_trimble_collection_argentina.pdf) and the steps for differential correction using the open-source program [RTKLIB](http://www.rtklib.com/) in [The Second Manual](docs/dGPS_with_RTKLIB.pdf). The ```example_gui``` folder contains all the files you need to follow along with [The Second Manual](docs/dGPS_with_RTKLIB.pdf).

Everything in the manual on PPK processing with RTKLIB can be done from the command-line and/or in Python, but my purpose in the basic walkthrough of the steps is to include all skill levels. 

I've also put up a Python script in the ```scripts``` folder that allow batch processing of dGPS files (in this case collected in Leica *.m00* format) without needing to touch any of the RTKLIB GUIs. It's decently commented, but if it doesn't work on your machine I can help troubleshoot (purinton@uni-potsdam.de). There are some example files in the ```example_python``` folder which should allow you to simply run: 

```
python C:\path\to\GNSS-Correction-RTKLIB\scripts\dGPS_PPK_RTKPOST.py 
```

from the command-line and output the corrected points in *.csv* and *.shp* format. 

To change the script to suit your needs, change the variables on **lines 30-56** of ```dGPS_PPK_RTKPOST.py```. Note the ```rnx2rtkp_options.conf``` file in the ```scripts``` directory, which is passed to RTKLIB at the command-line for setting the correction configuration. Refer to the [RTKLIB Manual](http://www.rtklib.com/prog/manual_2.4.2.pdf) for information on that file and more information in general about RTKLIB.

Enjoy!
