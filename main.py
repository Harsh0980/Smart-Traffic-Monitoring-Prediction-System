import cv2
import torch
import argparse

print("Loading model...")

# Load YOLOv5 model (pretrained)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

vehicle_classes = ['car', 'motorcycle', 'bus', 'truck']

def count_vehicles(results):
    count = 0
    for result in results.xyxy[0]:
        cls = int(result[5])
        label = model.names[cls]
        if label in vehicle_classes:
            count += 1
    return count

def get_green_time(vehicle_count, base_time=3, scale=2):
    return base_time + (vehicle_count * scale)

def run(source):
    print("Starting video...")
    
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("❌ Cannot open video")
        return

    cv2.namedWindow("Smart Traffic System", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("End of video")
            break

        print("Processing frame...")

        results = model(frame)
        vehicle_count = count_vehicles(results)
        green_time = get_green_time(vehicle_count)

        annotated_frame = results.render()[0].copy()

        cv2.putText(annotated_frame, f'Vehicles: {vehicle_count}', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(annotated_frame, f'Green Time: {green_time}s', (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Smart Traffic System", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Program started")

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='traffic.mp4')

    args = parser.parse_args()

    print("Running with:", args.source)

    run(args.source)
