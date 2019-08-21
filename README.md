# Concordia Grade Fetcher

App that takes in any Concordia student ID, password and semester from Fall 2016 to Winter 2020 and outputs what is typically seen in the "View My Grades" section of the myconcordia website.

<p align="center">
  <img src="/assets/2.png" height="623" width="927">
</p>

## Requirements

#### Firefox

[Install here](https://www.mozilla.org/en-CA/firefox/new/)

#### Geckodriver
You will need to install geckodriver for access to the "HTTP API described by the WebDriver protocol to communicate with Gecko browsers, such as Firefox." 

Having the Homebrew package manager will make things easier. Install by running the following (Mac):

```bash
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install geckodriver
```

or via this link (Windows/Linux):

|OS|Link|
|--|--|
|Windows 32 bit| [mozilla/geckodriver/win32.zip](https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-win32.zip)|
|Windows 64 bit| [mozilla/geckodriver/win64.zip](https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-win64.zip)|
|Linux 32 bit| [mozilla/geckodriver/linux32.zip](https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux32.tar.gz)|
|Linux 64 bit| [mozilla/geckodriver/linux64.zip](https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz)|

#### Python Packages
See `requirements.txt`.

## Usage

Clone the repository and run the app.
```bash
$ git clone https://github.com/matteo-esposito/grade-fetcher.git
$ cd grade-fetcher
$ python app.py
```

Enter Concordia username, password and desired semester when prompted. (Password is hidden during input.)

<p align="center">
  <img src="/assets/1.png" height="623" width="927">
</p>

Get grades!

<p align="center">
  <img src="/assets/2.png" height="623" width="927">
</p>
