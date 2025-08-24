# ScreenShare Project: Detailed Technical Architecture


<img src="https://img.shields.io/badge/PROJECT%20STATUS-ACTIVE%20BETA-FF8800?style=for-the-badge&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/VERSION-0.5.0-4D4D4D?style=for-the-badge&logo=azurepipelines&logoColor=white"> <img src="https://img.shields.io/badge/PYTHON-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">


# ScreenShare Setup Summary

<img src="https://img.shields.io/badge/-Quick%20Setup-0078D6?style=for-the-badge&logo=windows&logoColor=white"> <img src="https://img.shields.io/badge/-3%20Key%20Steps-FCC624?style=for-the-badge&logo=linux&logoColor=black">

- Simplified Step-by-Step:

    Install Python Packages:

        pip install opencv-python numpy pynput pillow

    Install ADB & Scrcpy:

        Download Android Platform Tools

        Download Scrcpy

        Extract and configure paths in the code

- Enable USB Debugging on Phone:

        Go to: Settings > About Phone

        Tap 7 times on Build Number to enable Developer Options

        Return to: Settings > System > Developer Options

        Enable: USB Debugging and Install via USB

        Connect USB cable and authorize computer when prompted

- Verification Commands:

    # Check if device is recognized
        adb devices

    # Start mirroring
        python main.py

- Tip: Keep USB debugging enabled and cable connected for stable operation!

---

# Core Architecture & Screen Mirroring

<img src="https://img.shields.io/badge/-Scrcpy%20Engine-FFE4E1?style=for-the-badge&logo=android&logoColor=black"> <img src="https://img.shields.io/badge/-H.264%20Encoding-FFE4E1?style=for-the-badge&logo=ffmpeg&logoColor=black"> <img src="https://img.shields.io/badge/-Low%20Latency-FFE4E1?style=for-the-badge&logo=clock&logoColor=black">

---

The application leverages the powerful Scrcpy engine under the hood for efficient screen capture and encoding. The technical pipeline works as follows:

# Simplified core mirroring command

    scrcpy_cmd = [
      self.scrcpy_path,
        '--video-bit-rate', '8M',        # Optimized video quality
        '--max-size', '1280',            # Resolution scaling
        '--max-fps', '60',               # High frame rate support
        '--audio-codec', 'opus',         # Audio streaming
        '--turn-screen-off',             # Device power saving
        '--stay-awake'                   # Prevents sleep mode
      ]

The device screen is captured as a raw H.264 video stream, efficiently encoded in real-time, and transmitted via ADB to the Python client where it's decoded and rendered.
Dual Connectivity Management

---

<img src="https://img.shields.io/badge/-USB%20Debugging-FFE4E1?style=for-the-badge&logo=usb&logoColor=black"> <img src="https://img.shields.io/badge/-WiFi%20ADB-FFE4E1?style=for-the-badge&logo=wifi&logoColor=white"> <img src="https://img.shields.io/badge/-Auto%20Detection-FFE4E1?style=for-the-badge&logo=android&logoColor=black">

---

The connection system automatically detects and manages both USB and WiFi connections through advanced ADB management:

    def check_connections(self):
        """Auto-detects available connections"""
        result = self.adb.run_adb(['devices'])
        lines = result.stdout.strip().split('\n')
    
    for line in lines[1:]:
        if 'device' in line:
            serial = line.split('\t')[0]
            if ':' in serial:  # WiFi connection
                print(f"✅ WiFi: {serial}")
            else:  # USB connection
                print(f"✅ USB: {serial}")

The system prioritizes USB for stability but seamlessly falls back to WiFi when available, using adb tcpip commands for wireless setup.
Advanced Input Control System

---

<img src="https://img.shields.io/badge/-Gesture%20Control-FFE4E1?style=for-the-badge&logo=gesture&logoColor=black"> <img src="https://img.shields.io/badge/-Mouse%20Mapping-FFE4E1?style=for-the-badge&logo=mouse&logoColor=black"> <img src="https://img.shields.io/badge/-Multi%20Threading-FFE4E1?style=for-the-badge&logo=thread&logoColor=black">

---

The input system translates PC mouse actions into native Android gestures through a sophisticated mapping layer:

    def on_click(self, x, y, button, pressed):
        """Converts mouse input to Android commands"""
        device_x, device_y = self.convert_coordinates(x, y)
    
    if button == mouse.Button.left:
        self.send_tap(device_x, device_y)  # Single tap
    elif button == mouse.Button.right:
        self.go_back()  # Back gesture
    elif button == mouse.Button.middle:
        self.go_home()  # Home action

Features include:

      Real-time coordinate conversion between PC and device resolutions

      Double-click detection for special actions (Instagram likes)

      Multi-threaded input handling to prevent UI blocking

      Native gesture support (swipe, scroll, tap)

# Technology Stack & Implementation

<img src="https://img.shields.io/badge/-Python%203.8%2B-FFE4E1?style=for-the-badge&logo=python&logoColor=black"> <img src="https://img.shields.io/badge/-PyNuput%20Library-FFE4E1?style=for-the-badge&logo=keyboard&logoColor=black"> <img src="https://img.shields.io/badge/-ADB%20Protocol-FFE4E1?style=for-the-badge&logo=android&logoColor=black">

---

- Core Dependencies:
  
      subprocess: Manages ADB process execution

      pynput: Advanced mouse input capture and handling

      threading: Non-blocking input processing

      Custom ADB wrapper classes for device communication

- Key Features:

      Automatic ADB path detection across platforms

      Connection timeout management

      Error handling and recovery systems

      Real-time performance monitoring

# Development Status & Roadmap

<img src="https://img.shields.io/badge/-BETA%20TESTING-FFE4E1?style=for-the-badge&logo=testrail&logoColor=black"> <img src="https://img.shields.io/badge/-ACTIVE%20DEVELOPMENT-FFE4E1?style=for-the-badge&logo=github&logoColor=black">

---

- Current Beta Features:

      Stable USB and WiFi mirroring

      Basic input control system

      Audio streaming support
  
      Resolution and quality settings

- Known Limitations:

      Occasional latency spikes on WiFi

      Limited to Android devices

      Requires USB debugging enabled

- Planned Improvements:

      Touchscreen gesture support

      Multi-device management

      Enhanced audio quality options

      Cross-platform compatibility improvements


Note: This project demonstrates advanced Python integration with Android debugging tools and real-time video streaming capabilities. Contributions and feedback are welcome to enhance functionality and stability.

GitHub Repository: Available for developers interested in contributing to mobile screen mirroring technology.

---

# Sobre o Desenvolvedor

<img src="https://img.shields.io/badge/-Vexy/Velquis-6A0DAD?style=for-the-badge&logo=atom&logoColor=white"> <img src="https://img.shields.io/badge/-Python%20Developer-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/-Android%20Enthusiast-3DDC84?style=for-the-badge&logo=android&logoColor=white"> <img src="https://img.shields.io/badge/-Open%20Source-25BE00?style=for-the-badge&logo=opensourceinitiative&logoColor=white">

Se precisar entrar em contato comigo, me chame no twitter/discord para que eu possa ver o necessario para arrumar o mais rapido possivel

Contatos:

- discord: velquis
- twitter: z_vexy
