import cv2
import speech_recognition as sr
import threading
import pyttsx3
import time


class FaceAndVoiceControl:
    def __init__(self):
        # Initialize text-to-speech engine and speech recognizer
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

        # Load the Haar cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Shared variables and termination event
        self.face_detected = False
        self.terminate_event = threading.Event()

    def detect_face(self):
        """Detect face using OpenCV."""
        cap = cv2.VideoCapture(0)  # Use index 0 for the laptop's built-in camera
        if not cap.isOpened():
            print("Error: Could not access the webcam.")
            return

        try:
            while not self.terminate_event.is_set():  # Run until termination event is set
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture video frame.")
                    break

                # Flip the frame horizontally for a mirror effect
                frame = cv2.flip(frame, 1)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                self.face_detected = len(faces) > 0

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                cv2.imshow("Face Detection", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.terminate_event.set()
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def speak(self, text):
        """Speak the given text."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen_for_commands(self):
        """Listen for and execute commands when a face is detected."""
        with sr.Microphone() as source:
            print("Listening for commands... (say 'exit' to stop)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            while not self.terminate_event.is_set():
                try:
                    if self.face_detected:
                        print("Listening for your command...")
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        detected_text = self.recognizer.recognize_google(audio).lower()
                        print(f"You said: {detected_text}")

                        if "turn right" in detected_text:
                            self.speak("Turning right")
                            print("Action: Turning right")
                        elif "turn left" in detected_text:
                            self.speak("Turning left")
                            print("Action: Turning left")
                        elif "stop" in detected_text:
                            self.speak("Stopping")
                            print("Action: Stopping")
                        elif "go forward" in detected_text:
                            self.speak("Moving forward")
                            print("Action: Moving forward")
                        elif "go backward" in detected_text:
                            self.speak("Reversing")
                            print("Action: Reversing")
                        elif "rotate" in detected_text:
                            self.speak("Rotating")
                            print("Action: Rotating")
                        elif "slow down" in detected_text:
                            self.speak("Slowing down")
                            print("Action: Slowing down")
                        elif "exit" in detected_text:
                            self.speak("Goodbye")
                            print("Exiting program. Goodbye!")
                            self.terminate_event.set()
                            break
                        else:
                            self.speak(f"I heard: {detected_text}")
                            print(f"No matching command for: {detected_text}")

                    else:
                        print("No face detected. Waiting...")
                        time.sleep(1)
                except sr.UnknownValueError:
                    print("I didn't catch that. Please try again.")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")
                    self.terminate_event.set()
                    break
                except sr.WaitTimeoutError:
                    print("No speech detected. Continuing...")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

    def run(self):
        """Run the face detection and speech recognition processes."""
        face_thread = threading.Thread(target=self.detect_face)
        speech_thread = threading.Thread(target=self.listen_for_commands)

        face_thread.start()
        speech_thread.start()

        face_thread.join()
        speech_thread.join()

        print("Program has terminated.")


if __name__ == "__main__":
    control_system = FaceAndVoiceControl()
    try:
        control_system.run()
    except KeyboardInterrupt:
        print("Interrupt received. Cleaning up...")
        control_system.terminate_event.set()
