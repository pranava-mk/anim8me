import os
from django.shortcuts import render
from django.http import FileResponse, StreamingHttpResponse
import cv2
import mediapipe as mp
import numpy as np


landmark_data = []  # Global list to store landmarks data


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def home(request):
    return render(request, 'index.html')

def webcam_view(request):
    return render(request, 'webcam.html')

def pose_estimation(request):
    def generate_frames():
        # cap = cv2.VideoCapture(0)  # Open the webcam (assuming it's the default camera, change if needed)
        cap = cv2.VideoCapture('/home/cruxx/repos/anim8me/anim8me/mainapp/video.mp4')
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

                # Append the pose landmarks data to the list
                # if results.pose_landmarks:
                    # landmark_data.append(results.pose_landmarks)
                    
                if results.pose_landmarks:
                # Convert the NormalizedLandmarkList to a list of dictionaries
                    landmarks = [
                        {
                            'x': landmark.x,
                            'y': landmark.y,
                            # Add other landmark attributes you need
                        }
                        for landmark in results.pose_landmarks.landmark
                    ]
                    landmark_data.append(landmarks)


                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            

        cap.release()
    response = StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
    return response

def webcam_with_pose(request):
    return render(request, 'webcam_with_pose.html')


def motion_visualization(request):
    return render(request, 'motion_visualization.html')

# def replay_motion(request):
#     # Retrieve landmark_data (e.g., from a database)
#     # Assume landmark_data is a list of lists, where each inner list represents pose landmarks for a frame

#     # Define the output video file
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     out = cv2.VideoWriter('replayed_motion.avi', fourcc, 30.0, (800, 600))  # Adjust the dimensions as needed

#     # Create a black background
#     black_background = np.zeros((600, 800, 3), dtype=np.uint8)

#     # Loop through the recorded landmarks and render them
#     for frame_landmarks in landmark_data:
#         frame = black_background.copy()

#         for landmark in frame_landmarks:
#             x = int(landmark.x * frame.shape[1])
#             y = int(landmark.y * frame.shape[0])

#             cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Draw red circles for landmarks

#         out.write(frame)  # Write the frame to the output video

#     out.release()  # Release the video writer when finished

#     # Return a response with the generated video file for playback
#     video_path = os.path.join(settings.BASE_DIR, 'replayed_motion.avi')
#     return FileResponse(open(video_path, 'rb'), content_type='video/avi')


def replay_motion(request):
    try:
        # Retrieve landmarks data from the request JSON
        landmarks_data_json = json.loads(request.body.decode('utf-8'))
        landmarks_data = landmarks_data_json['landmarks']

        if not landmarks_data:
            return HttpResponseServerError("No landmarks data provided.")

        # Define the output video file
        video_path = os.path.join(settings.MEDIA_ROOT, 'replayed_motion.avi')
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_path, fourcc, 30.0, (800, 600))  # Adjust the dimensions as needed

        # Create a black background
        black_background = np.zeros((600, 800, 3), dtype=np.uint8)

        # Loop through the recorded landmarks and render them
        for frame_landmarks in landmarks_data:
            frame = black_background.copy()

            for landmark in frame_landmarks:
                x = int(landmark['x'] * frame.shape[1])
                y = int(landmark['y'] * frame.shape[0])

                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Draw red circles for landmarks

            out.write(frame)  # Write the frame to the output video

        out.release()  # Release the video writer when finished

        # Return the path to the generated video file for download
        return JsonResponse({'video_path': video_path})
    except Exception as e:
        return HttpResponseServerError(f"Error: {str(e)}")