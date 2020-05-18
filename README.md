# Path Finding Algorithm Visualisation
Implement and Visualize A* and Dijkstra Algorithm in Python3 using Pygame library

Generate random maze using Depth-First Search

### Demo
Maze Generation

![maze-demo](https://github.com/JonathanChan1234/Path-Finding-Python/blob/master/maze-demo.png)

Path Finding

![demo-graph](https://github.com/JonathanChan1234/Path-Finding-Python/blob/master/demo.png)

![demo-gif](https://github.com/JonathanChan1234/Path-Finding-Python/blob/master/demo.gif)

### Project Structure

    ├── algorithm               # Implementation of the algorithm
    ├── asset                   # Picture used in visualisation
    ├── ui                     # implementation of the algorithm visualisation
    ├── ui_utility              # UI Component utility used in pygame
    └── README.md
    └── demo.gif
    └── demo.png


### Run the code
``` bash
pip install pygame
python ui/PathFindingGame.py
```


### Known Issues

Current implementation requires copying all the immediate status (visited, f distance) of the grid, which requires a lot of time to copy object. 
Copying objects in Python3 is expensive and time-consuming. Blocking nature in Python will cause "Not responding" in Pygame for large maps
