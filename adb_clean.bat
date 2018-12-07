@echo off
set/p option = clean?
adb shell rm /sdcard/Android/data/com.tsinghua.hci.arwatch/files/*.txt
