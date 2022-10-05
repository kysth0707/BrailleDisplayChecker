from guitester import GUITester
from rgbchecker import RGBChecker

from tkinter import *
from threading import Thread
from sys import platform
import time

# https://stackoverflow.com/questions/57742442/how-to-get-the-height-of-a-tkinter-window-title-bar
class BarHeight(Tk):
	def __init__(self):
		super().__init__()
		super().withdraw()
		Frame(self).update_idletasks()
		self.geometry('350x200+100+100')
		self.update_idletasks()

		offset_y = 0
		if platform in ('win32', 'darwin'):
			import ctypes
			try: # >= win 8.1
				ctypes.windll.shcore.SetProcessDpiAwareness(2)
			except: # win 8.0 or less
				ctypes.windll.user32.SetProcessDPIAware()
		offset_y = int(self.geometry().rsplit('+', 1)[-1])

		bar_height = self.winfo_rooty() - offset_y
		print(f'Height: {bar_height}\nPlatform: {platform}')
		self.destroy()
		return bar_height

RGBCheckers = []
RGBCheckerThreads = []

def Checker(index, ScreenWidth, ScreenHeight, DotCount, ScreenPos, BarHeight):
	return RGBCheckers[index].GetPixelColorsByPIL(ScreenWidth, ScreenHeight, DotCount, ScreenPos, BarHeight)

class SelectorGUI(BarHeight):
	root = None
	ExitFlag = False
	DotCount = 0

	Dots = None

	ScreenPos = (0, 0)
	BarHeight = None
	ScreenWidth = 0
	ScreenHeight = 0

	RGBCheckerLastTime = 0
	RGBCheckerRepeatNum = 0

	def __init__(self, Width, Height, Title, DotCount) -> None:
		self.BarHeight = super().__init__()

		self.DotCount = DotCount
		
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
		# =========================

		self.root.protocol("WM_DELETE_WINDOW", self.OnClose)
		self.root.bind("<Configure>", self.OnResize)

		self.RGBCheckerLastTime = time.time()
		for i in range(5):
			temp = Thread(target=Checker, args = [i, self.ScreenWidth, self.ScreenHeight, self.DotCount, self.ScreenPos, self.BarHeight])
			RGBCheckerThreads.append(temp)
			RGBCheckers.append(RGBChecker())
		

	def IsAlive(self):
		if self.ExitFlag == True:
			return False
		else:
			return True

	def GetDots(self):
		return self.Dots


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
		# return

	def Update(self):
		TempValue = self.root.winfo_geometry().split('+')
		self.ScreenPos = (int(TempValue[1]), int(TempValue[2]))

		# 이미지 가져오기
		# self.Dots = self.GetPixelColorsByPIL()

		TimeDif = time.time() - self.RGBCheckerLastTime
		if TimeDif > 0.02:
			self.RGBCheckerLastTime -= TimeDif

			self.RGBCheckerRepeatNum += 1
			if self.RGBCheckerRepeatNum >= 5:
				self.RGBCheckerRepeatNum = 0
				for i in range(5):
					RGBCheckers[i] = RGBChecker()
					temp = Thread(target=Checker, args = [i, self.ScreenWidth, self.ScreenHeight, self.DotCount, self.ScreenPos, self.BarHeight])
					self.RGBCheckerThreads[i] = temp
			# print(self.RGBCheckerRepeatNum)
			LastTime = time.time()
			RGBCheckerThreads[self.RGBCheckerRepeatNum].start()
			# self.Dots = self.RGBCheckers[self.RGBCheckerRepeatNum].GetPixelColorsByPIL(self.ScreenWidth, self.ScreenHeight, self.DotCount, self.ScreenPos, self.BarHeight)
			print(time.time() - LastTime)


		self.root.update()



MyGUI = SelectorGUI(600, 600, "선택 창", 128)
GUITest = GUITester(600, 600, "GUI 테스터", 128)

# print(MyGUI.BarHeight)
while True:
	if not MyGUI.IsAlive():
		break
	MyGUI.Update()
	GUITest.Update(MyGUI.GetDots())