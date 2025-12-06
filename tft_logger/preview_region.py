# Tymczasowy skrypt do podglądu regionu
from capture.screen_capture import ScreenCapture

# Region do sprawdzenia
REGION = (315, 880, 40, 30)

screen = ScreenCapture(monitor_index=2)
image = screen.grab_region(REGION)

# Pokaż w oknie
image.show()
print(f"Region: {REGION}")

