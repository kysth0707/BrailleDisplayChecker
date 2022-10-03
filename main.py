from tkinter import *

class SelectorGUI():
	ScreenWidth = 0
	ScreenHeight = 0
	root = None
	ExitFlag = False
	Dots = 0

	def __init__(self, Width, Height, Title, Dots) -> None:
		self.Dots = Dots
		
		self.ScreenWidth = Width
		self.ScreenHeight = Height
		
		self.root = Tk()
		self.root.title(Title)
		self.root.geometry(f"{Width}x{Height}")
		self.root.resizable(True, True)

		# https://stackoverflow.com/questions/19080499/transparent-background-in-a-tkinter-window
		# 투명 배경
		self.root.image = PhotoImage(file='TransparentImage.png')
		label = Label(self.root, image = self.root.image, bg='white')
		self.root.geometry(f"{Width}x{Height}")
		self.root.wm_attributes("-topmost", True)
		self.root.wm_attributes("-transparentcolor", "white")
		label.pack()

		self.root.protocol("WM_DELETE_WINDOW", self.OnClose)
		self.root.bind("<Configure>", self.OnResize)

	def OnClose(self):
		self.ExitFlag = True
		self.root.destroy()

	def OnResize(self, e):
		if self.ScreenWidth != self.root.winfo_width():
			# Width changed
			self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_width()}")

		elif self.ScreenHeight != self.root.winfo_height():
			# Height changed
			self.root.geometry(f"{self.root.winfo_height()}x{self.root.winfo_height()}")

		elif self.ScreenWidth != self.root.winfo_width() and self.ScreenHeight != self.root.winfo_height():
			# Width / Height changed
			self.root.geometry(f"{self.root.winfo_height()}x{self.root.winfo_height()}")

		self.ScreenWidth, self.ScreenHeight = self.root.winfo_width(), self.root.winfo_height()

	def Update(self):
		self.root.update()

	def IsAlive(self):
		if self.ExitFlag == True:
			return False
		else:
			return True



MyGUI = SelectorGUI(300, 300, "선택 창")
while True:
	if not MyGUI.IsAlive():
		break
	MyGUI.Update()