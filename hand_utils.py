import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

def count_fingers_one_hand(lm_list, hand_label):
    count = 0
    if hand_label == "Right":
        if lm_list[5][0] > lm_list[3][0]:
            count += 1
    else:
        if lm_list[5][0] < lm_list[3][0]:
            count += 1
    for tip in finger_tips:
        if lm_list[tip][1] < lm_list[tip - 2][1]:
            count += 1
    return count

def get_number_from_hands(multi_hand_landmarks, multi_handedness, w, h):
    counts = []
    for i, handLms in enumerate(multi_hand_landmarks):
        lm_list = []
        for id, lm in enumerate(handLms.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append((cx, cy))
        hand_label = multi_handedness[i].classification[0].label
        fingers = count_fingers_one_hand(lm_list, hand_label)
        counts.append(fingers)

    if len(counts) == 2:
        return max(counts) * 10 + min(counts)
    elif len(counts) == 1:
        return counts[0]
    else:
        return 0

def detect_operator(lm_list):
    fingers_up = [False] * 5
    fingers_up[0] = lm_list[thumb_tip][0] > lm_list[thumb_tip - 1][0]
    for i, tip in enumerate(finger_tips):
        fingers_up[i+1] = lm_list[tip][1] < lm_list[tip - 2][1]

    if fingers_up == [True, False, False, False, False]:
        return "+"
    elif fingers_up[1] and fingers_up[2] and not fingers_up[0] and not fingers_up[3] and not fingers_up[4]:
        return "-"
    elif fingers_up[0] and fingers_up[1] and not fingers_up[2] and not fingers_up[3] and not fingers_up[4]:
        return "*"
    elif fingers_up[0] and fingers_up[1] and fingers_up[2] and not fingers_up[3] and not fingers_up[4]:
        return "/"
    elif all(f == False for f in fingers_up):
        return "EVAL"
    elif all(f == True for f in fingers_up):
        return "CLEAR"
    else:
        return None