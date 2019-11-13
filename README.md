# OverWatch Stream Editing Automation

This project is to automate manual editing/cutting special action timestamps
from overwatch game. We used computer vision to detect a particular action and
based on timestamps given by user to cut " how many seconds before action happened
and how man after action happened". And this code will create a movie based on all
the actions from a particular game play video input.

Key Improvements:

1. Reduced video processing time by 370% through implementing binary search on which frame needs to be processed as per Game Action.
2. Improved fame action template matching by 24.27 sec/frame through partitioning frames(10 frames/core/flow) and optimized c++ implementation to find normalized correlation coefficient.

Currently we have support for 'Enemy Slept' Action available for editing.

![action_template](template.png)  &nbsp; Only for this action in the gameplay.

## Getting Started

```
# command to use
python3 core.py --file --output --before --after
e.g: python3 core.py --file todaysteream.mp4 --output youtubechannel_upload.mp4 --before 120 --after 120 

=> file takes your game play video file name
=> output is the filename you want to produce output
=> before takes time will cut before(in seconds) from the action started
=> after takes time will cut after(in seconds) from the action started
```

### Prerequisites

What things you need to install the software and how to install them

```
1. Linux (Tested on Ubuntu 16.04) [for ffmpeg dependency]
2. ffmpeg (sudo apt install ffmpeg)
3. Pytesseract (pip3 install pytesseract)
4. opencv (pip3 install opecv-python)
```


## Built With

* [Python 3](http://www.python.org) - Primary Language Used
* [C++](http://www.cplusplus.com) - SecondaryLanguage Used
* [ffmpeg](http://www.ffmpeg.org) - To cut/join the frames.
* [OpneCV](https://opencv.org) - To detect actions by using template matching algorithm.
* [Pytesseract](https://pytesseract.io) - To extract text from image
* [SQLite](https://sqlite.org) - To store previous folder fingerprint and temporary frame data.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


