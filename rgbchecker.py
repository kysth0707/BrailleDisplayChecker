import win32gui
from PIL import ImageGrab

class RGBChecker:
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
	def GetPixelColorsByPIL(self, ScreenWidth, ScreenHeight, DotCount, ScreenPos, BarHeight):
		Image = ImageGrab.grab().load()

		Dots = [[0 for i in range(DotCount)] for j in range(DotCount)] 

		for x in range(DotCount):
			for y in range(DotCount):
				PosX, PosY = (x + 0.5) * ScreenWidth / DotCount + ScreenPos[0], (y + 0.5) * ScreenHeight / DotCount + BarHeight + ScreenPos[1] + 10
				PosX, PosY = int(PosX), int(PosY)
				Dots[x][y] = True if (Image[PosX, PosY][0] > 127) else False
				pass
		return Dots