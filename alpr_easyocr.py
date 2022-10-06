import cv2
import re
import easyocr

plateCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")

cap = cv2.VideoCapture('licence_plate.mp4')

frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
franeHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
print(frameWidth)
print(franeHeight)
print(fps)
minArea = 5000
count = 0

# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('aplr_test_result.avi', fourcc, 30, (1920, 1080))

while True:
    ret, img = cap.read()

    # Quit when the input video file ends
    if not ret:
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)
    print(type(numberPlates))

    for (x, y, w, h) in numberPlates:
        print(w)
        print(h)
        area = w * h
        imgRoi = img[y:y + h, x:x + w]

        reader = easyocr.Reader(['en'])
        result = reader.readtext(imgRoi, text_threshold=0.5)
        if len(result) != 0:
            text = result[0][-2]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            print(text)
        else:
            print("Number plate not found")
            pass

    # Write the resulting image to the output video file
    output_movie.write(img)
    img2 = cv2.resize(img, (540, 540))
    cv2.imshow("ROI", img2)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()