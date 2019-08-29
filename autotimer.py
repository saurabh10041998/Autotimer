import win32gui as w
import uiautomation as auto
import psutil
import datetime
from activity import *
import sys
import time



active_window_name = ""
activity_name = ""
#new_window_name = ""
start_time = datetime.datetime.now()
activeList = ActivityList([])
first_time = True


def get_chrome_url():
    window = w.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    return "https://"+edit.GetValuePattern().Value

def url_to_name(url):
    string_list = url.split("/")
    return string_list[2]


try:
    activeList.initialize_me()
except Exception:
    print('No Json')
    


try:
    previous_site = ""
    while True:
        HWND = w.GetForegroundWindow()
        if HWND != 0 :
            new_window_name = w.GetWindowText(HWND)
        else:
            continue
        if "Google Chrome" in new_window_name: 
            new_window_name = url_to_name(get_chrome_url())
        if active_window_name != new_window_name:
            print(active_window_name)
            activity_name = active_window_name
            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time,0,0,0,0)
                time_entry._get_specific_time()

                exists = False

                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)
                if not exists:
                    activity_ = Activity(activity_name, [time_entry])
                    activeList.activities.append(activity_)   
                with open('Activities.json', 'w') as json_file:
                    json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
            first_time = False   
            active_window_name = new_window_name
        time.sleep(1)
      
      



except KeyboardInterrupt:
    print("terminated")
    with open('Activities.json', 'w') as json_file:
        json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)