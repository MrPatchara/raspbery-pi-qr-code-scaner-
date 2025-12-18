# 🔍 AI & QR Code Scanner

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)

**An intelligent QR code scanner with real-time object detection powered by YOLOv4-tiny**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**AI & QR Code Scanner** is a powerful desktop application that combines real-time QR code scanning with advanced object detection capabilities. Built with Python and OpenCV, this application uses YOLOv4-tiny for real-time object detection while simultaneously scanning QR codes from your webcam feed.

Perfect for:
- 🎓 Educational purposes
- 🏢 Interactive displays and kiosks
- 📱 Quick access to multimedia content via QR codes
- 🤖 Raspberry Pi projects
- 🔬 Computer vision research

---

## ✨ Features

### 🔍 **QR Code Scanning**
- ✅ Real-time QR code detection from webcam
- ✅ Automatic URL opening in browser
- ✅ vCard contact information handling
- ✅ Custom text display
- ✅ Video/image playback based on QR code data

### 🎨 **QR Code Generation**
- 📝 Generate QR codes from text
- 🌐 Generate QR codes from URLs
- 📇 Generate QR codes from vCard (contact information)
- 🎬 Generate QR codes from video file paths
- 🎨 Customizable QR code colors

### 🤖 **AI Object Detection**
- 🎯 Real-time object detection using YOLOv4-tiny
- 📦 Detects 80+ object classes (COCO dataset)
- 🎨 Visual bounding boxes and labels
- ⚡ Optimized for performance

### 🖥️ **User Interface**
- 🌙 Modern dark theme
- 🎨 Intuitive and user-friendly design
- 📱 Responsive layout
- 🔧 Easy-to-use controls

### 🌍 **Cross-Platform Support**
- 🪟 Windows
- 🐧 Linux (including Raspberry Pi)
- 🍎 macOS

---

## 📦 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **Webcam**: USB webcam or built-in camera
- **RAM**: Minimum 2GB (4GB recommended)
- **OS**: Windows 10+, Linux (Ubuntu 18.04+), or macOS 10.14+

### Python Dependencies
```
opencv-python >= 4.5.0
pyzbar >= 0.1.8
Pillow >= 8.0.0
qrcode >= 7.0.0
numpy >= 1.19.0
```

### Additional Requirements (Linux/Raspberry Pi)
- `mpv` media player (for video playback)
- `zbar` library:
  ```bash
  sudo apt-get install libzbar0
  ```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MrPatchara/raspbery-pi-qr-code-scaner-.git
cd raspbery-pi-qr-code-scaner-
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python pyzbar Pillow qrcode numpy
```

### 3. Download YOLOv4-tiny Weights

The application requires YOLOv4-tiny model files. Make sure you have:
- `yolov4-tiny.weights`
- `yolov4-tiny.cfg`
- `coco.names`

These files should be in the root directory of the project.

### 4. (Optional) Linux/Raspberry Pi Setup

For Linux systems, install additional dependencies:

```bash
# Install zbar library
sudo apt-get update
sudo apt-get install libzbar0

# Install mpv for video playback
sudo apt-get install mpv
```

---

## 💻 Usage

### Running the Application

#### Windows
```bash
python linuxVersion.py
```

#### Linux/Raspberry Pi
```bash
python3 LinuxVersion/linuxVersion.py
```

### Basic Operations

1. **Start Scanning**
   - Click the "Start Scanning" button
   - Point your webcam at a QR code
   - The application will automatically detect and process QR codes

2. **Stop Scanning**
   - Click the "Stop Scanning" button to stop the camera feed

3. **Generate QR Code**
   - Click "Generate QR Code"
   - Choose from:
     - Text
     - URL
     - vCard (contact information)
     - Video file path
   - Customize the color if desired

4. **View Developer Info**
   - Go to "Help!" → "Contact Developer" in the menu bar

---

## ⚙️ Configuration

### Settings.json

The application uses `settings.json` to map QR code data to files. Edit this file to customize behavior:

```json
{
    "your_qr_code_data": {
        "file_type": "image",
        "path": "data/pic/your_image.png"
    },
    "another_qr_code": {
        "file_type": "video",
        "path": "data/video/your_video.mp4"
    }
}
```

**File Types:**
- `image`: Displays the image in a new window
- `video`: Plays the video using the system's default player

### Directory Structure

```
raspbery-pi-qr-code-scaner-/
├── data/
│   ├── pic/          # Images for display
│   ├── video/        # Videos for playback
│   └── save/         # Generated QR codes
├── yolov4-tiny.weights
├── yolov4-tiny.cfg
├── coco.names
├── settings.json
└── linuxVersion.py
```

---

## 📁 Project Structure

```
raspbery-pi-qr-code-scaner-/
│
├── 📄 linuxVersion.py          # Main application (Linux/Raspberry Pi)
├── 📄 test.py                   # Windows version
├── 📄 update/test.py            # Updated version with settings.json
│
├── 📁 LinuxVersion/             # Linux-specific version
│   └── linuxVersion.py
│
├── 📁 data/                      # Application data
│   ├── pic/                     # Images
│   ├── video/                   # Videos
│   └── save/                    # Generated QR codes
│
├── 📁 build_installer/          # Build scripts and installers
│
├── 📁 Final Version for build/   # Final build versions
│
├── ⚙️ settings.json              # QR code to file mapping
├── ⚙️ yolov4-tiny.weights        # YOLO model weights
├── ⚙️ yolov4-tiny.cfg            # YOLO model configuration
└── 📄 coco.names                 # COCO class names
```

---

## 📸 Screenshots

> *Screenshots coming soon!*

---

## 🛠️ Technologies Used

- **Python 3.8+** - Programming language
- **OpenCV** - Computer vision and image processing
- **YOLOv4-tiny** - Real-time object detection
- **PyZBar** - QR code and barcode decoding
- **Tkinter** - GUI framework
- **Pillow (PIL)** - Image processing
- **QRCode** - QR code generation
- **NumPy** - Numerical computing

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Contact

**Patchara Al-umaree**

- 📧 Email: [Patcharaalumaree@gmail.com](mailto:Patcharaalumaree@gmail.com)
- 🐙 GitHub: [@MrPatchara](https://github.com/MrPatchara)
- 🎓 Student ID: 6651630177

---

## 🙏 Acknowledgments

- YOLOv4-tiny model by [Alexey Bochkovskiy](https://github.com/AlexeyAB)
- COCO dataset for object detection classes
- OpenCV community for excellent computer vision tools
- All contributors and users of this project

---

<div align="center">

**⭐ If you find this project helpful, please consider giving it a star! ⭐**

Made with ❤️ by [Patchara Al-umaree](https://github.com/MrPatchara)

</div>
