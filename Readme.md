purpose
----------
processes and displays pro sensitivity stats for competitive fps games 

requires
----------
python3 and chrome web driver to run

update_sens.py
----------
1. webscrapes from https://prosettings.net/ to gather sensitivities pros
use on different competitive games.
2. Converts sensitivities to cm/360 degrees using https://gamepros.gg/mouse-sensitivity-converter
3. Saves data for each game to csv files

stats.py 
----------
uses numpy to gather csv files information and display the 25th 50th(median) and 75th percentiles, as well as the average. 