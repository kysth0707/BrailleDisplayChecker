from guitester import GUITester

from tkinter import *
import win32gui
from sys import platform
from PIL import ImageGrab
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

class SelectorGUI(BarHeight, GUITester):
	root = None
	ExitFlag = False
	DotCount = 0

	Dots = None

	ScreenPos = (0, 0)
	BarHeight = None
	ScreenWidth = 0
	ScreenHeight = 0

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

	# 0.0164 sec / 1 dot ( 32*32 = 16 sec.. )
	# 사용 X
	def GetPixelColor(self, i_x, i_y):
		i_desktop_window_id = win32gui.GetDesktopWindow()
		i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
		long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
		i_colour = int(long_colour)
		win32gui.ReleaseDC(i_desktop_window_id,i_desktop_window_dc)
		return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)

	# 0.06 ~ 0.07 sec / screen ( 32*32 dots )
	def GetPixelColorsByPIL(self):
		Image = ImageGrab.grab().load()

		self.Dots = [[0 for i in range(self.DotCount)] for j in range(self.DotCount)] 

		for x in range(self.DotCount):
			for y in range(self.DotCount):
				PosX, PosY = (x + 0.5) * self.ScreenWidth / self.DotCount + self.ScreenPos[0], (y + 0.5) * self.ScreenHeight / self.DotCount + self.BarHeight + self.ScreenPos[1] + 10
				PosX, PosY = int(PosX), int(PosY)
				self.Dots[x][y] = True if (Image[PosX, PosY][0] > 127) else False
				pass
		

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

	def Update(self):
		TempValue = self.root.winfo_geometry().split('+')
		self.ScreenPos = (int(TempValue[1]), int(TempValue[2]))

		# LastTime = time.time()
		# 이미지 가져오기
		self.GetPixelColorsByPIL()
		# print(time.time() - LastTime)


		self.root.update()



MyGUI = SelectorGUI(600, 600, "선택 창", 32)
GUITest = GUITester(600, 600, "GUI 테스터", 32)

# print(MyGUI.BarHeight)
while True:
	if not MyGUI.IsAlive():
		break
	MyGUI.Update()
	GUITest.Update(MyGUI.GetDots())