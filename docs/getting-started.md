# Getting started with VMCGUI

## Prerequisites

- Having Python > v3.8 installed

## Installation

	git clone https://github.com/LSDRM/VMCGUI
	cd VMCGUI/APP
	pip install -r requirements.txt

## Run VMCGUI

Move to the `APP/` folder in your shell and run:

	py VMCGUI.py

You should see a small window (also called start window) appearing named **VMCGUI - choose your kit**.
On this window, you should have at least 3 buttons:

- **Debug GUI**: The default available 'kit'. This one open the VMCGUI interface by plotting fake values, so you can test the interface.
- **Personalized Kit**: *BETA*. This button is for a future development, to automate kit generation.
- **Load Data**: To open/plot and process data/measures recorded with VMCGUI.

!!! note
	When you launch VMCGUI, it parses `.py` files (except those starting with an `#`) in the `APP/Kits/` folder.
	All available `.py` files in this folder will add corresponding buttons on the start window, using filenames as buttons text.

## Adding new kits

To add new kits, you can either check for [existing kits](https://github.com/LSDRM/VMC_Kits) and follow their installation instructions or [make your own kit](tutorials/make-a-kit.md).