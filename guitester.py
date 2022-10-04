import pygame

class GUITester():
	ScreenWidth = 0
	ScreenHeight = 0
	Title = ""
	screen = None
	DotCount = 0
	def __init__(self, Width, Height, Title, DotCount) -> None:
		pygame.init()
		self.ScreenWidth = Width
		self.ScreenHeight = Height
		self.Title = Title

		self.DotCount = DotCount

		self.screen = pygame.display.set_mode((self.ScreenWidth, self.ScreenHeight))
		pygame.display.set_caption(self.Title)

	def Update(self, Dots):
		self.screen.fill((0, 0, 0))
		for x in range(self.DotCount):
			for y in range(self.DotCount):
				PosX, PosY = self.ScreenWidth / self.DotCount * x, self.ScreenHeight / self.DotCount * y
				if Dots[x][y]:
					pygame.draw.rect(self.screen, (255, 255, 255), [int(PosX), int(PosY), int(self.ScreenWidth / self.DotCount), int(self.ScreenHeight / self.DotCount)])
		pygame.display.update()