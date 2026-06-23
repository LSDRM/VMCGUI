def init():
    """
    Initialize global variables for the VMCGUI application.
    
    This function sets up the initial state of global variables used throughout
    the application, including URL storage, execution flags, data windows,
    plot identifiers, and current kit information.
    
    :return: None
    :rtype: None
    """
    global url, firstExec, DataWindow, dataPlotID, currentKit
    url = ''
    firstExec = True
    DataWindow = []
    dataPlotID = 0
    currentKit = ''