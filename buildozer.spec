[app]
title = BELKURI CRUNCH
package.name = belkuricrunch
package.domain = com.belkuricrunch

source.dir = .
source.main = main.py
requirements = python3,kivy
version = 1.0.0

orientation = portrait
fullscreen = 0

# Add your logo later if desired:
# presplash.filename = %(source.dir)s/assets/presplash.png
# icon.filename = %(source.dir)s/assets/icon.png

android.api = 35
android.minapi = 23
android.sdk = 35
android.ndk = 27c
android.ndk_api = 24
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.Material.Light.NoActionBar
android.permissions = INTERNET
android.arch = arm64-v8a
android.accept_sdk_license = True

p4a.branch = master

log_level = 2
warn_on_root = 1
