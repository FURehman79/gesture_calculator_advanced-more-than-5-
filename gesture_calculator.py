import cv2
import time
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
from tts_engine import speak, voice_queue, tts_thread
from hand_utils import hands, mp_draw, get_number_from_hands, detect_operator
thank_you_spoken = False

cap = cv2.VideoCapture(0)

operand1 = operand2 = operator = result = None
stage = "operand1"
last_change_time = time.time()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        all_lm = results.multi_hand_landmarks
        hand_info = results.multi_handedness

                # Say thank you if only one hand is visible and we're not in an input stage
        if len(all_lm) == 1 and stage == "done" and not thank_you_spoken:
            speak("Thank you")
            thank_you_spoken = True
 # Prevents repeated thank you

        lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in all_lm[0].landmark]
        for handLms in all_lm:
            mp_drawing.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS)

        if time.time() - last_change_time > 3:
            last_change_time = time.time()

            if stage == "operand1":
                operand1 = get_number_from_hands(all_lm, hand_info, w, h)
                speak(f"First number is {operand1}")
                stage = "operator"

            elif stage == "operator":
                op = detect_operator(lm_list)
                if op in ["+", "-", "*", "/"]:
                    operator = op
                    speak(f"Operator is {operator}")
                    stage = "operand2"

            elif stage == "operand2":
                operand2 = get_number_from_hands(all_lm, hand_info, w, h)
                speak(f"Second number is {operand2}")
                stage = "eval"

            elif stage == "eval":
                if operand1 is not None and operand2 is not None and operator is not None:
                    if operator == "+":
                        result = operand1 + operand2
                    elif operator == "-":
                        result = operand1 - operand2
                    elif operator == "*":
                        result = operand1 * operand2
                    elif operator == "/":
                        result = round(operand1 / operand2, 2) if operand2 != 0 else "∞"

                    print(f"Result: {operand1} {operator} {operand2} = {result}")
                    speak(f"The result is {result}")
                    stage = "done"

            elif stage == "done":
                op = detect_operator(lm_list)
                if op == "CLEAR":
                    operand1 = operand2 = operator = result = None
                    stage = "operand1"
                    thank_you_spoken = False
                    print("Calculator reset successfully")
                    speak("Calculator reset successfully")

    cv2.putText(img, f"Stage: {stage}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 255), 2)
    if operand1 is not None:
        cv2.putText(img, f"Operand1: {operand1}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if operator is not None:
        cv2.putText(img, f"Operator: {operator}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if operand2 is not None:
        cv2.putText(img, f"Operand2: {operand2}", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if result is not None:
        cv2.putText(img, f"Result: {result}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Optimized Gesture Calculator", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

voice_queue.put(None)
tts_thread.join()