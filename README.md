import os
import hashlib
import secrets
import base64
import tkinter as tk
from tkinter import ttk
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import time
import pyautogui
import pygetwindow as gw

class SecureOnScreenKeyboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure On-Screen Keyboard")
        self.master.attributes('-topmost', True)

        self.last_activity = time.time()
        self.timeout = 300  # 5 minutes

        self.create_widgets()
        self.create_buttons()
        
        # Generate a key for encryption
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
        # Start checking for inactivity
        self.check_activity()

    def create_widgets(self):
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(self.master, textvariable=self.input_var, show='*')
        self.input_entry.grid(row=0, column=0, columnspan=14, padx=5, pady=5, sticky='ew')

        self.submit_button = ttk.Button(self.master, text="Submit", command=self.submit)
        self.submit_button.grid(row=1, column=0, columnspan=14, padx=5, pady=5, sticky='ew')

    def create_buttons(self):
        keys = [
            ['1','2','3','4','5','6','7','8','9','0','-','=','Backspace'],
            ['q','w','e','r','t','y','u','i','o','p','[',']','\\'],
            ['a','s','d','f','g','h','j','k','l',';',"'"],
            ['z','x','c','v','b','n','m',',','.','/'],
            ['Space']
        ]

        for i, row in enumerate(keys):
            for j, key in enumerate(row):
                if key == 'Space':
                    ttk.Button(self.master, text=key, width=20, command=lambda x=key: self.press(x)).grid(row=i+2, column=0, columnspan=14, pady=2, padx=2, sticky='ew')
                elif key == 'Backspace':
                    ttk.Button(self.master, text=key, width=6, command=lambda x=key: self.press(x)).grid(row=i+2, column=j, pady=2, padx=2, sticky='ew')
                else:
                    ttk.Button(self.master, text=key, width=4, command=lambda x=key: self.press(x)).grid(row=i+2, column=j, pady=2, padx=2)

    def press(self, key):
        self.last_activity = time.time()
        current = self.input_var.get()
        if key == 'Space':
            self.input_var.set(current + ' ')
            pyautogui.press('space')  # Simulate space key press
        elif key == 'Backspace':
            self.input_var.set(current[:-1])
            pyautogui.press('backspace')  # Simulate backspace key press
        else:
            self.input_var.set(current + key)
            pyautogui.press(key)  # Simulate key press

    def submit(self):
        input_text = self.input_var.get()
        hashed_input = self.hash_input(input_text)
        encrypted_input = self.encrypt_input(input_text)
        print(f"Hashed input: {hashed_input}")
        print(f"Encrypted input: {encrypted_input}")
        self.input_var.set('')

        # Find the YouTube window and focus it
        youtube_window = None
        for window in gw.getWindowsWithTitle('YouTube'):
            if 'YouTube' in window.title:
                youtube_window = window
                break

        if youtube_window:
            youtube_window.activate()
            time.sleep(0.5)  # Wait for the window to be focused
            pyautogui.write(input_text)  # Type the input text into the YouTube search bar
            pyautogui.press('enter')  # Press Enter to search

    def hash_input(self, input_text):
        return hashlib.sha256(input_text.encode()).hexdigest()

    def encrypt_input(self, input_text):
        return self.cipher_suite.encrypt(input_text.encode())

    def check_activity(self):
        if time.time() - self.last_activity > self.timeout:
            self.logout()
        else:
            self.master.after(10000, self.check_activity)  # Check every 10 seconds

    def logout(self):
        print("Logging out due to inactivity")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureOnScreenKeyboard(root)
    root.mainloop()
