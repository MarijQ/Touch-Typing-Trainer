# MasterKeys

MasterKeys is a smart typing trainer designed for learning and mastering custom keyboard layouts, developed as part of a personal hobby project. Over the course of three years, this program was iteratively improved to intelligently train one new key at a time using contextually relevant English words and patterns. It enables users to gradually build typing muscle memory while focusing on their unique keyboard layout.

---

## Features

### 1. **Adaptive Typing Trainer**
- Utilizes letter, bigram, and trigram frequency data for intelligent word selection.
- Dynamically adjusts training difficulty based on user performance.
- Supports punctuation, numbers, and capitalization training.

### 2. **Dynamic Performance Feedback**
- Tracks and visualizes real-time typing metrics, including Words Per Minute (WPM) and accuracy.
- Highlights errors and provides constructive feedback for improvement.
- Displays historical progress with performance graphs.

### 3. **Customizable Key Training**
- Fully customizable to any keyboard layout or language pattern.
- Allows selective focus on specific keys, symbols, or word combinations.

### 4. **Built-in GUI**
- User-friendly interface built with Python’s `tkinter`.
- Live text display for typing and score metrics.
- Toggle between graphs, key art, and text.

---

## Background and Context

As part of this project, I built and customized a **Hillside52 split keyboard**, featuring Bluetooth connectivity and powered by Nice!Nano controllers. The journey involved sourcing components, soldering, flashing firmware, and designing a tailored keymap optimized for productivity.

MasterKeys was developed to complement the keyboard, ensuring a targeted and efficient way to learn the new layout and improve typing efficiency.

---

## Installation

1. **Clone This Repository**:
   ```
   git clone https://github.com/yourusername/MasterKeys.git
   cd MasterKeys
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python SmartTyper.py
   ```

---

## Usage

1. Launch the app and input your custom key patterns (letters, symbols, etc.) into the GUI fields.
2. Begin typing the randomly generated text shown in the typing area.
3. Monitor live WPM and accuracy feedback, while focusing on mastering one key or combination at a time.
4. Reference the plotted performance graphs to track improvement over time.

*(Optional)* Replace `data2_10kcut.csv, monogram.csv, bigram2.csv, trigram2.csv` with personalized datasets to train on custom word lists or frequencies.

---

## Screenshots

### Main Typing Trainer
![Screenshot](XX.png)

---

## Future Improvements
- Integrate with cloud-based result storage for long-term analysis.
- Expand to support multi-language layouts.
- Provide additional customization options for keymap variations.

---

## Technologies Used
- **Python**: Core implementation, data processing, and logic.
- **tkinter**: GUI framework.
- **matplotlib**: Graph performance tracking.
- **pynput**: Keyboard input tracking.

---

## Author
Marij Qureshi  
[LinkedIn](https://www.linkedin.com/in/marijqureshi/) | [Email](mailto:marij.qureshi@outlook.com)

---

**Disclaimer**: This project was developed as a personal learning tool and is provided as-is.
