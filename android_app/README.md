# TheFatRat Android Installer

A mobile application to run the TheFatRat installation process on rooted Android devices.

## Features

- Web-based UI (Streamlit)
- Automated TheFatRat setup and dependency installation
- Package and prepare files for deployment
- Real-time installation logs and status monitoring
- Support for rooted Android devices (Samsung Galaxy S25+)

## Requirements

- Rooted Android device (Galaxy S25 or similar)
- Python 3.8+
- Kivy framework
- Streamlit
- Termux or similar terminal emulator

## Installation

### Option 1: Build APK (Recommended)
```bash
cd android_app
./build_apk.sh
```

### Option 2: Run on Device with Termux
1. Install Termux on your Android device
2. Install Python: `apt install python3 python3-pip`
3. Clone the repo and install dependencies:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Launch the app on your Android device
2. Configure installation preferences
3. Start the installation process
4. Monitor progress and logs in real-time
5. Package files for deployment when complete

## Project Structure

```
android_app/
├── app.py                 # Main Streamlit application
├── main.py               # Kivy entry point
├── buildozer.spec        # APK build configuration
├── requirements.txt      # Python dependencies
├── setup_manager.py      # TheFatRat setup logic
├── file_manager.py       # File packaging utilities
├── config/               # Configuration files
└── build/               # Build output directory
```

## Configuration

Edit `config/settings.json` to customize:
- Installation paths
- Package selections
- Deployment targets

## Building the APK

```bash
cd android_app
pip install buildozer cython
buildozer android debug
# APK output: bin/thefatrat-android-*.apk
```

## Troubleshooting

- Ensure device is rooted
- Check internet connection
- Verify Python 3.8+ installed
- Review logs in `logs/` directory

## License

Same as TheFatRat (Original project by Screetsec)

## Support

For issues with the original TheFatRat: https://github.com/screetsec/TheFatRat
For Android app issues: https://github.com/ryanrebel/TheFatRat/issues
