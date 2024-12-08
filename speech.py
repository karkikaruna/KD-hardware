
import cv2
import speech_recognition as sr
import threading

import pyttsx3



# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Initialize the recognizer
recognizer = sr.Recognizer()

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Shared flags
face_detected = False
exit_program = False  # Flag to terminate both threads

def detect_face():
    """Detect face using OpenCV."""
    global face_detected, exit_program
    cap = cv2.VideoCapture(0)  # Open the webcam
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    while not exit_program:  # Run until exit_program is True
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture video frame.")
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Update the shared flag based on face detection
        face_detected = len(faces) > 0

        # Draw rectangles around detected faces (optional)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Show the video feed
        cv2.imshow("Face Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()
    exit_program = True  # Ensure the speech thread exits as well


def speak(text):
    """Speak the given text."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_for_directions():
    """Continuously listen for directions when a face is detected."""
    global face_detected, exit_program

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for directions... (say 'exit' to stop)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        while not exit_program:  # Run until exit_program is True
            if face_detected:
                try:
                    # Capture audio
                    print("Listening for commands...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    # Recognize speech using Google Web Speech API
                    detected_text = recognizer.recognize_google(audio).lower()
                    print(f"You said: {detected_text}")

                    # Check for direction commands
                    if "right" in detected_text:
                        print("Detected: Right")
                        speak("Turning right")
                    elif "left" in detected_text:
                        print("Detected: Left")
                        speak("Turning left")
                    elif "front" in detected_text:
                        print("Detected: Front")
                        speak("Moving forward")
                    elif "back" in detected_text:
                        print("Detected: Back")
                        speak("Reversing")
                    elif "stop" in detected_text:
                        print("Detected: Stop")
                        speak("Stopping")
                    elif "exit" in detected_text:
                        print("Exiting program. Goodbye!")
                        speak("Goodbye")
                        exit_program = True  # Set the flag to terminate both threads
                        break
                except sr.UnknownValueError:
                    print("I didn't catch that. Please try again.")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")
                    break
                except sr.WaitTimeoutError:
                    print("No speech detected. Continuing...")
            else:
                print("No face detected. Waiting...")
                threading.Event().wait(1)  # Wait for 1 second before checking again


# def listen_for_directions():
#     """Continuously listen for directions when a face is detected."""
#     global face_detected, exit_program
#     with sr.Microphone() as source:
#         print("Listening for directions... (say 'exit' to stop)")
#         recognizer.adjust_for_ambient_noise(source, duration=0.5)

#         while not exit_program:  # Run until exit_program is True
#             if face_detected:
#                 try:
#                     # Capture audio
#                     print("Listening for commands...")
#                     audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
#                     # Recognize speech using Google Web Speech API
#                     detected_text = recognizer.recognize_google(audio).lower()
#                     print(f"You said: {detected_text}")

#                     # Check for direction commands
#                     if "right" in detected_text:
#                         print("Detected: Right")
#                     elif "left" in detected_text:
#                         print("Detected: Left")
#                     elif "front" in detected_text:
#                         print("Detected: Front")
#                     elif "back" in detected_text:
#                         print("Detected: Back")
#                     elif "stop" in detected_text:
#                         print("Detected: Ok Riya")
#                     elif "exit" in detected_text:
#                         print("Exiting program. Goodbye!")
#                         exit_program = True  # Set the flag to terminate both threads
#                         break
#                 except sr.UnknownValueError:
#                     print("I didn't catch that. Please try again.")
#                 except sr.RequestError as e:
#                     print(f"Error with the speech recognition service: {e}")
#                     break
#                 except sr.WaitTimeoutError:
#                     print("No speech detected. Continuing...")
#             else:
#                 print("No face detected. Waiting...")
#                 threading.Event().wait(1)  # Wait for 1 second before checking again

def main():
    """Main program to run face detection and speech recognition simultaneously."""
    global exit_program
    # Create threads for face detection and speech recognition
    face_thread = threading.Thread(target=detect_face)
    speech_thread = threading.Thread(target=listen_for_directions)

    # Start both threads
    face_thread.start()
    speech_thread.start()

    # Wait for both threads to finish
    face_thread.join()
    speech_thread.join()

    # Ensure program exits cleanly
    print("Program has terminated.")

# Run the main function
if __name__ == "__main__":
    main()

