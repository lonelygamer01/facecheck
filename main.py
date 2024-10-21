import face_recognition
import os, sys
import tkinter as tk
from tkinter import filedialog
import time
import inquirer
from termcolor import colored
import numpy as np
possible_matches = []
def compare_faces(target_image_path, image_folder, precision):
    global possible_matches
    target_image = face_recognition.load_image_file(target_image_path)
    target_encoding = face_recognition.face_encodings(target_image)[0]
    for image_name in os.listdir(image_folder):
        if image_name.endswith(('.png', '.jpg', '.jpeg')):
            current_image_path = os.path.join(image_folder, image_name)
            current_image = face_recognition.load_image_file(current_image_path)
            current_encodings = face_recognition.face_encodings(current_image)
            if len(current_encodings) == 0:
                print(colored(f"No face detected in {image_name}", "red"))
                time.sleep(0.2)
                continue
            for current_encoding in current_encodings:
                distance = np.linalg.norm(target_encoding - current_encoding)
                print(colored(f"Similarity score with {image_name}: {1 - distance:.2f} (Distance: {distance:.2f})", "red"))
                time.sleep(0.2)
                if distance < precision:
                    possible_matches.append(f"{image_name}, similarity: {1-distance:.2f}")

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Target image")
    if file_path:
        return file_path
    else:
        return None

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a Folder")
    if folder_path:
        return folder_path
    else:
        return None
title = """
   __                                                _ _   _             
  / _|                                              (_) | (_)            
 | |_ __ _  ___ ___   _ __ ___  ___ ___   __ _ _ __  _| |_ _  ___  _ __  
 |  _/ _` |/ __/ _ \ | '__/ _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \ 
 | || (_| | (_|  __/ | | |  __/ (_| (_) | (_| | | | | | |_| | (_) | | | |
 |_| \__,_|\___\___| |_|  \___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
                                          __/ |                          
                                         |___/                           
"""
if __name__ == "__main__":
    time.sleep(1)
    print(colored("Loading face recognition library...","red"))
    time.sleep(0.5)
    print(colored("Loading cv2 library...","red"))
    time.sleep(0.5)
    print(colored("Loading tkinter filepicker library...","red"))
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored(title, "red"))
    select_target = [
        inquirer.List(
            'select_target',
            message="Select target",
            choices=["Select target", "Exit"],
            carousel=False
        ),
    ]
    answer = inquirer.prompt(select_target)
    if answer['select_target'] == "Select target":
        file = select_file()
        if file:
            select_database = [
                inquirer.List(
                    'select_database',
                    message="Select database",
                    choices=["Select database", "Exit"],
                    carousel=False
                ),
            ]
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colored(title, "red"))
            answer = inquirer.prompt(select_database)
            if answer["select_database"] == "Select database":
                folder = select_folder()
                if folder:
                    set_precision = [
                        inquirer.List(
                            'set_precision',
                            message="Set precision",
                            choices=["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "Exit"],
                            carousel=False
                        ),
                    ]
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(colored(title, "red"))
                    answer = inquirer.prompt(set_precision)
                    if answer["set_precision"] == "Exit":
                        sys.exit()
                    else:
                        print_file = file
                        print_folder = folder
                        print_precision = float(answer["set_precision"])
                        print(colored(f"Target file: '{print_file}'\ndatabase folder: '{print_folder}'\nprecission: {print_precision}", "red"))
                        print(colored("Prepairing for comparison...", "red"))
                        time.sleep(1)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        compare_faces(print_file, print_folder, print_precision)
                        if possible_matches == []:
                            print(colored("No matches found!", "red"))
                        else:
                            print(colored("Matches found!", "red"))
                            for element in possible_matches:
                                print(colored(element, "red"))
            else:
                sys.exit()
    else:
        sys.exit()
    