# Welcome to VMCGUI documentation

Full documentation for [VMCGUI](https://github.com/LSDRM/VMCGUI), the Versatile Measurement and Control Graphical User Interface.

## Project layout

    APP/
        VMCGUI.py           # The Python App to run.
        requirements.txt    # First time ? Run `pip install -r requirements.txt`
        ...
        Kits/               # Where you should place Python kit scripts for VMCGUI.
            #BlankKit.py    # A template to make your own kits.
            Debug GUI.py    # A kit script to debug the graphical user interface.
            libsForKits/
                ...         # Place here custom Python librairies called by kits.
    ...                     # Documentation & miscellaneous
