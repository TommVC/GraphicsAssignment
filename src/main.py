import pygame as pg
from GLWindow import *
import pyrr

def main():
	""" The main method where we create and setup our PyGame program """
	window = OpenGLWindow()
	window.initGL()
	running = True
	paused = False
	earthSpeed = 0.01
	moonSpeed = 0.03
	xViewRot = False
	yViewRot = False
	zViewRot = False
	while running:
		if(not(paused)):
			window.render()
		for event in pg.event.get(): # Grab all of the input events detected by PyGame
			if event.type == pg.QUIT:  # This event triggers when the window is closed
				running = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_q:  # This event triggers when the q key is pressed down
					running = False
				if event.key == pg.K_p: #Pause action triggers when p key is pressed down
					if paused:
						paused = False
					else:
						paused= True
				if event.key == pg.K_UP and not(paused):
					earthSpeed+=0.01
					window.setEarthSpeed(earthSpeed)
				if event.key == pg.K_DOWN and not(paused):
					earthSpeed-=0.01
					if earthSpeed < 0 :
						earthSpeed = 0
					window.setEarthSpeed(earthSpeed)
				if event.key == pg.K_RIGHT and not(paused):
					moonSpeed+=0.01
					window.setMoonSpeed(moonSpeed)
				if event.key == pg.K_LEFT and not(paused):
					moonSpeed-=0.01
					if moonSpeed < 0 :
						moonSpeed = 0
					window.setMoonSpeed(moonSpeed)
				
				if event.key == pg.K_d and not(paused):
					if(yViewRot):
						yViewRot = False
					else:
						yViewRot = True
					window.setYRotation(yViewRot)

				if event.key == pg.K_w and not(paused):
					if(xViewRot):
						xViewRot = False
					else:
						xViewRot = True
					window.setXRotation(xViewRot)
	
				if event.key == pg.K_s and not(paused):
					if(zViewRot):
						zViewRot = False
					else:
						zViewRot = True
					window.setZRotation(zViewRot)
				
				if event.key == pg.K_r and not(paused):
					xViewRot = False
					yViewRot = False
					zViewRot = False
					window.reset()

					

	window.cleanup()
	pg.quit()


if __name__ == "__main__":
	main()