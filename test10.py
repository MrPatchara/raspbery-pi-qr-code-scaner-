import cv2
from pyzbar.pyzbar import decode
import os
import subprocess
import platform
import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox, Frame, Toplevel, colorchooser, simpledialog, PhotoImage
from PIL import Image, ImageTk
import qrcode
import numpy as np
import webbrowser



class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI & QR Code Scanner by Mr.Patchara Al-umaree : 6651630177 ")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.root.iconphoto(False, PhotoImage(file=r'data\pic\icon.png'))  # Set the app icon

        # Create the menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Add "Contact Developer" menu
        developer_menu = tk.Menu(menubar, tearoff=0)
        developer_menu.add_command(label="Contact Developer", command=self.show_developer_info)
        menubar.add_cascade(label="Help!", menu=developer_menu)

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
        self.yolo_net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes = f.read().strip().split("\n")
        self.layer_names = self.yolo_net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.yolo_net.getUnconnectedOutLayers()]


        # Use grid() to align buttons
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)

        # Scan buttons
        self.start_button = Button(self.button_frame, text="Start Scanning", command=self.start_scanning, font=("Segoe UI", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.start_button.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W+tk.E)

        self.stop_button = Button(self.button_frame, text="Stop Scanning", command=self.stop_scanning, state=tk.DISABLED, font=("Segoe UI", 12), bg="#F44336", fg="white", padx=10, pady=5)
        self.stop_button.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        # QR Code buttons
        self.generate_button = Button(self.button_frame, text="Generate QR Code", command=self.show_qr_code_options, font=("Segoe UI", 12), bg="#2196F3", fg="white", padx=10, pady=5)
        self.generate_button.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W+tk.E)

        self.qr_color_button = Button(self.button_frame, text="Choose QR Code Color", command=self.choose_qr_color, font=("Segoe UI", 12), bg="#9C27B0", fg="white", padx=10, pady=5)
        self.qr_color_button.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        # Exit button
        self.exit_button = Button(self.button_frame, text="Exit", command=self.root.quit, font=("Segoe UI", 12), bg="#B71C1C", fg="white", padx=10, pady=5)
        self.exit_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W+tk.E)

        self.cap = None
        self.running = False
        self.qr_color = "black"
        self.qr_code_data = []

        # Load Haar Cascade Classifier for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.object_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')  # Example for object detection

    def show_developer_info(self):
        # Create a new window for developer information
        developer_window = Toplevel(self.root)
        developer_window.title("Developer Information")
        developer_window.geometry("250x350")  # Set a smaller size for the window
        developer_window.configure(bg="#2E2E2E")  # Dark background

        # Developer information
        dev_name = "Patchara Al-umaree"
        dev_email = "Patcharaalumaree@gmail.com"
        dev_student_id = "6651630177"
        dev_github = "https://github.com/MrPatchara"  
        dev_photo_path = r'data\pic\pic.png'  # Replace with the path to your photo
        developer_window.iconphoto(False, PhotoImage(file=dev_photo_path))# Set the developer photo as the window icon


        # Display developer photo
        photo = PhotoImage(file=dev_photo_path)
        photo = photo.subsample(3, 3)  # Resize the image (subsample reduces the size)
        photo_label = Label(developer_window, image=photo)
        photo_label.image = photo  # Keep a reference to the image to prevent garbage collection
        photo_label.pack(pady=10)
        photo_label.config(bg="#2E2E2E")  # Set background color

        # Display developer name
        name_label = Label(developer_window, text=f"Name: {dev_name}", font=("Arial", 10))
        name_label.pack(pady=5)
        name_label.config(bg="#2E2E2E", fg="white")  # Set background and text color

        # Display student ID
        student_id_label = Label(developer_window, text=f"Student ID: {dev_student_id}", font=("Arial", 10))
        student_id_label.pack(pady=5)
        student_id_label.config(bg="#2E2E2E", fg="white")  # Set background and text color

        # Display developer email
        email_label = Label(developer_window, text=f"Email: {dev_email}", font=("Arial", 10))
        email_label.pack(pady=5)
        email_label.config(bg="#2E2E2E", fg="white")  # Set background and text color

        # Display developer GitHub
        github_label = Label(developer_window, text=f"GitHub: {dev_github}", font=("Arial", 10), fg="green", cursor="hand2")
        github_label.pack(pady=5)
        github_label.config(bg="#2E2E2E")  # Set background color

        # Open GitHub link on click
        github_label.bind("<Button-1>", lambda e: webbrowser.open(dev_github))

        # Display grade photo
        grade_photo_path = r'data\pic\mygrade.png'  # Replace with the path to your photo
        grade_photo = PhotoImage(file=grade_photo_path)
        grade_photo = grade_photo.subsample(6, 6)  # Resize the image (subsample reduces the size)
        grade_photo_label = Label(developer_window, image=grade_photo)
        grade_photo_label.image = grade_photo
        grade_photo_label.pack(pady=10) # Add some space between the labels
        grade_photo_label.config(bg="#2E2E2E")  # Set background color

    def play_video(self, video_path):
        system_name = platform.system()

        if system_name == "Linux":  # For Linux or Raspberry Pi
            subprocess.run(["mpv", video_path])
        elif system_name == "Darwin":  # For macOS
            subprocess.run(["open", video_path])
        elif system_name == "Windows":  # For Windows
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
            # YOLOv4-tiny object detection
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
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

                # Check if data is a URL
                if data.startswith('http://') or data.startswith('https://'):
                    print(f"URL detected: {data}")
                    # Open URL in default web browser
                    webbrowser.open(data)

                # Check if data is a vCard
                elif data.startswith('BEGIN:VCARD'):
                    print("vCard detected")
                    vcard_path = os.path.join('data', 'vcard.vcf')
                    with open(vcard_path, 'w') as vcard_file:
                        vcard_file.write(data)
                    print(f"vCard saved to {vcard_path}")
                    # Optional: You could open the vCard file or process it further

                else:
                    # Assume the data is plain text and show a popup
                    print(f"Text detected: {data}")
                    messagebox.showinfo("QR Code Text", data)

                    # Retrieve video from library based on QR code data
                    video_library_path = r'data\video'
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

        # Call scan again after 10 ms
        self.root.after(10, self.scan)


    def stop_scanning(self):
        self.running = False
        self.cap.release()
        self.video_label.config(image='')
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def show_qr_code_options(self):
        self.qr_option_window = Toplevel(self.root)
        self.qr_option_window.title("QR Code Options")
        self.qr_option_window.geometry("300x250")
        self.qr_option_window.configure(bg="#2E2E2E")

        # Buttons for different QR Code generation
        Button(self.qr_option_window, text="Generate QR Code from Video", command=self.generate_qr_code_from_video, font=("Segoe UI", 12), bg="#2196F3", fg="white", padx=10, pady=5).pack(pady=10)
        Button(self.qr_option_window, text="Generate QR Code from URL", command=self.generate_qr_code_from_url, font=("Segoe UI", 12), bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)
        Button(self.qr_option_window, text="Generate QR Code from vCard", command=self.generate_qr_code_from_vcard, font=("Segoe UI", 12), bg="#9C27B0", fg="white", padx=10, pady=5).pack(pady=10)
        Button(self.qr_option_window, text="Generate QR Code from Text", command=self.generate_qr_from_text, font=("Segoe UI", 12), bg="#FF5722", fg="white", padx=10, pady=5).pack(pady=10)

    def generate_qr_code_from_video(self):
        video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if video_path:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(video_path)
            qr.make(fit=True)
            img = qr.make_image(fill_color=self.qr_color, back_color="white")
            img_path = os.path.join(r'data\save', f"{os.path.basename(video_path)}.png")
            img.save(img_path)

            pil_img = Image.open(img_path)
            pil_img.show()

    def generate_qr_code_from_url(self):
        url = simpledialog.askstring("Input", "Enter URL:")
        if url:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color=self.qr_color, back_color="white")
            img_path = os.path.join(r'data\save', "url_qr_code.png")
            img.save(img_path)

            pil_img = Image.open(img_path)
            pil_img.show()

    def generate_qr_code_from_vcard(self):
        name = simpledialog.askstring("Input", "Enter Name:")
        phone = simpledialog.askstring("Input", "Enter Phone Number:")
        email = simpledialog.askstring("Input", "Enter Email Address:")
        vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(vcard_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.qr_color, back_color="white")
        img_path = os.path.join(r'data\save', "vcard_qr_code.png")
        img.save(img_path)

        pil_img = Image.open(img_path)
        pil_img.show()

    def generate_qr_from_text(self):
        text = simpledialog.askstring("Input", "Enter Text:")
        if text:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color=self.qr_color, back_color="white")
            img_path = os.path.join(r'data\save', "text_qr_code.png")
            img.save(img_path)

            pil_img = Image.open(img_path)
            pil_img.show()

    def choose_qr_color(self):
        color_code = colorchooser.askcolor(title="Choose QR Code Color")[1]
        if color_code:
            self.qr_color = color_code

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeScannerApp(root)
    root.mainloop()
