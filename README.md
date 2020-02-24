# Coding Challenge for Luminari

####Dependencies
To install dependencies, run 
```shell script
pip install --user --requirement requirements.txt`
```

#### Running the code
```shell script
python3 main.py
```

####Database
The code uses a SQLite library to run efficiently. To reset database just simply delete assets.db

JSON files are located in `/data`
####Testing
Unit tests were written with the pytest framework.

To run the unit tests:
```shell script
cd tests
pytest test_assets.py
```