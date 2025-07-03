# finger_counter.py
finger_tips = [8, 12, 16, 20]

def count_fingers_one_hand(lm_list, hand_label):
    count = 0
    if hand_label == "Right":
        if lm_list[4][0] > lm_list[3][0]:
            count += 1
    else:
        if lm_list[4][0] < lm_list[3][0]:
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
