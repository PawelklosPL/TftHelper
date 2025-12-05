import time

from capture.screen_capture import ScreenCapture
from capture.ocr import OcrEngine
from storage.json_storage import JsonStorage


# 1) KONFIGURACJA – tu wpiszesz swoje współrzędne
#    GOLD_REGION = (left, top, width, height)
GOLD_REGION = (950, 880, 50, 30)  # <<< PRZYKŁAD, zmienisz na swoje wartości
MAP_REGION = (765, 10, 50, 30)
EXPO_REGION = (400, 880, 50, 30)
PLAYER_LEVEL_REGION = (315, 880, 40, 30)

# print("Map:" + read_digit_from_screen(765, 10, 50, 30))
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
    global_map: str = ""
    global_expo: str = ""
    global_player_level: int = 0

    try:
        while True:
            gold_image = screen.grab_region(GOLD_REGION)
            gold_value = ocr.read_number(gold_image)

            map_image = screen.grab_region(MAP_REGION)
            map_value = ocr.read_text(map_image)

            expo_image = screen.grab_region(EXPO_REGION)
            expo_value = ocr.read_text(expo_image)

            player_level_image = screen.grab_region(PLAYER_LEVEL_REGION)
            player_level_value = ocr.read_number(player_level_image)

            now_ts = time.time()
            
            # We check each value separately
            gold_changed = global_gold != gold_value
            map_changed = global_map != map_value
            expo_changed = global_expo != expo_value
            player_level_changed = global_player_level != player_level_value

            if gold_changed or map_changed or expo_changed or player_level_changed:
                storage.append_state(
                    timestamp=now_ts,
                    gold=gold_value,
                    map=map_value,
                    expo=expo_value,
                    player_level=player_level_value,
                )
                if gold_changed:
                    print(f"[{now_ts:.2f}] Gold: {gold_value}")
                    global_gold = gold_value
                if map_changed:
                    print(f"[{now_ts:.2f}] Map: {map_value}")
                    global_map = map_value
                if expo_changed:
                    print(f"[{now_ts:.2f}] Expo: {expo_value}")
                    global_expo = expo_value
                if player_level_changed:
                    print(f"[{now_ts:.2f}] Player Level: {player_level_value}")
                    global_player_level = player_level_value
            time.sleep(INTERVAL_S)

    except KeyboardInterrupt:
        print("\nReading stopped (CTRL+C).")
    finally:
        storage.close()


if __name__ == "__main__":
    main()
