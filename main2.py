import tkinter as tk
from tkinter import filedialog, Label, Button, Scrollbar, Canvas, Frame
from PIL import Image, ImageTk
from emotion_recognition import predict_emotion
from dass21 import dass21_score
from emoji_calculation import calculate_emojis_scores
from normalised_score_cal import calculate_normalised_score

class EmotionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Recognition & Mental Health Assessment")
        
        self.dass_result = {}  # Stores DASS-21 scores as a dictionary
        self.emoji_result = {}  # Stores Emoji-based scores as a dictionary

        # === IMAGE UPLOAD SECTION ===
        self.label = Label(root, text="Upload an Image for Emotion Detection", font=("Arial", 14))
        self.label.pack(pady=10)

        self.upload_button = Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.image_label = Label(root)
        self.image_label.pack(pady=5)

        self.result_label = Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.dass_button = Button(root, text="Take DASS-21 Test", command=self.start_dass_test, state=tk.DISABLED)
        self.dass_button.pack(pady=5)

        self.dass_result_label = Label(root, text="", font=("Arial", 12))
        self.dass_result_label.pack(pady=10)

        self.emoji_result_label = Label(root, text="", font=("Arial", 12))
        self.emoji_result_label.pack(pady=10)


        # === EMOJI SELECTION SECTION ===
        self.emoji_phase = 0  # Track current phase
        self.selected_emojis = []  # Store selected emojis
        self.emoji_button = Button(root, text="Proceed to Emoji Selection", command=self.start_emoji_selection, state=tk.DISABLED)
        self.emoji_button.pack(pady=5)

        # === NORMALIZED SCORE SECTION ===
        self.normalized_score_button = Button(root, text="Show Normalized Score", command=self.show_normalized_score, state=tk.DISABLED)
        self.normalized_score_button.pack(pady=5)

        self.normalized_score_label = Label(root, text="", font=("Arial", 14))
        self.normalized_score_label.pack(pady=10)
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((150, 150))
            img = ImageTk.PhotoImage(img)

            self.image_label.config(image=img)
            self.image_label.image = img

            try:
                predicted_emotion = predict_emotion(file_path)
                self.result_label.config(text=f"Predicted Emotion: {predicted_emotion}")
                self.dass_button.config(state=tk.NORMAL)
            except Exception as e:
                self.result_label.config(text="Error: Could not classify image")
                print(f"Error: {e}")

    def start_dass_test(self):
        self.dass_window = tk.Toplevel(self.root)
        self.dass_window.title("DASS-21 Test")

        # === SCROLLABLE FRAME SETUP ===
        canvas = Canvas(self.dass_window)
        scrollbar = Scrollbar(self.dass_window, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.responses = []
        self.questions = [
            "I found it hard to wind down.", "I was aware of dryness of my mouth.",
            "I couldn't seem to experience any positive feeling.", "I experienced breathing difficulty.",
            "I found it difficult to work up the initiative.", "I tended to over-react to situations.",
            "I experienced trembling (e.g. in hands).", "I felt that I was using a lot of nervous energy.",
            "I was worried about situations in which I might panic.","I felt that I had nothing to look forward to", 
            "I found myself getting agitated.","I found it difficult to relax.",
            "I felt down-hearted and blue.", "I was intolerant of anything that kept me from getting on with things.",
            "I felt I was close to panic.","I was unable to become enthusiastic about anything.",
            "I felt I wasn’t worth much as a person.",
            "I felt that I was rather touchy.", 
            "I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat)", 
            "I felt scared without any good reason","I felt that life was meaningless."
            
        ]

        for i, question in enumerate(self.questions):
            label = Label(scrollable_frame, text=question, font=("Arial", 12))
            label.pack()

            response = tk.IntVar(value=0)
            self.responses.append(response)

            for j in range(4):
                radio = tk.Radiobutton(scrollable_frame, text=str(j), variable=response, value=j)
                radio.pack()

        submit_button = Button(scrollable_frame, text="Submit", command=self.calculate_dass_scores)
        submit_button.pack(pady=10)

    def calculate_dass_scores(self):
        scores = [response.get() for response in self.responses]
        result = dass21_score(scores)
        print("Raw DASS-21 Output (Before Fixing Keys):", result)  # Debugging

        # Convert keys to lowercase
        fixed_result = {k.lower(): v for k, v in result.items()}
        print("Fixed DASS-21 Output (Corrected Keys):", fixed_result)# Debugging
        print("Data Types:", {k: type(v) for k, v in fixed_result.items()})  # Ensure integer values

        self.process_dass_scores(result)
        self.dass_result_label.config(text=f"DASS-21 Result: {result}")
        self.emoji_button.config(state=tk.NORMAL)
        self.dass_window.destroy()

    def start_emoji_selection(self):
        self.emoji_window = tk.Toplevel(self.root)
        self.emoji_window.title("Emoji Selection Phase 1")

        self.emoji_options = [
            ["😎", "😭", "😖", "😁", "😞", "😨", "🙂", "🤬", "😡", "😰", "💢", "😢"],
            ["😇 ", "😱", "💔", "😓", "😔", "😄", "😵", "😊", "🤯", "🥀", "😤", "🫣"],
            ["😧", "😬", "🤗", "😆", "😠", "😩", "🖤", "😶", "🤦", "🏃💨", "😏", "😩"]
        ]


        self.create_emoji_selection()
        
    def create_emoji_selection(self):
        # Clear the existing window content
        for  widget in self.emoji_window.winfo_children():
            widget.destroy()

        Label(self.emoji_window, text=f"Select 4 Emojis (Phase {self.emoji_phase + 1}/3)", font=("Arial", 14)).pack(pady=10)

        self.selected_phase_emojis = []

        def select_emoji(emoji, button):
            if emoji in self.selected_phase_emojis:
                self.selected_phase_emojis.remove(emoji)
                button.config(relief="raised")
            elif len(self.selected_phase_emojis) < 4:
                self.selected_phase_emojis.append(emoji)
                button.config(relief="sunken")

        button_list = []  # Store button references

        for emoji in self.emoji_options[self.emoji_phase]:
            btn = Button(self.emoji_window, text=emoji, font=("Arial", 20))
            btn.config(command=lambda e=emoji, b=btn: select_emoji(e, b))
            btn.pack(side="left", padx=5, pady=5)
            button_list.append(btn)  # Save button reference

        submit_btn = Button(self.emoji_window, text="Next", command=self.next_emoji_phase)
        submit_btn.pack(pady=10)


    def next_emoji_phase(self):
        if len(self.selected_phase_emojis) != 4:
            return  # Ensure exactly 4 emojis are selected

        self.selected_emojis.extend(self.selected_phase_emojis)

        if self.emoji_phase < 2:
            self.emoji_phase += 1
            self.create_emoji_selection()
        else:
            self.emoji_window.destroy()
            self.display_emoji_results()
            print("Final Selected Emojis:", self.selected_emojis)
                    
        
    def display_emoji_results(self):
        # Calculate scores using the correct function
        emoji_counts = calculate_emojis_scores(self.selected_emojis)
        print("Raw Emoji Analysis Output:", emoji_counts)  # Debug
        self.process_emoji_scores(emoji_counts)
        # Update the result label below the emoji buttons
        result_text = (
            f"Emoji Analysis Result:\n"
            f"Stress: {emoji_counts['stress']} emojis\n"
            f"Anxiety: {emoji_counts['anxiety']} emojis\n"
            f"Depression: {emoji_counts['depression']} emojis\n"
            # f"normal: {emoji_counts['normal']} emojis"
            
        )

            
        self.emoji_result_label.config(text=result_text)
        self.emoji_result_label.pack_forget()  # Remove from current position
        self.emoji_result_label.pack(pady=10, after=self.emoji_button)

        self.normalized_score_button.config(state=tk.NORMAL)
        self.emoji_window.destroy()
        
        
    # def process_dass_scores(self, dass_scores):
    #     """Process and store DASS-21 scores as a dictionary."""
    #     if isinstance(dass_scores, dict) and all(k in dass_scores for k in ["stress", "anxiety", "depression"]):
    #         self.dass_result = dass_scores  # Store as dictionary ✅
    #     else:
    #         print("Error: Invalid DASS scores format")
            
            
            
    def process_dass_scores(self, scores):
        print("Received scores for processing:", scores)  # Debugging

        # Convert keys to lowercase
        scores = {key.lower(): value for key, value in scores.items()}
        print("Fixed DASS-21 Output (Corrected Keys):", scores)

        # Check if all required keys exist
        required_keys = {"depression", "anxiety", "stress"}
        if not required_keys.issubset(scores.keys()):
            print(f"Error: Missing required keys. Found: {scores.keys()}, Expected: {required_keys}")
            return
    
        # Validate that all values are integers
        for key, value in scores.items():
            if not isinstance(value, int):
                print(f"Error: DASS value for {key} is not an integer. Got: {value} (type: {type(value)})")
                return
    
        # Store the validated scores
        self.dass_result = scores
        print("DASS scores successfully stored:", self.dass_result)


    def process_emoji_scores(self, emoji_scores):
        """Process and store emoji-based scores as a dictionary."""
        print("Received emoji scores for processing:", emoji_scores)  # Debugging
        if isinstance(emoji_scores, dict) and all(k in emoji_scores for k in ["stress", "anxiety", "depression"]):
            self.emoji_result = emoji_scores  # Store as dictionary ✅
            print("Emoji scores successfully stored:", self.emoji_result)
        else:
            print("Error: Invalid Emoji scores format")
            
    

    # def classify_severity(score, category):
            
    #     if category == "depression":
    #         if score <= 0.21:
    #             return "Normal"
    #         elif score <= 0.31:
    #             return "Mild"
    #         elif score <= 0.48:
    #             return "Moderate"
    #         elif score <= 0.64:
    #             return "Severe"
    #         else:
    #             return "Extremely Severe"

    #     elif category == "anxiety":
    #         if score <= 0.18:
    #             return "Normal"
    #         elif score <= 0.21:
    #             return "Mild"
    #         elif score <= 0.33:
    #             return "Moderate"
    #         elif score <= 0.44:
    #             return "Severe"
    #         else:
    #             return "Extremely Severe"

    #     elif category == "stress":
    #         if score <= 0.33:
    #             return "Normal"
    #         elif score <= 0.42:
    #             return "Mild"
    #         elif score <= 0.59:
    #             return "Moderate"
    #         elif score <= 0.78:
    #             return "Severe"
    #         else:
    #             return "Extremely Severe"
            
    def show_normalized_score(self):
        def classify_severity(score, category):
            
            if category == "depression":
                if score <= 0.21:
                    return "Normal"
                elif score <= 0.31:
                    return "Mild"
                elif score <= 0.48:
                    return "Moderate"
                elif score <= 0.64:
                    return "Severe"
                else:
                    return "Extremely Severe"

            elif category == "anxiety":
                if score <= 0.18:
                    return "Normal"
                elif score <= 0.21:
                    return "Mild"
                elif score <= 0.33:
                    return "Moderate"
                elif score <= 0.44:
                    return "Severe"
                else:
                    return "Extremely Severe"

            elif category == "stress":
                if score <= 0.33:
                    return "Normal"
                elif score <= 0.42:
                    return "Mild"
                elif score <= 0.59:
                    return "Moderate"
                elif score <= 0.78:
                    return "Severe"
                else:
                    return "Extremely Severe"
        try:
            if self.dass_result and self.emoji_result:
                normalized = calculate_normalised_score(self.dass_result, self.emoji_result)
                normalized = {key: round(value, 2) for key, value in normalized.items()}

                print("Normalized Score Output:", normalized)  # Debug

                depression_level = classify_severity(normalized["depression"], "depression")
                anxiety_level = classify_severity(normalized["anxiety"], "anxiety")
                stress_level = classify_severity(normalized["stress"], "stress")

                result_text = (
                    f"Normalized Emotion Severity:\n"
                    f"Depression Score: {normalized['depression']:.2f} ({depression_level})\n"
                    f"Anxiety Score: {normalized['anxiety']:.2f} ({anxiety_level})\n"
                    f"Stress Score: {normalized['stress']:.2f} ({stress_level})"
                )
                self.normalized_score_label.config(text=result_text)
            else:
                self.normalized_score_label.config(text="Error: Missing DASS or Emoji results.")

        except Exception as e:
            self.normalized_score_label.config(text="Error while computing normalized score.")
            print("Error:", e)


    # def show_normalized_score(self):
    #     dass_score = self.dass_result # Ensure this stores DASS-21 scores as a dictionary
    #     emoji_score = self.emoji_result  # Ensure this stores emoji scores as a dictionary

    #     print("DASS Score:", dass_score)  # Debugging output
    #     print("Emoji Score:", emoji_score)  # Debugging output


    #     if not dass_score or not emoji_score:
    #         self.normalized_score_label.config(text="Error: Missing scores.")
    #         return
        
    #     # Get the individual normalized scores
    #     normalized_scores = calculate_normalised_score(dass_score, emoji_score)
    #     normalized_scores = {key: round(value, 2) for key, value in normalized_scores.items()}
        
    #     stress_severity = classify_severity(normalized_scores['stress'])
    #     anxiety_severity = classify_severity(normalized_scores['anxiety'])
    #     depression_severity = classify_severity(normalized_scores['depression'])
        


        
        # Display the individual scores for Stress, Anxiety, and Depression
        # result_text = (
        #     f"Normalized Scores:\n"
        #     f"Stress: {normalized_scores['stress']}\n"
        #     f"Anxiety: {normalized_scores['anxiety']}\n"
        #     f"Depression: {normalized_scores['depression']}"
        # )
        # result_text = (
        #     f"Normalized Scores and Severity:\n"
        #     f"Stress: {normalized_scores['stress']:.2f} - {stress_severity}\n"
        #     f"Anxiety: {normalized_scores['anxiety']:.2f} - {anxiety_severity}\n"
        #     f"Depression: {normalized_scores['depression']:.2f} - {depression_severity}"
        # )

        # self.normalized_score_label.config(text=result_text)

        
root = tk.Tk()
app = EmotionGUI(root)
root.mainloop()