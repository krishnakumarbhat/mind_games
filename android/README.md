# Mario Maze Game - Android Version

## Overview

An Android app version of the Mario Maze Race game built with Apache Cordova. This wraps the web version in a native Android app container.

## Prerequisites

1. **Node.js and npm**: [Download](https://nodejs.org/)
2. **Java Development Kit (JDK)**: Version 11 or higher
3. **Android Studio**: [Download](https://developer.android.com/studio)
4. **Apache Cordova**: Install globally

## Installation Steps

### 1. Install Cordova

```bash
npm install -g cordova
```

### 2. Install Dependencies

```bash
cd android
npm install
```

### 3. Add Android Platform

```bash
cordova platform add android
```

### 4. Set Up Android SDK

Make sure you have the following environment variables set:

**Windows:**
```bash
set ANDROID_SDK_ROOT=C:\Users\YourUsername\AppData\Local\Android\Sdk
set JAVA_HOME=C:\Program Files\Java\jdk-11
```

**Linux/Mac:**
```bash
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
```

## Building the App

### Debug Build

```bash
cordova build android
```

The APK will be located at:
`platforms/android/app/build/outputs/apk/debug/app-debug.apk`

### Release Build

1. Create a keystore (first time only):
```bash
keytool -genkey -v -keystore mario-maze.keystore -alias mario-maze -keyalg RSA -keysize 2048 -validity 10000
```

2. Build the release APK:
```bash
cordova build android --release -- --keystore="mario-maze.keystore" --storePassword=yourpassword --alias=mario-maze --password=yourpassword
```

## Running the App

### On Emulator

1. Create an Android Virtual Device (AVD) in Android Studio
2. Start the emulator
3. Run:
```bash
cordova emulate android
```

### On Physical Device

1. Enable Developer Options on your Android device
2. Enable USB Debugging
3. Connect device via USB
4. Run:
```bash
cordova run android
```

## Testing Without Building APK

You can test the mobile version directly in a browser:

```bash
cd www
python -m http.server 8000
```

Then open `http://localhost:8000` on your mobile browser.

## Project Structure

```
android/
├── www/                    # Web assets
│   ├── index.html         # Mobile-optimized HTML
│   ├── styles.css         # Mobile styles
│   ├── maze.js           # Maze logic
│   └── game-mobile.js    # Mobile game logic
├── config.xml            # Cordova configuration
├── package.json          # NPM dependencies
└── README.md            # This file
```

## Features

- Touch-optimized controls
- Responsive design for different screen sizes
- Fullscreen game experience
- Same gameplay as desktop versions
- Smart AI opponent

## Troubleshooting

### Issue: "Android SDK not found"
**Solution**: Set ANDROID_SDK_ROOT environment variable

### Issue: "Java not found"
**Solution**: Install JDK 11 or higher and set JAVA_HOME

### Issue: "Gradle build failed"
**Solution**: Open Android Studio, accept all SDK licenses:
```bash
cd $ANDROID_SDK_ROOT/tools/bin
./sdkmanager --licenses
```

### Issue: "Device not detected"
**Solution**: 
1. Enable USB Debugging on device
2. Install device drivers
3. Run `adb devices` to verify connection

## Building for Distribution

### Google Play Store

1. Create a production keystore
2. Build signed APK
3. Test thoroughly on multiple devices
4. Create Google Play Developer account
5. Upload APK to Play Console
6. Fill in app details and screenshots
7. Submit for review

### Direct Distribution

1. Build signed APK
2. Upload to your website
3. Users must enable "Install from Unknown Sources"

## Performance Optimization

- Game runs at 60 FPS
- Optimized canvas rendering
- Minimal battery usage
- Small APK size (~5 MB)

## Supported Versions

- **Minimum Android Version**: 5.1 (API Level 22)
- **Target Android Version**: 13 (API Level 33)
- **Recommended**: Android 8.0+ for best performance

## Controls

- **Touch Buttons**: Arrow buttons to move Mario
- **New Maze**: Button to generate new maze
- **Restart**: Button after game over

## License

MIT License - Free to use and modify!

## Additional Resources

- [Cordova Documentation](https://cordova.apache.org/docs/en/latest/)
- [Android Development](https://developer.android.com/)
- [Building Your First App](https://cordova.apache.org/docs/en/latest/guide/cli/)
