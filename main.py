from camera import Camera
import credentials

# --------------------------------------------------

# cam = Camera(credentials.ip42,
#              credentials.port,
#              credentials.login,
#              credentials.password,
#              True)
#
# # --------------------------------------------------
#
# cam.get_position()
#
# # --------------------------------------------------
#
# # Absolute move
#
# # Move to coordinates
# cam.move_absolute(0.1, -0.5, 0)
#
# # --------------------------------------------------
#
# cam.get_position()

# --------------------------------------------------

cam = Camera(credentials.ip43,
             credentials.port,
             credentials.login,
             credentials.password,
             True)

cam.change_focus(2)

# --------------------------------------------------

# cam.get_position()

# --------------------------------------------------

# Continuous move

# # Move to the right
# cam.move_pan(0, 1)
#
# # Move to the left
# cam.move_pan(-1, 1)
#
# # Move downwards
# cam.move_tilt(-1, 1)
#
# # Move upwards
# cam.move_tilt(1, 1)
#
# # Move diagonally up and right
# cam.move_diagonal(0.5, 0.5, 0.5)
#
# # Move diagonally down and right
# cam.move_diagonal(1, -1, 1)
#
# # Move diagonally up and left
# cam.move_diagonal(-1, 1, 1.5)
#
# # Zoom in
# cam.move_zoom(1, 1)
#
# # Zoom out
# cam.move_zoom(-1, 2)

# # Custom continuous move
# # x, y, z, Tx, Ty, Tz
# cam.move_custom(-1, -0.5, 0.1, 1, 0.5, 1)

# --------------------------------------------------

# cam.get_position()
