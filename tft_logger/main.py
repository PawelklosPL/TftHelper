# main.py
import time

from capture.screen_capture import ScreenCapture
from capture.ocr import OcrEngine
from storage.json_storage import JsonStorage


# 1) KONFIGURACJA – tu wpiszesz swoje współrzędne
#    GOLD_REGION = (left, top, width, height)
GOLD_REGION = (950, 880, 50, 30)  # <<< PRZYKŁAD, zmienisz na swoje wartości
LEVEL_REGION = (765, 10, 50, 30)

# print("Level:" + read_digit_from_screen(765, 10, 50, 30))
# print("Gold:" + read_digit_from_screen(950, 880, 50, 30))
# print("Expo:" + read_digit_from_screen(400, 880, 50, 30))
# print("Na Benchu:" + read_text_from_screen(480, 1040, 80, 30)+ " za "+ read_text_from_screen(650, 1040, 15, 30)+","+
# read_text_from_screen(685, 1040, 130, 30)+ " za "+ read_text_from_screen(855, 1040, 15, 30)+","+
# read_text_from_screen(890, 1040, 130, 30)+ " za "+ read_text_from_screen(1055, 1040, 15, 30)+","+
# read_text_from_screen(1095, 1040, 130, 30)+ " za "+ read_text_from_screen(1255, 1040, 15, 30)+","+
# read_text_from_screen(1290, 1040, 130, 30)+ " za "+ read_text_from_screen(1455, 1040, 15, 30)
# )

INTERVAL_S = 0.5
LOG_PATH = "logs.jsonl"


def main():
    screen = ScreenCapture(monitor_index=2)
    ocr = OcrEngine()

    print("Gold reading started. Stop with CTRL+C.")
    print(f"Gold region: {GOLD_REGION}, interval: {INTERVAL_S}s")

    storage = JsonStorage(LOG_PATH)
    first = True
    global_gold: int = 0
    global_level: int = 0

    try:
        while True:
            gold_image = screen.grab_region(GOLD_REGION)
            gold_value = ocr.read_number(gold_image)

            map_level_image = screen.grab_region(LEVEL_REGION)
            map_level_value = ocr.read_number(map_level_image)

            now_ts = time.time()
            if global_gold != gold_value and global_level != map_level_value:
                storage.append_state(
                    timestamp=now_ts,
                    gold=gold_value,
                    level=map_level_value,
                )
                print(f"[{now_ts:.2f}] Gold: {gold_value}")
                print(f"[{now_ts:.2f}] Level: {map_level_value}")
                global_gold = gold_value
                global_level = map_level_value
            # else:
            #     print("Bez zmian")
            time.sleep(INTERVAL_S)

    except KeyboardInterrupt:
        print("\nReading stopped (CTRL+C).")
    finally:
        storage.close()


if __name__ == "__main__":
    main()
