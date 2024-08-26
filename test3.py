import cv2
from pyzbar.pyzbar import decode
import os
import subprocess
import platform
import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox, Frame, Toplevel, colorchooser, simpledialog
from PIL import Image, ImageTk
import qrcode

class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#2E2E2E")  # Dark background

        # สร้างกรอบหลัก
        self.main_frame = Frame(root, bg="#2E2E2E")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # สร้างกรอบวิดีโอ
        self.video_frame = Frame(self.main_frame, bg="#1C1C1C", bd=2, relief=tk.RAISED)
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        self.video_label = Label(self.video_frame, bg="#1C1C1C")
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # สร้างกรอบปุ่ม
        self.button_frame = Frame(self.main_frame, bg="#2E2E2E")
        self.button_frame.pack(pady=20, anchor=tk.CENTER)

        # ใช้ grid() เพื่อจัดเรียงปุ่ม
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)

        # ปุ่มการสแกน
        self.start_button = Button(self.button_frame, text="Start Scanning", command=self.start_scanning, font=("Segoe UI", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.start_button.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W+tk.E)

        self.stop_button = Button(self.button_frame, text="Stop Scanning", command=self.stop_scanning, state=tk.DISABLED, font=("Segoe UI", 12), bg="#F44336", fg="white", padx=10, pady=5)
        self.stop_button.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        # ปุ่มสำหรับการสร้าง QR Code
        self.generate_button = Button(self.button_frame, text="Generate QR Code", command=self.generate_qr_code, font=("Segoe UI", 12), bg="#2196F3", fg="white", padx=10, pady=5)
        self.generate_button.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W+tk.E)

        self.qr_color_button = Button(self.button_frame, text="Choose QR Code Color", command=self.choose_qr_color, font=("Segoe UI", 12), bg="#9C27B0", fg="white", padx=10, pady=5)
        self.qr_color_button.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        self.text_qr_button = Button(self.button_frame, text="Generate QR from Text", command=self.generate_qr_from_text, font=("Segoe UI", 12), bg="#FF5722", fg="white", padx=10, pady=5)
        self.text_qr_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W+tk.E)

        # เพิ่มปุ่มออก
        self.exit_button = Button(self.button_frame, text="Exit", command=self.root.quit, font=("Segoe UI", 12), bg="#B71C1C", fg="white", padx=10, pady=5)
        self.exit_button.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W+tk.E)

        self.cap = None
        self.running = False
        self.qr_color = "black"
        self.qr_code_data = []

    def play_video(self, video_path):
        system_name = platform.system()

        if system_name == "Linux":  # สำหรับ Linux หรือ Raspberry Pi
            subprocess.run(["mpv", video_path])
        elif system_name == "Darwin":  # สำหรับ macOS
            subprocess.run(["open", video_path])
        elif system_name == "Windows":  # สำหรับ Windows
            os.startfile(video_path)
        else:
            print(f"Unsupported OS: {system_name}")

    def start_scanning(self):
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.qr_code_data = []  # Initialize list to store QR Code data
        self.scan()

    def scan(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print(f"QR Code Data: {data}")

                # เก็บข้อมูล QR Code
                self.qr_code_data.append(data)

                # ดึงวีดีโอจากคลัง
                video_library_path = '/path/to/video/library/'
                video_path = os.path.join(video_library_path, data)

                if os.path.exists(video_path):
                    print(f"Playing video: {video_path}")
                    self.play_video(video_path)
                else:
                    print("Video not found.")

            # แสดงภาพใน GUI
            cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv2_image)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            self.video_label.config(image=tk_image)
            self.video_label.image = tk_image

        self.root.after(10, self.scan)

    def stop_scanning(self):
        self.running = False
        self.cap.release()
        self.video_label.config(image='')
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def generate_qr_code(self):
        video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if video_path:
            video_filename = os.path.basename(video_path)
            qr_data = video_filename

            # เลือกสี QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=self.qr_color, back_color="white")
            img_path = os.path.join('/path/to/save/qr/codes/', f"{video_filename}.png")
            img.save(img_path)

            # แสดง QR code ใน GUI
            pil_image = Image.open(img_path)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.video_label.config(image=tk_image)
            self.video_label.image = tk_image

            messagebox.showinfo("Success", f"QR Code generated and saved as {img_path}")

    def choose_qr_color(self):
        color_code = colorchooser.askcolor(title="Choose QR Code Color")[1]
        if color_code:
            self.qr_color = color_code

    def generate_qr_from_text(self):
        text = simpledialog.askstring("Input", "Enter text to generate QR Code:")
        if text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill_color=self.qr_color, back_color="white")
            img_path = os.path.join('/path/to/save/qr/codes/', f"{text[:10]}.png")
            img.save(img_path)

            # แสดง QR code ใน GUI
            pil_image = Image.open(img_path)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.video_label.config(image=tk_image)
            self.video_label.image = tk_image

            messagebox.showinfo("Success", f"QR Code generated and saved as {img_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeScannerApp(root)
    root.mainloop()
