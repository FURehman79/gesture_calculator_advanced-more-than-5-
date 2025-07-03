# Advanced Gesture Calculator (More Than 5 Fingers)

This project is a **Hand Gesture Based Calculator** that allows users to perform basic arithmetic operations using finger gestures detected via webcam. The calculator can detect **two-hand gestures**, allowing numbers beyond 5 (e.g., 54, 23, 10) by combining both hands.

---

## 🔧 Features

- 👋 Detects hand gestures using **MediaPipe**
- 🧠 Understands operands from **both hands**
- ➕➖✖️➗ Supports operations: `+`, `-`, `*`, `/`
- 🗣️ Speaks out operands, operator, and result using **pyttsx3 TTS**
- 🔁 Reset functionality using `CLEAR` gesture
- ✋ Thanks the user if only one hand is shown (friendly UX)

---

## 📁 Project Structure

```
gesture_calculator_advanced/
├── gesture_calculator.py      # Main runner script
├── hand_utils.py              # Hand detection & landmark extraction
├── finger_counter.py          # Finger counting logic
├── tts_engine.py              # Threaded TTS implementation
└── README.md                  # Project documentation
```

---

## 🖥️ Requirements

Install required packages:

```bash
pip install opencv-python mediapipe pyttsx3
```

---

## ▶️ How It Works

1. **Operand 1:** Show fingers using both hands (e.g., 5 left + 4 right = 54)
2. **Operator:** Show gesture (e.g., thumb up = +, peace sign = -)
3. **Operand 2:** Show fingers again
4. **Result:** Voice announces result and displays it
5. **Reset:** Show all 5 fingers to reset

---

## 🧠 Operator Gestures
| Gesture                | Operator |
| ---------------------- | -------- |
| 👍 Thumb Only          | +        |
| ✌ Peace (Index+Middle) | -        |
| 👆 Thumb+Index       | \*       |
| ☝️ Three Fingers     | /        |
| ✊ All fingers folded     | EVAL     |
| 🖐️ All fingers open       | CLEAR    |

---

## 🙏 Acknowledgment Gesture

If the user shows **only one hand**, the app says **"Thank you"** as a friendly UX touch.

---

## 🧑‍💻 Author

Developed with ❤️ by [FAIZAN UR REHMAN]

---

## 🌐 GitHub Repo

```
https://github.com/FURehman79/gesture_calculator_advanced
```

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---

Feel free to fork, use, and improve this project. Pull requests are welcome!

Happy Coding ✌️

