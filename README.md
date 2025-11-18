# Baligh Translator

**Baligh Translator** is an AI-powered desktop translation application built with **Python** and **PyQt5**. It provides a modern, intuitive interface for instant text translation, works offline, and ensures full privacy for users.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation & Usage](#installation--usage)
4. [Developer Guide](#developer-guide)
5. [Project Structure](#project-structure)
6. [AI & Models](#ai--models)
7. [Localization](#localization)
8. [Known Limitations](#known-limitations)
9. [License](#license)
10. [Developer](#developer)

---

## Features

- ⚡ **Instant Translation:** Translate text in real-time using advanced AI models.
- 💬 **Multi-Language Support:** Supports a variety of languages.
- 🖥️ **Modern User Interface:** Clean, responsive, and intuitive design.
- 💾 **Offline Mode:** Can operate without an internet connection after setup.
- 🔒 **Privacy-Friendly:** No data is stored or sent externally.
- 🪟 **Windows Compatibility:** Supports Windows 10 and 11 fully.

---

## Requirements

### Running from Source

- **Python 3.10 or higher**
- Install dependencies:
```
pip install -r requirements.txt
```

### Using Executable (EXE)
No dependencies needed. Run main.exe directly.

### Installation & Usage
Option 1 – Run Directly

### Open the dist/ folder.
1. Double-click main.exe.

### Option 2 – Install as a Windows App
1. Run BalighTranslatorSetup.exe.
2. Follow the installation wizard.
3. Launch via:
   - Desktop shortcut
   - Windows Start menu
 
### Developer Guide
- Build Executable
To create the .exe file from source:
```
pyinstaller main.spec
```
Output structure:
```
dist/
└── main.exe
```
To build a single-file executable with a custom icon:
```
pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
```
### Recommended Practices
Use a virtual environment:
 ```
python -m venv venv
venv\Scripts\activate
```
Ensure required packages are installed:
```
pip install pyqt5 pyinstaller
```

### Project Structure
```
BalighTranslator/
├── main.py              # Main entry point
├── ui/                  # UI layouts and components
├── core/                # Business logic & translation engine
├── assets/              # Icons and images
├── config/              # Configuration files
├── services/            # Services: cache, clipboard, keyboard, etc.
├── models/              # Pre-trained AI translation models
├── infrastructure/      # File/download management, quantization
├── utils/               # Helpers, logger, localization utilities
├── main.spec            # PyInstaller build spec
├── requirements.txt
└── README.md
```

### AI & Models
- AI Model: facebook/nllb-200-distilled-600M for multilingual translation.
- Offline inference supported after model download.
- Includes pytorch_model.bin, tokenizer.json, sentencepiece.bpe.model, and config files.

### Localization
- Multi-language UI support.
- Configuration file: Localization/en.json.
- Easily extendable to other languages.

## Known Limitations
Windows 64-bit only.
DLL errors may require reinstalling PyQt5:
```
pip install pyqt5==5.15.9
```
Avoid deleting subfolders unless building with --onefile.

### License
Released under the MIT License. Free to use, modify, and distribute with proper attribution.

### Developer
Abdulmonem Omar
