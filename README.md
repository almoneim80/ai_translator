### 🧠 Baligh Translator
Baligh Translator is an AI-powered translation desktop app built with Python and PyQt5.
It provides a smooth, modern, and intelligent interface for instant text translation.

### 🚀 Features
⚡ Instant translation using advanced AI models
💬 Supports multiple languages
🖥️ Clean and modern user interface
💾 Works offline after setup
🔒 Privacy-friendly – no data storage
🪟 Fully compatible with Windows 10/11

### 🧩 Requirements
If running from source:
Python 3.10 or higher
Install dependencies:
pip install -r requirements.txt


If using the executable (EXE) version:
No requirements — just run the file directly.

🏗️ Installation & Usage
🔹 Option 1 – Run directly

Open the dist/ folder

Double-click main.exe

🔹 Option 2 – Install as a Windows app

Run BalighTranslatorSetup.exe

Follow the installation wizard

Launch from:

Desktop shortcut

Windows Start menu

⚙️ Building the Executable (Developers)

To generate the .exe file:

pyinstaller main.spec


After completion, you’ll get:

dist/
 └── main.exe


To build with a custom icon or single-file mode:

pyinstaller --onefile --windowed --icon=assets/icon.ico main.py

🧠 Project Structure
BalighTranslator/
├── main.py                 # Main entry point
├── ui/                     # UI layouts and components
├── core/                   # Business logic & processing
├── assets/                 # Icons and images
├── requirements.txt
├── main.spec               # PyInstaller build spec
└── README.md

🪄 Developer Tips

Always use a virtual environment:

python -m venv venv
venv\Scripts\activate


Ensure required packages are installed:

pip install pyqt5 pyinstaller

⚠️ Notes

Supports Windows 64-bit only

If DLL errors appear, reinstall PyQt5:

pip install pyqt5==5.15.9


Avoid deleting subfolders when moving the app (unless built with --onefile)

📄 License

Released under the MIT License.
You can use, modify, and distribute the app freely, provided attribution is preserved.

👤 Developer