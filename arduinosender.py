from serial import Serial
import serial.tools.list_ports
from tkinter import Tk, StringVar, ttk, Button


class ArduinoSender:
	SerialCom = 0
	ser = None
	Port = 115200
	def __init__(self) -> None:
		ports = serial.tools.list_ports.comports()

		def S_StartSerial():
			self.SerialCom = S_Combx.get().split(' ')[0]
			S_root.destroy()

			self.ser = Serial(self.SerialCom, self.Port, timeout = 0.005)

		S_root = Tk()
		S_root.geometry("450x100")
		S_root.title("포트 설정")

		S_CombxString = StringVar()
		S_Combx = ttk.Combobox(textvariable = S_CombxString,width=40)
		S_Combx['value'] = ports
		S_Combx.current(0)
		S_Combx.pack()

		S_Button = Button(S_root, text = "시리얼 시작", command = S_StartSerial, width=40)
		S_Button.pack()

		S_root.mainloop()

	def Send(self, txt):
		self.ser.write(txt.encode())
		print(txt)