#This Script checks every 3 seconds if there are any sources active that are greater than 0 by 0 pixels, and if there are, and the replay buffer is not active, then it starts the replay buffer, and vice versa.
#Finally my monitors can sleep
import obspython as obs
import os

def is_live_preview_showing_video():
    current_scene_as_source = obs.obs_frontend_get_current_scene()
    if current_scene_as_source:
        current_scene = obs.obs_scene_from_source(current_scene_as_source)
        scene_items = obs.obs_scene_enum_items(current_scene)
        for scene_item in scene_items:
            source = obs.obs_sceneitem_get_source(scene_item)
            width = obs.obs_source_get_width(source)
            if width > 0:
                return True
        return False
    

def start():
    if not obs.obs_frontend_replay_buffer_active():
        obs.obs_frontend_replay_buffer_start()
        
def stop():
    if obs.obs_frontend_replay_buffer_active():
        obs.obs_frontend_replay_buffer_stop()

if os.name == 'nt':
    from ctypes import windll, wintypes, WinError, get_last_error, byref, Structure
    class LASTINPUTINFO(Structure):
        _fields_ = [("cbSize", wintypes.UINT),
                    ("dwTime", wintypes.DWORD)]

    user32 = windll.user32
    kernel32 = windll.kernel32

    def get_last_input_time():
        lii = LASTINPUTINFO()
        lii.cbSize = 8

        if user32.GetLastInputInfo(byref(lii)):
            system_uptime = kernel32.GetTickCount() & 0xFFFFFFFF
            last_input_tick = lii.dwTime

            if system_uptime < last_input_tick:
                elapsed_ms = (system_uptime + (0xFFFFFFFF + 1)) - last_input_tick
            else:
                elapsed_ms = system_uptime - last_input_tick

            return elapsed_ms
        else:
            raise WinError(get_last_error())
        
    def callback(): 
        if (not is_live_preview_showing_video()) or (get_last_input_time() > 600000) :
            stop()   
        else:
            start()
else:
    def callback():
        if (not is_live_preview_showing_video()):
            stop()   
        else:
            start()

obs.timer_add(callback, 3000)
