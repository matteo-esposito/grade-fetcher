# Concordia Grade Fetcher

App that takes in any Concordia student ID, password and semester from Fall 2016 to Winter 2020 and outputs what is typically seen in the "View My Grades" section of the myconcordia website.

## TODO
* Exception handling for username, password and semesters
* Generalization of filepaths (`os.join()`, etc.)

## Usage

Clone the repo and run the app.
```bash
$ git clone https://github.com/matteo-esposito/grade-fetcher.git
$ cd grade-fetcher
$ python app.py
```

Enter Concordia username and password when prompted. (Password is hidden during input.)

<p align="center">
  <img src="/assets/1.png" height="449" width="668">
</p>

Enter desired semester. (Fall 2016 to Winter 2020 inclusive)

<p align="center">
  <img src="/assets/2.png" height="449" width="668">
</p>

See grades!

<p align="center">
  <img src="/assets/3.png" height="449" width="668">
</p>

