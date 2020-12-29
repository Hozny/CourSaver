# Coursaver
A python script for downloading all course content from University of Waterloo Learn courses. 

## Installation
Make sure Python3 Selenium, and a Chrome Webdriver are installed.              

Run coursaver.py with Python3 in a directory with courses.txt which must contain 
links to the homepages of courses you would like to download. 

### MacOS & Linux
Sample usage: 
```Bash
git clone https://github.com/Hozny/CourSaver.git
pip3 install selenium
# Install and add chrome driver to PATH
cd CourSaver
# Paste links to the course homepages in courses.txt
LINKS TO THE COURSE HOMPAGES IN courses.txt
python3 coursaver.py
```

![Adding course links demo](./coursaverDemo.gif)
