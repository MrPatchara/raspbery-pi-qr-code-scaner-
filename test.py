import cv2
from pyzbar.pyzbar import decode
import os
import subprocess
import platform
import tkinter as tk
from tkinter import Label, Button, filedialog
from PIL import Image, ImageTk
import qrcode

class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.root.geometry("800x600")

        self.video_label = Label(root)
        self.video_label.pack()

        self.start_button = Button(root, text="Start Scanning", command=self.start_scanning)
        self.start_button.pack(pady=20)

        self.stop_button = Button(root, text="Stop Scanning", command=self.stop_scanning, state=tk.DISABLED)
        self.stop_button.pack(pady=20)

        self.generate_button = Button(root, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_button.pack(pady=20)

        self.cap = None
        self.running = False

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

                # ดึงวีดีโอจากคลัง
                video_library_path = ''
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

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img_path = os.path.join('', f"{video_filename}.png")
            img.save(img_path)

            # แสดง QR code ใน GUI
            pil_image = Image.open(img_path)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.video_label.config(image=tk_image)
            self.video_label.image = tk_image

            print(f"QR Code generated and saved as {img_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeScannerApp(root)
    root.mainloop()
