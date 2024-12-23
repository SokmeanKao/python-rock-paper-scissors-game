import cv2
import random
import mediapipe as mp
import time
import threading
import tkinter as tk

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Global variable to control the webcam
running = True

def detect_hand_choice(image):
    """Detects hand gesture from video feed."""
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the image
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Placeholder: Replace this with actual detection logic based on landmarks
            return "rock"  # You need to implement gesture detection here
    return None

def display_timer(frame, time_left):
    """Displays a countdown timer on the frame."""
    timer_text = f"Time left: {time_left:.1f} seconds"
    cv2.putText(frame, timer_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def display_result(frame, result_text):
    """Displays the result on the frame."""
    cv2.putText(frame, result_text, (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

def play_game():
    """Main game function."""
    # Countdown before starting the game
    for countdown in range(3, 0, -1):
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Display countdown timer on the frame
        cv2.putText(frame, f"Game starts in: {countdown}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imshow("Rock Paper Scissors", frame)
        cv2.waitKey(1000)  # Wait for 1 second

    player_choice = None
    start_time = time.time()
    countdown_duration = 3  # Set countdown duration in seconds

    while player_choice is None and (time.time() - start_time) < countdown_duration:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Calculate time left
        time_left = countdown_duration - (time.time() - start_time)

        # Display timer on the frame
        display_timer(frame, time_left)

        # Detect hand gesture
        player_choice = detect_hand_choice(frame)

        cv2.imshow("Rock Paper Scissors", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    if player_choice is None:
        result_text = "Time's up! You didn't show your hand in time."
    else:
        # Computer choice
        options = ["rock", "paper", "scissors"]
        computer_choice = random.choice(options)

        # Determine winner
        if player_choice == computer_choice:
            result_text = "It's a tie!"
        elif (player_choice == "rock" and computer_choice == "scissors") or \
             (player_choice == "paper" and computer_choice == "rock") or \
             (player_choice == "scissors" and computer_choice == "paper"):
            result_text = "You win!"
        else:
            result_text = "Computer wins!"

    # Show the result on the frame for a while
    for _ in range(30):  # Show result for about 3 seconds
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        display_result(frame, result_text)
        cv2.imshow("Rock Paper Scissors", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def close_window():
    """Function to close the game window."""
    global running
    running = False
    cap.release()
    cv2.destroyAllWindows()
    root.quit()

def run_game():
    """Function to run the game in a separate thread."""
    global running
    while running:
        play_game()

# Initialize video capture
cap = cv2.VideoCapture(0)

# Create a Tkinter window
root = tk.Tk()
root.title("Rock Paper Scissors Game")

# Create a button to close the game
close_button = tk.Button(root, text="Close Game", command=close_window)
close_button.pack(pady=20)

# Start the game in a separate thread
running = True
game_thread = threading.Thread(target=run_game)
game_thread.start()

# Run the Tkinter main loop
root.mainloop()

# Wait for the game thread to finish before exiting
game_thread.join()
