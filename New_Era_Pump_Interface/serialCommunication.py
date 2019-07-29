import serial
from tkinter import Tk
from tkinter import simpledialog
from tkinter import messagebox

def getPort():
	root = Tk()
	root.withdraw()
	num = simpledialog.askinteger("Input", "What port number is the pump connected to (default is 4)",parent = root)
	return num,root

def destroyPrompt(root):
	root.destroy

class Pump:
	
	def __init__(self, portNumber):
		
		self.port = "COM%d" % portNumber
		try:

			ser = serial.Serial(self.port, 9600,timeout = .5)
			ser.write('RESET\x0D'.encode())
		except:
			self.status = False
		else:
			self.ser = ser
			
			self.status = ser.isOpen()
			#maybe change baud rate here
			#self.ser.write()

	def sendCmd(self,cmd):


		self.ser.write(cmd.encode())
		output = self.ser.readline()
		print(output)

	def exit(self):
		self.ser.close()

	def checkConnection(self):
		return self.status

	def errorMessage(self):
		root = Tk()
		root.withdraw()
		messagebox.showerror("Error", "Unable to connect to device, check port number in device mangager and try again.")
		
	def sendRun(self,rate_vol_pairs,units):
		i = 1
		u = units
		for pair in rate_vol_pairs:
			rate = pair[0]
			vol = pair[1]
			fun_rat = 'FUN RAT\x0D'
			phase = f'PHN {i}\x0D'
			rate_cmd = f'RAT {rate} {u}\x0D'
			vol_cmd = f'VOL{vol}\x0D'
			print((rate_cmd,vol_cmd))
			self.sendCmd('CLD WDR\x0D')
			self.sendCmd(phase)
			self.sendCmd(fun_rat)
			self.sendCmd(rate_cmd)
			self.sendCmd(f'VOL{u}\x0D')
			self.sendCmd(vol_cmd)
			self.sendCmd('DIR WDR\x0D')
			i = i+1

		self.sendCmd('RUN\x0D')

	def Pause(self):
		self.sendCmd('STP\x0D')

	def Resume(self):
		self.sendCmd('RUN\x0D')
