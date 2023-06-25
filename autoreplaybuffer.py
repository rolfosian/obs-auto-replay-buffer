#This Script checks every 3 seconds if there are any sources active that are greater than 0 by 0 pixels, and if there are, and the replay buffer is not active, then it starts the replay buffer, and vice versa.
#Finally my monitors can sleep
import obspython as obs

def start():
    if obs.obs_frontend_replay_buffer_active() is False:
        obs.obs_frontend_replay_buffer_start()
        return
    else:
        return
def stop():
    if obs.obs_frontend_replay_buffer_active() is True:
        obs.obs_frontend_replay_buffer_stop()
        return
    else:
        return

def check_live_preview():
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
                
def callback(): 
    output = check_live_preview()
    if not output:
        stop()   
    else:
        start()

obs.timer_add(callback, 3000)
