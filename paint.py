import glfw
from OpenGL.GL import *
import numpy as np
import imageio
import freetype as ft

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW initialization failed")

# Initialize monitor and window
monitor = glfw.get_primary_monitor()
vidmode = glfw.get_video_mode(monitor)
WIDTH = vidmode.size.width
HEIGHT = vidmode.size.height

# Constants for brush colors and eraser
BRUSH_COLORS = {
    "black": (0.0, 0.0, 0.0),
    "red": (1.0, 0.0, 0.0),
    "green": (0.0, 1.0, 0.0),
    "blue": (0.0, 0.0, 1.0),
    "eraser": (1.0, 1.0, 1.0),
}

BRUSH_SIZES = {
    "small": 5,
    "medium": 10,
    "large": 15,
}

# Initial brush color
current_color = BRUSH_COLORS["black"]
current_size = BRUSH_SIZES["small"]

# Store drawn points and their colors
drawn_points = []


# Callback functions
def key_callback(window, key, scancode, action, mods):
    global current_color, current_size
    if action == glfw.PRESS:
        if key == glfw.KEY_B:
            current_color = BRUSH_COLORS["black"]
        elif key == glfw.KEY_R:
            current_color = BRUSH_COLORS["red"]
        elif key == glfw.KEY_G:
            current_color = BRUSH_COLORS["green"]
        elif key == glfw.KEY_U:
            current_color = BRUSH_COLORS["blue"]
        elif key == glfw.KEY_E:
            current_color = BRUSH_COLORS["eraser"]
        elif key == glfw.KEY_S:
            save_image()
        elif key == glfw.KEY_1:
            current_size = BRUSH_SIZES["small"]
        elif key == glfw.KEY_2:
            current_size = BRUSH_SIZES["medium"]
        elif key == glfw.KEY_3:
            current_size = BRUSH_SIZES["large"]


def mouse_button_callback(window, button, action, mods):
    global drawing
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            drawing = True
        elif action == glfw.RELEASE:
            drawing = False


def save_image(filename="drawing.png"):
    widht, height = glfw.get_framebuffer_size(window)
    glReadBuffer(GL_FRONT)
    pixels = glReadPixels(0, 0, widht, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = np.frombuffer(pixels, dtype=np.uint8).reshape(height, widht, 3)
    image = np.flipud(image)  # Flip the image vertically
    imageio.imwrite(filename, image)


window = glfw.create_window(WIDTH, HEIGHT, "2D Drawing Program", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window creation failed")

glfw.make_context_current(window)
glfw.set_key_callback(window, key_callback)
glfw.set_mouse_button_callback(window, mouse_button_callback)

# OpenGL settings
glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glfw.swap_buffers(window)

drawing = False

while not glfw.window_should_close(window):
    glfw.wait_events()

    if drawing:
        x, y = glfw.get_cursor_pos(window)
        y = HEIGHT - y  # Convert to OpenGL coordinates
        drawn_points.append((x, y, current_color, current_size))

    # Draw the canvas
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for point in drawn_points:
        glColor3f(*point[2])
        glPointSize(point[3])
        glBegin(GL_POINTS)
        glVertex2f(point[0], point[1])
        glEnd()

    glfw.swap_buffers(window)

glfw.terminate()
