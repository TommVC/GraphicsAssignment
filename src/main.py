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
	xViewRot = 0
	yViewRot = 0
	zViewRot = 0
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
					yViewRot += 1
					if(yViewRot > 360):
						yViewRot-=360
					window.setYRotation(yViewRot)
				if event.key == pg.K_a and not(paused):
					yViewRot -= 1
					if(yViewRot < 0):
						yViewRot+=360
					window.setYRotation(yViewRot)

				if event.key == pg.K_w and not(paused):
					xViewRot += 1
					if(xViewRot > 360):
						xViewRot-=360
					window.setXRotation(xViewRot)
				if event.key == pg.K_s and not(paused):
					xViewRot -= 1
					if(xViewRot < 0):
						xViewRot+=360
					window.setXRotation(xViewRot)

				if event.key == pg.K_r and not(paused):
					zViewRot += 1
					if(zViewRot > 360):
						zViewRot-=360
					window.setZRotation(zViewRot)
				if event.key == pg.K_t and not(paused):
					zViewRot -= 1
					if(zViewRot < 0):
						zViewRot+=360
					window.setZRotation(zViewRot)

					

	window.cleanup()
	pg.quit()


if __name__ == "__main__":
	main()