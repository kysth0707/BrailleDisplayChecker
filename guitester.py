import pygame
import time
import math

class GUITester():
	ScreenWidth = 0
	ScreenHeight = 0
	Title = ""
	screen = None
	DotCount = 0
	ShowFPS = False
	LastTime = 0

	def __init__(self, Width, Height, Title, DotCount, ShowFPS = False) -> None:
		pygame.init()
		self.ScreenWidth = Width
		self.ScreenHeight = Height
		self.Title = Title

		self.DotCount = DotCount
		self.ShowFPS = ShowFPS

		self.screen = pygame.display.set_mode((self.ScreenWidth, self.ScreenHeight))
		pygame.display.set_caption(self.Title)
		self.LastTime = time.time()

	def Update(self, Dots):
		if Dots == None:
			self.screen.fill((0, 0, 0))
			return
		self.screen.fill((0, 0, 0))
		for x in range(self.DotCount):
			for y in range(self.DotCount):
				PosX, PosY = self.ScreenWidth / self.DotCount * x, self.ScreenHeight / self.DotCount * y
				try:
					if Dots[x][y]:
						pygame.draw.rect(self.screen, (255, 255, 255), [int(PosX), int(PosY), int(self.ScreenWidth / self.DotCount), int(self.ScreenHeight / self.DotCount)])
				except:
					return

		if self.ShowFPS:
			FPS = math.floor(1 / (time.time() - self.LastTime))
			self.screen.blit(pygame.font.SysFont("malgungothic", 26).render(str(FPS), True, (127, 127, 127)), (0, 0))
			self.LastTime = time.time()
		pygame.display.update()