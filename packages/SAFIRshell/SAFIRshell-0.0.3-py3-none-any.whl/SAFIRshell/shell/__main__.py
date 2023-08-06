# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-11-03"

#
# run SAFIR through Python shell
# - derived from shellSAFIR.py, cfr. local SAFIRpy, dated 2018-09-17
# - acknowledgement Ian Fu, cfr. development PySFE/SAFIRpy
#
# 2018-11-03: version 0.0.1: first initialization
# 2018-11-03: version 0.0.2: update allows to pass *.in file immediately with command "python -m SAFIRshell.shell [*.in]"


import os
import sys
from SAFIRshell.runSAFIR import SAFIR_run
from tkinter import filedialog, Tk

##############
## FUNCTION ##
##############

def run(infile=None):
    ## run SAFIR calculation for given path

    ## Input file path
    if infile is None:
        root = Tk()
        root.withdraw()
        text_io = filedialog.askopenfile(title = "Select *.in file for SAFIR calculation")
        infile = text_io.name
        if infile == '':
            return -1
        else: print(infile)

    ## execution ##
    SAFIR_run(infile)

#########################
## STAND ALONE - DEBUG ##
#########################

if __name__ == '__main__':

    n_arg=len(sys.argv)-1 # number of arguments passed with script
    
    # assign arguments
    script=sys.argv[0] # script
    infile=None if n_arg==0 else sys.argv[1] # first argument

    # run SAFIR
    run(infile)
