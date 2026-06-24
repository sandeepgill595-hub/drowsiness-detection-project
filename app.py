import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import math
import tempfile


# =========================
# Helper Functions
# =========================
def euclidean(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def calculate_ear(landmarks):
    # Left eye landmarks
    p1 = landmarks[33]
    p2 = landmarks[160]
    p3 = landmarks[158]
    p4 = landmarks[133]
    p5 = landmarks[153]
    p6 = landmarks[144]

    vertical1 = euclidean(p2, p6)
    vertical2 = euclidean(p3, p5)
    horizontal = euclidean(p1, p4)

    if horizontal == 0:
        return 0

    ear = (vertical1 + vertical2) / (2 * horizontal)
    return ear

def process_face(frame, face_landmarks):
    h, w, _ = frame.shape

    x_list = []
    y_list = []

    for landmark in face_landmarks.landmark:
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        x_list.append(x)
        y_list.append(y)

    x_min = min(x_list)
    x_max = max(x_list)
    y_min = min(y_list)
    y_max = max(y_list)

    ear = calculate_ear(face_landmarks.landmark)

    return ear, x_min, y_min, x_max, y_max

# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="Drowsiness Detection System")

choice = st.sidebar.selectbox(
    "MY MENU",
    ("HOME", "IMAGE", "VIDEO")
)

st.write(type(mp))
st.write(dir(mp))
st.stop()


# =========================
# HOME
# =========================
if choice == "HOME":
    st.title("AI Drowsiness Detection System")
    st.write("""
    This system detects whether a person is:
    - Awake 🟢
    - Drowsy 🔴

    Supported Modes:
    - IMAGE 
    - VIDEO
    """)


# =========================
# IMAGE
# =========================
elif choice == "IMAGE":
    st.header("Image Detection")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        file_bytes = np.asarray(
            bytearray(uploaded_file.read()),
            dtype=np.uint8
        )

        img = cv2.imdecode(file_bytes, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=10,
            min_detection_confidence=0.5
        ) as face_mesh:

            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    ear, x_min, y_min, x_max, y_max = process_face(img, face_landmarks)

                    if ear < 0.20:
                        status = "Drowsy"
                        color = (0, 0, 255)
                    else:
                        status = "Awake"
                        color = (0, 255, 0)

                    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 3)

                    cv2.putText(
                        img,
                        status,
                        (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2
                    )

                st.success(
                    f"Detected {len(results.multi_face_landmarks)} face(s)"
                )
            else:
                st.warning("No face detected")

        st.image(img, channels="BGR")

# =========================
# VIDEO
# =========================
elif choice == "VIDEO":
    st.header("Video Detection")

    video_file = st.file_uploader(
        "Upload a video",
        type=["mp4", "avi", "mov"]
    )

    replay = st.button("Replay Video")
    frame_window = st.empty()

    if video_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())

        cap = cv2.VideoCapture(tfile.name)
        closed_frames = {}
        drowsy_threshold_frames = 40

        with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=5,
            min_detection_confidence=0.5
        ) as face_mesh:

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb)

                if results.multi_face_landmarks:
                    for i, face_landmarks in enumerate(results.multi_face_landmarks):
                        ear, x_min, y_min, x_max, y_max = process_face(frame, face_landmarks)

                        if i not in closed_frames:
                            closed_frames[i] = 0

                        if ear < 0.20:
                            closed_frames[i] += 1
                        else:
                            closed_frames[i] = 0

                        if closed_frames[i] >= drowsy_threshold_frames:
                            status = "Drowsy"
                            color = (0, 0, 255)
                        else:
                            status = "Awake"
                            color = (0, 255, 0)

                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 3)

                        cv2.putText(
                            frame,
                            status,
                            (x_min, y_min - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            color,
                            2
                        )
                frame_window.image(frame, channels="BGR")

        cap.release()

        if replay:
            st.rerun()


# =========================
# CAMERA
# =========================
# elif choice == "CAMERA":
#     st.header("Live Camera Detection")

#     start = st.button("Start Camera")
#     stop = st.button("Stop Camera")

#     frame_window = st.empty()

#     if start:
#         cap = cv2.VideoCapture(0)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         st.write("Camera FPS:", fps)
#         closed_frames = {}
#         drowsy_threshold_frames = 40

#         with mp_face_mesh.FaceMesh(
#             static_image_mode=False,
#             max_num_faces=5,
#             min_detection_confidence=0.5
#         ) as face_mesh:

#             while cap.isOpened():
#                 if stop:
#                     break

#                 ret, frame = cap.read()

#                 if not ret:
#                     st.error("Camera not accessible")
#                     break

#                 rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 results = face_mesh.process(rgb)

#                 if results.multi_face_landmarks:
#                     for i, face_landmarks in enumerate(results.multi_face_landmarks):
#                         ear, x_min, y_min, x_max, y_max = process_face(frame, face_landmarks)

#                         if i not in closed_frames:
#                             closed_frames[i] = 0

#                         if ear < 0.20:
#                             closed_frames[i] += 1
#                         else:
#                             closed_frames[i] = 0

#                         if closed_frames[i] >= drowsy_threshold_frames:
#                             status = "Drowsy"
#                             color = (0, 0, 255)
#                         else:
#                             status = "Awake"
#                             color = (0, 255, 0)

#                         cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 3)

#                         cv2.putText(
#                             frame,
#                             status,
#                             (x_min, y_min - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.8,
#                             color,
#                             2
#                         )

#                         if closed_frames[i] >= drowsy_threshold_frames:
#                             cv2.putText(
#                                 frame,
#                                 "DROWSINESS ALERT",
#                                 (50, 50),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 1,
#                                 (0, 0, 255),
#                                 3
#                             )
#                 frame_window.image(frame, channels="BGR")

#         cap.release()        