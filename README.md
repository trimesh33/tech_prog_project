My project was some DnD game (description bellow).
I'd love to do it, but time...

But now I have some time issues (because of cold).
So I decided to change my theme (but it was interesting...)

# Pacman game

This game was implemented as original Pacman game as a project for python course (2nd semester, MIPT).

## How to run
```
git clone git@github.com:trimesh33/tech_prog_project.git
cd tech_prog_project/source_py
pip3 install -r requirements.txt
python3 main.py [<player_name> [<map_name>]]
```
player_name: without spaces

current maps name: classic, edited

## __Game logic__
## Ghost behavior
The are two mode of ghost behavior: scatter and chase.
 Common behavior
Scatter behavior: going to the target corner and making circles around it.
Chase described in the next block.

The are severals rounds of scatter and chase behavior:
| round | scatter time | chase time |
| :---: | :---: | :---: |
| 1     | 7     | 20        |
| 2     | 7     | 20        |
| 3     | 5     | 20        |
| 4     | 5     | $\infty$  |

## Individual behavior

| ghost | color | scatter corner | behavior | target cell |
| :---: | :---: | :---: | :---: | :---:|
| Blinky | red    | top right  | following pacman | pacman position |
| Pinky  | pink   | top left | advanced following pacman | 4 steps ahead of pacman in his current direction |
| Inky   | blue   | bottom right | wait until will be eaten at least 30 points, then running in random direction | if Blinky near pacman then Inky runs toward |
| Clyde  | orange | bottom left | wait until tow third of point eaten | if pacman further than 8 cells, targeting for corner, else behaves as Blinky |

(more precise explanation https://habr.com/ru/post/109406/)

## Back to technology of programming
Objects:
- Player
- Ghosts
- Tiles
- Animation class (drawer and commander)


### __Current__
Patterns:
- Creational:
    - Builder for Ghosts: one class to build Ghost based on its type
    - Builder for Tiles: one class to build ground Tiles based on its type 
-  Structural:
    - Facade for Anim: animation provides interaction between Spirit, Player and Tiles (so all objects in the game)
- Behavioral:
    - State for animation which depends on game state
- Software Design:
  - Model–view–controller which provides by pygame's functions (more precise described in my previous project, where u have that all functions implementations by classes: keyboard, input, render, anim)

UML-scheme:
![uml_pacman_cur](https://user-images.githubusercontent.com/39986899/162732776-848ba388-86bf-46c1-8ac0-73b9eafc2c21.png)

### __Thoughts__

Patterns (additions):
- Creational:
    + Builder for maps
-  Structural:
    + Interfaces between Animation class and MovingObjects
    + Interfaces for Input, Timer
    + Union of Ghosts names (forgotten on diagram: must be as game states)
- Behavioral:
    - Unify behavior of Ghosts and Player by abstract class MovingObject 

UML-scheme (final):
![uml_pacman_final](https://user-images.githubusercontent.com/39986899/162732819-726c6a15-c7af-4db9-9977-62f628035da7.png)

# DnD proj
Now there is no way to run code with cmake & make, but it'll be added.
## Description
DnD isometric game, based on text-based, but game with graphics.

### Structure
In the game u have several not match option: walk throw map and find escape doing quests along the way and sometimes fighting with monsters (fights are based on your spells, that u acquire while walk through, and their damage varies from dices)

(This project base on my previous graphics project with added game logic)
### Implementation
Used pattens:
- Model-View-Controller
- Builder for Spells (in progress)
- Strategy pattern for units, that behave the same
- Singleton fof Game class


UML-scheme:

![uml_cpp](https://user-images.githubusercontent.com/39986899/162703361-7334352e-6648-45cb-9437-3760c52cdf97.png)