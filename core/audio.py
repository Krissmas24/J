import os
import subprocess

class AudioEngine:
    def __init__(self):
        # We'll use paplay (PulseAudio) or similar common Linux tools
        self.enabled = True

    def play_ping(self):
        if not self.enabled: return
        # Using a standard system sound as a placeholder
        # In a real app, we'd bundle custom .wav files
        try:
            subprocess.Popen(["paplay", "/usr/share/sounds/freedesktop/stereo/message.oga"], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except: pass

    def play_success(self):
        if not self.enabled: return
        try:
            subprocess.Popen(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except: pass

audio = AudioEngine()
