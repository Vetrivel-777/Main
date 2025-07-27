from ultralytics import YOLO
import cv2
import requests
import time

# Load YOLOv8 model
model = YOLO("best1.pt")

# URL of NodeMCU Access Point (default)
NODEMCU_IP = "http://192.168.4.1/"

# Map your class names to robot commands (update these to match your training labels!)
class_to_command = {
    "left": "left",
    "right": "right",
    "stop": "stop",
    "forward": "forward",
    "backward": "backward"
}

# Reverse the mapping to get class IDs
id_to_command = {}

for idx, name in model.names.items():
    if name in class_to_command:
        id_to_command[idx] = class_to_command[name]

# Timing to prevent spamming requests
last_command = ""
last_time = 0
command_delay = 1  # seconds

def send_command(command):
    global last_command, last_time
    current_time = time.time()
    if command != last_command or (current_time - last_time) >= command_delay:
        try:
            requests.get(NODEMCU_IP + command)
            print(f"Sent: {command}")
            last_command = command
            last_time = current_time
        except:
            print("Failed to send HTTP request")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Failed to open webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference
    results = model.predict(source=frame, conf=0.5, verbose=False)

    # Annotate frame
    annotated_frame = results[0].plot()

    # Get detected classes
    boxes = results[0].boxes
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            class_id = int(box.cls[0].item())
            if class_id in id_to_command:
                command = id_to_command[class_id]
                send_command(command)
                break
    else:
        send_command("stop")

    # Show webcam
    cv2.imshow("Gesture Control", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()