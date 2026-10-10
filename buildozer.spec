[app]
title = BELKURI CRUNCH
package.name = belkuricrunch
package.domain = com.belkuricrunch

source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav
requirements = python3,kivy==2.3.0,pyjnius
version = 1.0.0

orientation = portrait
fullscreen = 0

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/belkui.png

android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.Material.Light.NoActionBar
android.permissions = android.permission.INTERNET
android.archs = arm64-v8a
android.accept_sdk_license = True

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
