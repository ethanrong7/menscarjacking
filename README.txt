1. install python 3.9 https://www.python.org/downloads/ (any of the 3.9.x versions should be fine)
2. once installed, you will need to manually install some of the python dependencies. Go to your cmd.exe or terminal
   and type the following:
   1. pip install pynput
   2. pip install keyboard
3. Once dependencies are installed, you need to record a macro by running:
   python record.py "{insert a description of your choice}"
   - In 3 seconds, the recording will start and it will key log all your keyboard presses and mouse clicks
   - once you're done recording, press f4 and then left click and the recording will stop
4. You should now see a txt file generated in the "data" folder with the same name as the description you gave
   - E.g. if you executed python record.py "burnium map 3"
   - The text file will be called burnium map 3.txt
5. To play the macro enter:
   - python play.py "burnium map 3" {number}
   - insert whatever number of repetitions you want in {number}
   - e.g. python play.py "burnium map 3" 8