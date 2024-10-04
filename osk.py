import tkinter as tk
from tkinter import ttk
import win32com.client
import win32gui
import win32con
import time

class OnScreenKeyboard:
    def __init__(self, master):
        self.master = master
        self.master.title("แป้นพิมพ์บนหน้าจอ")
        self.master.attributes('-topmost', True)  # ทำให้หน้าต่างอยู่บนสุดเสมอ
        
        self.shell = win32com.client.Dispatch("WScript.Shell")
        
        self.create_buttons()

    def create_buttons(self):
        keys = [
            ['`','1','2','3','4','5','6','7','8','9','0','-','=','Backspace'],
            ['Tab','q','w','e','r','t','y','u','i','o','p','[',']','\\'],
            ['Caps','a','s','d','f','g','h','j','k','l',';',"'",'Enter'],
            ['Shift','z','x','c','v','b','n','m',',','.','/','Shift'],
            ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Fn', 'Ctrl']
        ]
        
        for i, row in enumerate(keys):
            for j, key in enumerate(row):
                if key == 'Space':
                    ttk.Button(self.master, text=key, width=20, command=lambda x=key: self.press(x)).grid(row=i, column=j, columnspan=4, pady=2, padx=2, sticky='ew')
                elif key in ('Backspace', 'Tab', 'Caps', 'Shift', 'Enter', 'Ctrl', 'Win', 'Alt', 'Fn'):
                    ttk.Button(self.master, text=key, width=6, command=lambda x=key: self.press(x)).grid(row=i, column=j, pady=2, padx=2, sticky='ew')
                else:
                    ttk.Button(self.master, text=key, width=4, command=lambda x=key: self.press(x)).grid(row=i, column=j, pady=2, padx=2)

    def press(self, key):
        # บันทึกหน้าต่างปัจจุบัน
        current_window = win32gui.GetForegroundWindow()
        
        # ซ่อนแป้นพิมพ์บนหน้าจอชั่วคราว
        self.master.withdraw()
        
        # รอให้แน่ใจว่าแป้นพิมพ์ถูกซ่อน
        time.sleep(0.1)
        
        # ส่งคีย์ไปยังแอปพลิเคชันที่เปิดอยู่ล่าสุด
        if key == 'Space':
            self.shell.SendKeys(' ')
        elif key == 'Backspace':
            self.shell.SendKeys('{BACKSPACE}')
        elif key in ('Tab', 'Enter', 'Ctrl', 'Win', 'Alt', 'Fn'):
            self.shell.SendKeys(f'{{{key.upper()}}}')
        elif key == 'Caps':
            self.shell.SendKeys('{CAPSLOCK}')
        elif key == 'Shift':
            self.shell.SendKeys('+')
        else:
            self.shell.SendKeys(key)
        
        # แสดงแป้นพิมพ์บนหน้าจออีกครั้ง
        self.master.deiconify()
        
        # นำโฟกัสกลับไปยังหน้าต่างเดิม
        win32gui.SetForegroundWindow(current_window)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        osk = OnScreenKeyboard(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("โปรแกรมถูกขัดจังหวะ")
        