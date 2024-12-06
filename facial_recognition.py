import cv2
from deepface import DeepFace
# Start the webcam
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Perform emotion detection using DeepFace
    try:
        # Analyze the frame for emotions
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        # Get the dominant emotion (with the highest score)
        emotion = analysis[0]['dominant_emotion']
    except Exception as e:
        print(f"Error during emotion detection: {e}")
        emotion = "Unknown"

    # Display the emotion on the frame
    cv2.putText(frame, f"Emotion: {emotion}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the frame with the emotion
    cv2.imshow("Emotion Detection", frame)

    # Press 'q' to quit the video capture
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cam.release()
cv2.destroyAllWindows()
