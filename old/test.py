# import pygame
# import win32.win32gui as win32gui
# import win32.win32console as win32con
# import win32.win32api as win32api
# import win32.win32console

# class SelectorGUI():
# 	ScreenWidth = 0
# 	ScreenHeight = 0
# 	Screen = None
# 	def __init__(self, Width, Height) -> None:
# 		self.ScreenWidth = Width
# 		self.ScreenHeight = Height
		
# 		pygame.display.set_mode((self.ScreenWidth, self.ScreenHeight), pygame.RESIZABLE)

# 		Fuchsia = (0, 0, 0)  # Transparency color

# 		# Create layered window
# 		hwnd = pygame.display.get_wm_info()["window"]
# 		win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
# 							win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# 		# Set window transparency color
# 		win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*Fuchsia), 0, win32con.LWA_COLORKEY)

# 	def Update(self):
# 		pygame.display.update()
		
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT: 
# 				pygame.quit()