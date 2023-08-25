from django.shortcuts import render
import cv2
import mediapipe as mp
import pickle
import numpy as np
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles 
mp_pose = mp.solutions.pose




def start_pose_estimation(request):
    cap = cv2.VideoCapture(0)
    pose_landmarks_history = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring: No video in camera frame")
                continue
        
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
            results = pose.process(image)
        
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec = mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
            if results.pose_landmarks is not None:
                pose_landmarks_history.append(results.pose_landmarks)
        
            cv2.imshow('MediaPipe Pose Estimation', cv2.flip(image, 1))
        
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    cap.release()

    # Save pose_landmarks_history using pickle
    with open('pose_landmarks_history.pkl', 'wb') as f:
        pickle.dump(pose_landmarks_history, f)

    return render(request, 'start_pose_estimation.html')





def show_motion(request):
    # Your motion visualization logic goes here
    global pose_landmarks_history
    with open('pose_landmarks_history.pkl', 'rb') as f:
        pose_landmarks_history = pickle.load(f)

    for landmarks in pose_landmarks_history:
        image = np.zeroes((480, 640, 3), dtype=np.uint8)  # Black

        mp_drawing.draw_landmarks(
            image,
            landmarks,
            mp.solutions.pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )

        cv2.imshow('Motion Visualization', cv2.flip(image, 1))

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    return render(request, 'show_motion.html')





def index(request):
    return render(request,'start_pose_estimation.html')