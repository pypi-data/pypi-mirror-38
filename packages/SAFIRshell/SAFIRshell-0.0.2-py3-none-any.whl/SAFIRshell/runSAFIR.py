# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-09-17"

#
# run SAFIR through Python shell
#

#####################
## REFERENCE PATHS ##
#####################

## system path SAFIR executable ##
SAFIRpath="C:/SAFIR/SAFIR.exe"

####################
## MODULE IMPORTS ##
####################

# standard module reads
import os
import subprocess
import shutil

# local function reads
# NONE

# distant function reads
# directory="C:/Users/rvcoile/Google Drive/Research/Codes/Python3.6/REF/rvcpy"
# sys.path.append(directory)
# from PrintAuxiliary import Print_DataFrame


##############
## FUNCTION ##
##############

def SAFIR_run(file,path=SAFIRpath,SW_removeItem=False):
	# run SAFIR *.in file
	#	copy *.tem file to Python directory in case of structural analysis

	## check type of SAFIR calcuation
	SAFIRtype=SAFIR_type(file)

	## Run calculation ##
	## if Thermal2D ==> run calculation
	if SAFIRtype=='Thermal2D': SAFIR_exe(path,file) # run SAFIR
	## else (Structural calculation) ==> determine and copy *.tem file to Python dir
	else:
		## move *.tem file to SAFIRpy working directory
		temfilepath,temname=SAFIR_TEMinIN(file) # determine *.tem file (full path - *.in directory assumed)
		# temtargetpath=os.getcwd()+'\\'+'tmp.tem'
		temtargetpath=os.getcwd()+'\\'+temname
		if temtargetpath!=temfilepath: shutil.copy(temfilepath,temtargetpath) # copy *.tem file to SAFIRpy working directory
		## run SAFIR
		SAFIR_exe(path,file)
		## remove *.tem file from SAFIRpy directory - exception if directory equals original *.tem location
		if SW_removeItem: os.remove(temtargetpath)
		# if os.path.exists(os.getcwd()+'\\comeback'): os.remove(os.getcwd()+'\\comeback') # comeback removal - FAIL - administrator rights

def SAFIR_exe(path,file):

	## remove *.in extension
	file=file[0:-3] 

	## run through subprocess
	subprocess.call([path,file])

def SAFIR_type(file):
	# returns type of *.in file: Thermal2D, Structural2D, Structural3D

	with open(file) as f:
		line=f.readline() # first line
		line=f.readline().rstrip() # second line and remove newline indication

	if line == 'Safir_Thermal_Analysis': return 'Thermal2D'
	if line == 'Safir_Static_2D_Analysis': return 'Structural2D'
	if line == 'Safir_Static_3D_Analysis': return 'Structural3D'

def SAFIR_TEMinIN(file):
	# returns name *.TEM file referenced in *.IN file

	with open(file) as f:
		line=f.readline()
		while len(line)>0:
			line=f.readline() # read line
			if '.tem' in line:
				line=line.rstrip() # remove newline character
				infolderpath='\\'.join(file.split('\\')[0:-1]) # path to folder of *.in file
				temfilepath=infolderpath+'\\'+line
				return temfilepath,line # returns full path and name only of *.tem file


#########################
## STAND ALONE - DEBUG ##
#########################

if __name__ == "__main__": 

	########################
	## SWITCH FOR TESTING ##
	########################

	SW_testcase=4
	SW_debug=False



	## SWITCH ##
	if not SW_debug:

	###############
	## EXECUTION ##
	###############

		## *.in file without extension ##
		# NOTES
		# *.in file path should not include a "."
		if SW_testcase==1:
			# temperature calculation - steel profile
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\3DsteelbeamPy\\w21x44"
			# success confirmed
			infile+=".in" # add *.in extension
		if SW_testcase==2:
			# 3D structural calculation - frame (concrete columns, steel beam) example case JHU training
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\3Dframe_mod\\3dframe"
			# seemingly limitation on *.in file path length
			# *.tem files should be copied to directory SAFIRpy
			# TO DO
			# - check if run refers to structural calc or thermal calc
			# - copy *.tem files in case of structural calc to SAFIRpy directory
			infile+=".in" # add *.in extension
		if SW_testcase==3:
			# 2D structural calculation - concrete column - testcase ISO WI Probab
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\2Dcc\\6MN_0mm0"
			infile+=".in" # add *.in extension
		# trial from alternative path
		if SW_testcase==4:
			# 2D structural calculation - concrete column - testcase ISO WI Probab
			infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\modfileTest\\6MN_0mm0.in"

		## execution ##
		SAFIR_run(SAFIRpath,infile)

	###########
	## DEBUG ##
	###########

	# temporary codes for debugging - activate as needed

	else:

		## TRIAL SAFIRtype ##
		#####################
		# ## system path SAFIR executable ##
		# SAFIRpath="C:/SAFIR/SAFIR.exe"

		# ## *.in file without extension ##
		# # NOTES
		# # *.in file path should not include a "."
		# if SW_testcase==1:
		# 	# temperature calculation - steel profile
		# 	infile="C:/Users/rvcoile/Documents/SAFIR/SAFIRpyTest/3DsteelbeamPy/w21x44"
		# 	# success confirmed
		# if SW_testcase==2:
		# 	# structural calculation - frame (concrete columns, steel beam) example case JHU training
		# 	infile="C:/Users/rvcoile/Documents/SAFIR/SAFIRpyTest/3Dframe_mod/3dframe"
		# if SW_testcase==3:
		# 	# 2D structural calculation - concrete column - testcase ISO WI Probab
		# 	infile="C:/Users/rvcoile/Documents/SAFIR/SAFIRpyTest/2Dcc/6MN_0mm0"
		# ## add *.in extension ##
		# infile+=".in"

		# ## debug testing ##
		# SAFIRtype=SAFIR_type(infile)

		# print(SAFIRtype)

		## TRIAL TEMfileIN ##
		#####################

		# # infile
		# infile="C:\\Users\\rvcoile\\Documents\\SAFIR\\SAFIRpyTest\\2Dcc\\6MN_0mm0"
		# infile+=".in"

		# # path to infile folder
		# # infilepath='\\'.join(infile.split('\\')[0:-1])
		# # print("\nTesting")
		# # print(infilepath)

		# # *.tem file indentification
		# temfilepath,temname=SAFIR_TEMinIN(infile)
		# print(temfilepath)
		# print(temname)
		# # print(os.getcwd()+'\\'+temname)

		# temtargetpath=os.getcwd()+'\\'+temname
		# shutil.copy(temfilepath,temtargetpath)

		os.remove(os.getcwd()+'\\comeback')