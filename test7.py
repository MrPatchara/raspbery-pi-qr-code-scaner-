import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
import subprocess
import platform
import tkinter as tk
from tkinter import Label, Button, filedialog, Frame, Toplevel, simpledialog
from PIL import Image, ImageTk
import qrcode

class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner with YOLO")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#2E2E2E")

        # Create main frame
        self.main_frame = Frame(root, bg="#2E2E2E")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create video frame
        self.video_frame = Frame(self.main_frame, bg="#1C1C1C", bd=2, relief=tk.RAISED)
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        self.video_label = Label(self.video_frame, bg="#1C1C1C")
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # Create button frame
        self.button_frame = Frame(self.main_frame, bg="#2E2E2E")
        self.button_frame.pack(pady=20, anchor=tk.CENTER)

        # YOLO Model Files
        self.yolo_net = cv2.dnn.readNet("yolov4.cfg", "yolov4.weights")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes = f.read().strip().split("\n")
        self.layer_names = self.yolo_net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.yolo_net.getUnconnectedOutLayers()]

        # Buttons
        self.start_button = Button(self.button_frame, text="Start Scanning", command=self.start_scanning, font=("Segoe UI", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.start_button.grid(row=0, column=0, padx=10, pady=5)

        self.stop_button = Button(self.button_frame, text="Stop Scanning", command=self.stop_scanning, state=tk.DISABLED, font=("Segoe UI", 12), bg="#F44336", fg="white", padx=10, pady=5)
        self.stop_button.grid(row=0, column=1, padx=10, pady=5)

        self.generate_button = Button(self.button_frame, text="Generate QR Code", command=self.generate_qr_code, font=("Segoe UI", 12), bg="#2196F3", fg="white", padx=10, pady=5)
        self.generate_button.grid(row=0, column=2, padx=10, pady=5)

        self.exit_button = Button(self.button_frame, text="Exit", command=self.root.quit, font=("Segoe UI", 12), bg="#B71C1C", fg="white", padx=10, pady=5)
        self.exit_button.grid(row=0, column=3, padx=10, pady=5)

        self.cap = None
        self.running = False

    def play_video(self, video_path):
        system_name = platform.system()
        if system_name == "Linux":
            subprocess.run(["mpv", video_path])
        elif system_name == "Darwin":
            subprocess.run(["open", video_path])
        elif system_name == "Windows":
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
            # YOLO object detection
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.yolo_net.setInput(blob)
            outs = self.yolo_net.forward(self.output_layers)

            height, width, channels = frame.shape
            boxes = []
            confidences = []
            class_ids = []

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            if len(indices) > 0:
                for i in indices.flatten():
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # QR Code detection
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print(f"QR Code Data: {data}")

                # Retrieve video from library
                video_library_path = '/path/to/video/library/'
                video_path = os.path.join(video_library_path, data)
                if os.path.exists(video_path):
                    print(f"Playing video: {video_path}")
                    self.play_video(video_path)
                else:
                    print("Video not found.")

            # Show image in GUI
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
        text = simpledialog.askstring("Input", "Enter text to generate QR code:")
        if text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                img.save(save_path)
                print(f"QR Code saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeScannerApp(root)
    root.mainloop()
