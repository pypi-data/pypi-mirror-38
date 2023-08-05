# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-11-03"

#
# run SAFIR through Python shell
# - derived from shellSAFIR.py, cfr. local SAFIRpy, dated 2018-09-17
# - acknowledgement Ian Fu, cfr. development PySFE/SAFIRpy
#
# 2018-11-03: version 0.0.1: first initialization


import os
from SAFIRshell.runSAFIR import SAFIR_run
from tkinter import filedialog, Tk, StringVar

##############
## FUNCTION ##
##############

def run(path_input=None):
    ## run SAFIR calculation for given path

    ## Input file path
    if path_input is None:
        root = Tk()
        root.withdraw()
        text_io = filedialog.askopenfile()
        infile = text_io.name
        if infile == '':
            return -1
        else: print(infile)

    ## execution ##
    ## overwrite default SAFIRpath and execute
    # SAFIRpath="C:\\SAFIR\\SAFIR2016c0_proba.exe"
    # SAFIR_run(infile,SAFIRpath)
    # default execution
    SAFIR_run(infile)

#########################
## STAND ALONE - DEBUG ##
#########################

if __name__ == '__main__':
    run()
