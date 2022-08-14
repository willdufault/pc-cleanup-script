import os
import glob
import getpass
import pathlib
import pywintypes
import win32serviceutil  # in cmd: pip install pywin32

def removeFiles(path):
	# remove all files that are safe to remove (including those in subdirectories)
	files = glob.glob(f"{path}**/*", recursive=True)
	for f in files:
		try:
			os.remove(f)
		except:
			pass
	# remove all empty subdirectories
	for folder in list(os.walk(path)):
		if not os.listdir(folder[0]):
			os.removedirs(folder[0])
	# recreate parent folder if it gets deleted (if empty)
	if not os.path.exists(path):
		os.makedirs(path)
	print(f"cleared {path}")

def disableService(svc):
	os.system("sc config " + svc + " start=disabled")
	print(f"disabled {svc} on startup")
	win32serviceutil.StopService(svc)
	print(f"stopped {svc} or it wasn't running")

def main():
	# remove temp files
	print('removing temp files:')
	user = getpass.getuser()  # your username on this pc
	drive = pathlib.Path.home().drive  # drive windows is installed on
	paths = [f"{drive}/Windows/Temp/", f"{drive}/Users/{user}/AppData/Local/Temp/", f"{drive}/Users/{user}/AppData/Local/NVIDIA/DXCache/"]  # can add more if you want
	'''
	options:

	f"{drive}:/Windows/Temp/"
	- windows temp files

	f"{drive}/Users/{user}/AppData/Local/Temp/"
	- more windows temp files

	f"{drive}/Users/{user}/AppData/Local/NVIDIA/DXCache/"
	- gpu cache (nvidia only), sometimes decreases stutter in games

	f"{drive}/Windows/Prefetch/"
	- does not actually speed anything up, actually slows your machine down but will clear up a tiny amount of space
	'''
	for path in paths:
		removeFiles(path)
	print()  # prettier
	# disable services, NEEDS ADMIN TO DO THIS
	print('disabling services:')
	svcs = ['DiagTrack', 'BITS', 'SysMain']  # service names
	'''
	options:
	
	DiagTrack (Connected User Experiences and Telemetry)
	- Windows Telemetry and Data Collection

	BITS (Background Intelligent Transfer Service)
	- automatically downloads and transfers files in the background, can slow machine down

	SysMain
	- supposedly maintains system performance over time, slows machine down
	'''
	for svc in svcs:
		try:
			disableService(svc)
		except:
			pass
	input("press enter to exit\n")

main()