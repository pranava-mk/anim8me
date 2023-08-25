from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import mediapipe as mp

landmark_data = []  # Global list to store landmarks data


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def home(request):
    return render(request, 'index.html')

def webcam_view(request):
    return render(request, 'webcam.html')

# def pose_estimation(request):
#     def generate_frames():
#         cap = cv2.VideoCapture(0) # Open the webcam (assuming it's the default camera, change if needed)
#         # cap = cv2.VideoCapture('video.mp4') 

#         with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#             while True:
#                 success, frame = cap.read()
#                 if not success:
#                     continue

#                 # Perform pose estimation on the frame
#                 image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 results = pose.process(image_rgb)
#                 mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 # Convert the frame to JPEG format
#                 _, buffer = cv2.imencode('.jpg', frame)
#                 frame_bytes = buffer.tobytes()

#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#         cap.release()

#     response = StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
#     return response


def pose_estimation(request):
    def generate_frames():
        # cap = cv2.VideoCapture('/home/cruxx/repos/anim8me/anim8me/mainapp/video.mp4')  # Open a pre-recorded video file
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while True:
                success, frame = cap.read()
                if not success:
                    break

                # Perform pose estimation on the frame
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Convert the frame to JPEG format
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()

    response = StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
    return response




def webcam_with_pose(request):
    return render(request, 'webcam_with_pose.html')
