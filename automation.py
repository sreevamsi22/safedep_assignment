#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import subprocess
import time

exe_path = input("enter path for exe file : ")


interval = 20                  #Interval in seconds

while True:
    try:
        # Run the .exe file
        print(f"Running {exe_path}...")
        subprocess.run(exe_path, check=True)
        print("Synchronization complete. Waiting for the next run...")
    except subprocess.CalledProcessError as e:
        print(f"Error while running the script: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")
    
    # Wait for the next interval
    time.sleep(interval)


# In[ ]:




