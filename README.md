# snes_move_trainer

* Install pygame

Once that is installed, right now you run the script with python3.

python3 trainer.py

*Right now the script is setup to train for a mockball*

As a note, it's not great. I want to add timing, etc into it. However right now it times how fast you can perform the move.

````
C:\Users\hotdog\Documents\projects\metroid_training>python trainer.py
pygame 1.9.4
Hello from the pygame community. https://www.pygame.org/contribute.html
input finished
First Sequence ['B', 'Right']
Next Sequence ['B', 'Right', 'A']
Next Sequence ['B', 'Right']
Next Sequence ['B', 'Right', 'A']
Next Sequence ['B', 'Down', 'A']
Next Sequence ['B', 'A']
Next Sequence ['B', 'Down', 'A']
Next Sequence ['B', 'Right', 'A']
It took you  3.6762565 seconds
````

Next Todo is to add some timing constraints, so maybe from when you hit B right you have to hit A within a certain amount of time, not sure.

I also plan to make it so you can just use a json file to load in and it'll train you. 

Some kind of visual feedback might be useful too.

i primarily built this so i could practice moves for super metroid impossible.

you can see my slow progress here:

https://youtu.be/z-7ytkaTlHc


