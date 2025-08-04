
[app]

# (str) Title of your application
title = SentinelIT Mobile

# (str) Package name
package.name = sentinelitmobile

# (str) Package domain (needed for android/ios packaging)
package.domain = mail.diakriszuluinvestmentsprojects.co.za

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,json

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = kivy,plyer,requests

# (str) Fullscreen (0 if False, 1 if True)
fullscreen = 0

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (str) Icon of the application
icon.filename = assets/icon.png

# (str) Presplash of the application
presplash.filename = assets/presplash.png

# (str) Supported orientation
supported.orientation = portrait

# (str) Entry point to your application
source.main = sentinelit_mobile.py

[android]

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android architecture to build for
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.accept_sdk_license = True

# Optional filters
# android.logcat_filters = *:S python:D

# Optional debug build
# android.debug = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1