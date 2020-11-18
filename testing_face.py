import cv2 as cv
import fungsi

detector = fungsi.faceDetect('dnn')
cam = cv.VideoCapture(0)

while True:
	_, frame = cam.read()
	#frame = cv.flip(frame, 1)
	faces = detector.face_dnn(frame, conf=0.8)

	if len(faces) >= 1:
		for (x, y, w, h) in faces:
			cv.rectangle(frame, (x,y), (x+w, y+h), color=(57,196,35), thickness=4)
	
	cv.imshow('Image', frame)
	if cv.waitKey(20) & 0xFF == ord('q'):
		break

cam.release()
cv.destroyAllWindows()