import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr

from Geometry import Geometry

class OpenGLWindow:

    def __init__(self):
        self.sun = None
        self.sunRot = 0
        self.earth = None
        self.moon = None
        self.earthRot = 0
        self.earthSpeed = 0.01
        self.moonRot = 0
        self.moonSpeed = 0.03
        self.colourLoc = None
        self.modelMatrixLoc = None
        self.textures = None
        self.clock = pg.time.Clock()

    def setEarthSpeed(self, speed):
        self.earthSpeed = speed

    def setMoonSpeed(self, speed):
        self.moonSpeed = speed

    def loadShaderProgram(self, vertex, fragment):
        with open(vertex, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))

        return shader

    def initGL(self, screen_width=720, screen_height=720):
        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 2)

        pg.display.set_mode((screen_width, screen_height), pg.OPENGL | pg.DOUBLEBUF)

        glEnable(GL_DEPTH_TEST)
        # Uncomment these two lines when perspective camera has been implemented
        #glEnable(GL_CULL_FACE)
        #glCullFace(GL_BACK)
        glClearColor(0, 0, 0, 1)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.textures = glGenTextures(3)

        # Note that this path is relative to your working directory when running the program
        # You will need change the filepath if you are running the script from inside ./src/

        self.shader = self.loadShaderProgram("./shaders/simple.vert", "./shaders/simple.frag")
        glUseProgram(self.shader)
        self.colourLoc = glGetUniformLocation(self.shader, "objectColor")
        glUniform1i(glGetUniformLocation(self.shader,"imageTexture"), 0)

        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        self.sun = Geometry('./resources/sphere-fixed.obj')
        image = pg.image.load("./resources/sun.png")
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        self.earth = Geometry('./resources/sphere-fixed.obj')
        image = pg.image.load("./resources/earth.png")
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, self.textures[2])
        self.moon = Geometry('./resources/sphere-fixed.obj')
        image = pg.image.load("./resources/moon.png")
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        projectionMatrix = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = screen_width/screen_height, near = 0.1, far = 10,
            dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projectionMatrix
        )
        self.modelMatrixLoc = glGetUniformLocation(self.shader, "model")
        print("Setup complete!")


    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)  # You may not need this line
        self.sunRot += 0.05
        if(self.sunRot > 360):
            self.sunRot-=360
        modelMatrix = pyrr.matrix44.create_identity(dtype=np.float32)
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_scale([0.2,0.2,0.2],dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_y_rotation(np.radians(self.sunRot),dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_translation([0,0,-3],dtype=np.float32)
        )
        glUniformMatrix4fv(self.modelMatrixLoc, 1, GL_FALSE, modelMatrix)
        glUniform3f(self.colourLoc, 1, 1, 1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        glDrawArrays(GL_TRIANGLES, 0, self.sun.vertexCount)


        self.earthRot += self.earthSpeed
        if(self.earthRot > 360):
            self.earthRot -= 360
        modelMatrix = pyrr.matrix44.create_identity(dtype=np.float32)
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_scale([0.1,0.1,0.1],dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_y_rotation(np.radians(self.sunRot),dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_translation([0,0.6,-3],dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_z_rotation(np.radians(self.earthRot),dtype=np.float32)
        )
        glUniformMatrix4fv(self.modelMatrixLoc, 1, GL_FALSE, modelMatrix)
        glUniform3f(self.colourLoc, 1,1,1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        glDrawArrays(GL_TRIANGLES, 0, self.earth.vertexCount)

        self.moonRot += self.moonSpeed
        if(self.moonRot > 360):
            self.moonRot -= 360
        modelMatrix = pyrr.matrix44.create_identity(dtype=np.float32)
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_scale([0.02,0.02,0.02],dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_y_rotation(np.radians(self.sunRot),dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_translation([0,0.8,-3],dtype=np.float32)
        )  
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_translation([0,-0.6,3],dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_z_rotation(np.radians(self.moonRot),dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_translation([0,0.6,-3],dtype=np.float32)
        )
        modelMatrix = pyrr.matrix44.multiply(
            m1= modelMatrix,
            m2 = pyrr.matrix44.create_from_z_rotation(np.radians(self.earthRot),dtype=np.float32)
        )
        glUniformMatrix4fv(self.modelMatrixLoc, 1, GL_FALSE, modelMatrix)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textures[2])
        glUniform3f(self.colourLoc, 1,1,1)
        glDrawArrays(GL_TRIANGLES, 0, self.moon.vertexCount)

        # Swap the front and back buffers on the window, effectively putting what we just "drew"
        # Onto the screen (whereas previously it only existed in memory)
        pg.display.flip()

    def cleanup(self):
        glDeleteVertexArrays(1, (self.vao,))
        self.sun.cleanup()