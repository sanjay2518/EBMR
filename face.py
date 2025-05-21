import cv2
from deepface import DeepFace

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Analyze the face for emotions
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Extract emotion details
        dominant_emotion = analysis[0]['dominant_emotion']
        print(f"Detected Emotion: {dominant_emotion}")

        # Display result on video frame
        cv2.putText(frame, f"Emotion: {dominant_emotion}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except Exception as e:
        print("Error:", e)

    # Show the frame
    cv2.imshow("Live Face Emotion Recognition", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
