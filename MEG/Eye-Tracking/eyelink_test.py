import expyriment
from eyelink import EyeLinkWrapper

# ==================================================
# Set parameters
# ==================================================
# Colors (RGB format)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

# Define experiment constants
TEXT_DISPLAY_TIME = 5000  # in milliseconds (5 seconds)
BLANK_DISPLAY_TIME = 2000  # in milliseconds (2 seconds)
CIRCLE_DISPLAY_TIME = 1500  # in milliseconds (1.5 seconds)
CIRCLE_RADIUS = 20  # Circle radius in pixels
TEXT_SIZE = 50  # Text size (default is 32)

# Define eye-tracker constants
cfg_eyelink = dict()
cfg_eyelink['edf_file_base_name'] = "ss00"
cfg_eyelink['background_color'] = GREY
cfg_eyelink['foreground_color'] = WHITE
cfg_eyelink['calibration_target_size'] = 100
el = EyeLinkWrapper(cfg_eyelink)

# ==================================================
# Initialize the experiment
# ==================================================
expyriment.control.defaults.opengl = 1
exp = expyriment.design.Experiment(name="Eye Tracking Task")
expyriment.control.initialize(exp)

# ==================================================
# Initialize the eye-tracker
# ==================================================
el.initialize()  # Initializes EyeLink and opens the first EDF file
el.calibrate()  # Calibrate once before starting blocks

# ==================================================
# Initialize the stimuli components
# ==================================================
# Set the background color to grey
expyriment.stimuli.defaults.clear_surface_color = GREY

# Prepare stimuli with white text and circle
text = expyriment.stimuli.TextLine("Please follow the circle with your eyes!", text_size=TEXT_SIZE, text_colour=WHITE)
circle = expyriment.stimuli.Circle(CIRCLE_RADIUS, colour=WHITE)

# ==================================================
# Start the experiment
# ==================================================
expyriment.control.start(subject_id=0, skip_ready_screen=True)

# Screen size
screen_size = exp.screen.window_size
middle_left = (-screen_size[0] // 2, 0)
left_up = (-screen_size[0] // 2, screen_size[1] // 2)
middle_center = (0, 0)
down_right = (screen_size[0] // 2, -screen_size[1] // 2)
up_right = (screen_size[0] // 2, screen_size[1] // 2)
down_middle = (0, -screen_size[1] // 2)

# ==================================================
# Show text message
# ==================================================
text.present()
exp.clock.wait(TEXT_DISPLAY_TIME)

# Initialize EyeLink for the new block
el.start_new_block()
# Start recording for the new block
el.start_recording()
# Send message to the eye-tracker
el.send_message(f"First run started.")

# ==================================================
# Show blank screen (grey background)
# ==================================================
expyriment.stimuli.BlankScreen().present()
exp.clock.wait(BLANK_DISPLAY_TIME)

# ==================================================
# Show circle at different positions
# ==================================================
positions = [middle_left, left_up, middle_center, down_right, up_right, down_middle]

for pos in positions:
    el.send_message("Position changed")
    circle.position = pos
    circle.present()
    exp.clock.wait(CIRCLE_DISPLAY_TIME)

# ==================================================
# End the eye-tracker
# ==================================================
el.send_message("First run ended.")
el.stop_recording()
el.close()

# ==================================================
# End the experiment
# ==================================================
expyriment.control.end()
