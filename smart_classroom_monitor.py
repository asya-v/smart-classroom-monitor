import cv2
from ultralytics import YOLO
import time
import os
from datetime import datetime

model = YOLO("yolov8n.pt")

CAMERA_URL = "http://YOUR_PHONE_IP:8080/video"
CONFIDENCE = 0.35
LIMIT = 5

SCREENSHOT_FOLDER = "screenshots"
LOG_FILE = "people_log.txt"

LOG_DELAY = 5
SCREENSHOT_DELAY = 10

os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

cap = cv2.VideoCapture(CAMERA_URL)

if not cap.isOpened():
    print("Не удалось открыть камеру")
    print("Проверь адрес камеры или подключение")
    exit()

max_people = 0
last_log_time = 0
last_screenshot_time = 0

occupied_start = None
total_occupied_time = 0


def format_seconds(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def write_log(people_count, max_people, status, occupied_time):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"people: {people_count} | "
            f"max: {max_people} | "
            f"status: {status} | "
            f"occupied_time: {format_seconds(occupied_time)}\n"
        )


def save_screenshot(frame):
    filename = datetime.now().strftime(
        f"{SCREENSHOT_FOLDER}/crowded_%Y%m%d_%H%M%S.jpg"
    )

    cv2.imwrite(filename, frame)
    print(f"Скриншот сохранён: {filename}")


while True:
    ret, frame = cap.read()

    if not ret:
        print("Не удалось получить кадр")
        break

    results = model(
        frame,
        conf=CONFIDENCE,
        classes=[0],
        verbose=False
    )

    people_count = 0

    for result in results:
        for box in result.boxes:
            people_count += 1

            confidence = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Person {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    if people_count > max_people:
        max_people = people_count

    if people_count == 0:
        status = "EMPTY"
        status_color = (180, 180, 180)

    elif people_count <= LIMIT:
        status = "OCCUPIED"
        status_color = (0, 200, 0)

    else:
        status = "CROWDED"
        status_color = (0, 0, 255)

    now = time.time()

    if people_count > 0:
        if occupied_start is None:
            occupied_start = now

        current_occupied_time = total_occupied_time + (
            now - occupied_start
        )

    else:
        if occupied_start is not None:
            total_occupied_time += now - occupied_start
            occupied_start = None

        current_occupied_time = total_occupied_time

    if now - last_log_time > LOG_DELAY:
        write_log(
            people_count,
            max_people,
            status,
            current_occupied_time
        )

        last_log_time = now

    if (
        status == "CROWDED"
        and now - last_screenshot_time > SCREENSHOT_DELAY
    ):
        save_screenshot(frame)
        last_screenshot_time = now

    cv2.putText(
        frame,
        f"People: {people_count}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        f"Max: {max_people}",
        (30, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        f"Status: {status}",
        (30, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        status_color,
        2
    )

    cv2.putText(
        frame,
        f"Occupied: {format_seconds(current_occupied_time)}",
        (30, 175),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 120, 255),
        2
    )

    if status == "CROWDED":
        cv2.putText(
            frame,
            "WARNING: TOO MANY PEOPLE",
            (30, 225),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            3
        )

    cv2.imshow("Smart Classroom Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Программа завершена")
print(f"Максимальное количество людей: {max_people}")
