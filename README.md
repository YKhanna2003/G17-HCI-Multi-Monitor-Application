# Smart Multi-Monitor Gaze Detection

❗️<mark> Currently Supported for Windows only.</mark>

## About the Project
1. This tool utlises GazePointer: A Webcam eye tracker software that lets us determine the position of an individual's gaze on the screen. 
2. GazePointer API provides the GazeX and GazeY coordinates.
3. These Coordinates can be utilised along with key-binding techniques to perform a variety of on-screen interactive actions. 

### On-Screen Interactions<br/>
 1. Move Window<br/>
 2. Desktop Switching<br/>
 3. Scrolling<br/>
 4. Resizing<br/>
 5. Active window focus<br/>

### How to use
1. Download, Install and Run GazePointer from [here](https://sourceforge.net/projects/gazepointer/)
2. Calibrate GazePointer by following the instructions.
3. Run requirements.txt. For mouse functionality refer to the "mouse" Source Files in Main.

```bash
pip install -r requirements.txt
```

4. Run the python script gazefunction.py.

```bash
python3 gazefunction.py
```

5. Code will track your gaze and you can control your desktop just by your eye movement.

### Key bindings
1. <kbd>Alt</kbd> + <kbd>w</kbd> Hold to Activate Window Relocation
2. <kbd>Alt</kbd> + <kbd>s</kbd> Hold to Activate Active-Window Resizing
3. <kbd>Alt</kbd> + <kbd>a</kbd> Press to Activate Eye-Scrolling
4. <kbd>Alt</kbd> + <kbd>z</kbd> Hold to Change Active Window
5. Desktop Switching is always active<br/>
