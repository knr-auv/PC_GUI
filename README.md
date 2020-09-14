# PC_GUI


## How to
Recomended python version for running GUI is 3.8. It is possible to run app on python 3.7 but then asyncio goes crazy with debug logs so i recommend to disable/change logging level (line 20 in main.py). 

 - install all dependencies
 - build or [download simulation for windows](https://wutwaw-my.sharepoint.com/:f:/g/personal/01150165_pw_edu_pl/EjOHoKseOLNOgENz9IiM4V0BiRVOugkU3vvRkIwqplCoFQ?e=8MJe4b "LearnpyQt")
 - git clone https://github.com/knr-auv/jetson-v2/tree/GuiIntegration
 - run simulation (simulation must be running before starting odroid client)
 - run odroid client
 - run GUI

All packages are available in standard pip repository. Pip install should work just fine.

Required packages:
  - asyncio
  - pyqt5
  - inputs
## Control
Boat can be controlled by keyboard or pad. After selecting the appropriate control method click start then arm. Pad control method can be started only if Xbox one/360 or ps4 pad is detected. All controls and osd settings are automatically stored after each change. They will be loaded every time GUI is launched.
