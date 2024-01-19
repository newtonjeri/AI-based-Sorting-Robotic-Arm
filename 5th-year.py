from ultralytics import YOLO
import cv2
import cvzone
import math

cap = cv2.VideoCapture(0)  # For Webcam
address= "http://172.16.104.223:8080//video"
cap.open(address)

cap.set(3, 1280)
cap.set(4, 720)
# cap = cv2.VideoCapture("../Videos/ppe-3.mp4")  # For Video

model = YOLO("2best.pt")

classNames = ['Arduino-Uno', 'Stapler', 'Calculator', 'Mouse']
myColor = (0, 0, 255)
while True:
    success, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            Centre = center_x, center_y
            print(center_x, center_y)

            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            # cvzone.cornerRect(img, (x1, y1, w, h))

            table_width, table_height = 44.5, 25.4  # set the width and height of the table
            obj_pos_x = (center_x / img.shape[1]) * table_width
            obj_pos_y = (center_y / img.shape[0]) * table_height
            obj_width = (w / img.shape[1]) * table_width

            obj_pos_y = round(obj_pos_y, 2)
            obj_pos_x = round(obj_pos_x, 2)

            position = obj_pos_x, obj_pos_y
            cvzone.putTextRect(img, f'{position}', (max(0, x1 + 90), max(0, y1 + 180)))

            print(obj_pos_x, obj_pos_y)

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            print(currentClass)
            if conf>0.5:
                if currentClass =='Arduino-Uno' or currentClass =='Calculator' or currentClass == "Mouse":
                    myColor = (0, 0,255)
                elif currentClass =='Stapler':
                    myColor =(0,255,0)
                else:
                    myColor = (255, 0, 0)

                cvzone.putTextRect(img, f'{classNames[cls]} {conf}',
                                   (max(0, x1), max(30, y1-10)), scale=1, thickness=1,colorB=myColor,
                                   colorT=(255,255,255),colorR=myColor, offset=5)
                cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
