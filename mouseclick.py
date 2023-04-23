import pyautogui

# Save the current mouse position
original_x, original_y = pyautogui.position()

# Set the target location where you want to click
target_x, target_y = 500, 500

# Move the mouse pointer to the target location
pyautogui.moveTo(target_x, target_y, duration=0)

# Perform a left-click at the target location
pyautogui.click(button='left')

# Move the mouse pointer back to its original location
pyautogui.moveTo(original_x, original_y, duration=0)
