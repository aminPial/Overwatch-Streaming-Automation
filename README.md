# OverWatch Stream Editing Automation

This project is to automate manual editing/cutting special action timestamps
from overwatch game. We used computer vision to detect a particular action and
based on timestamps given by user to cut " how many seconds before action happened
and how man after action happened". And this code will create a movie based on all
the actions from a particular game play video input.

## Getting Started



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


