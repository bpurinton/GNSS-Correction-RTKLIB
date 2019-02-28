---
title: "GNSS Collection and Post-Processing with RTKLIB"
date: "March 2019"
author: "Ben Purinton ([purinton@uni-potsdam.de](purinton@uni-potsdam.de))"
---

This repository contains information on the collection of differential GPS (dGPS) data using a Trimble Pro XRS receiver in [The First Manual](docs/dGPS_trimble_collection_argentina.pdf) and the steps for differential correction using the open-source program [RTKLIB](http://www.rtklib.com/) in [The Second Manual](docs/dGPS_with_RTKLIB.pdf). The ```example``` folder contains all the files you need to follow along with [The Second Manual](docs/dGPS_with_RTKLIB.pdf).

Everything in the manual on PPK processing with RTKLIB can be done from the command-line and/or in Python, but my purpose in the basic walk-through of the steps is to include all skill levels. I also plan on putting up some rough Python scripts that allow batch-processing of dGPS files without needing to touch any of the RTKLIB GUIs, they should be decently commented, but if they don't work on your machine I can help troubleshoot (purinton@uni-potsdam.de). More on that soon...
