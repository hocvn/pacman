# Pacman

## Description

Pacman is a project that implements a simple game inspired by the classic Pacman. This repository contains the source code, assets, and documentation needed to use and extend the project.

## Features

- Classic Pacman gameplay
- Customizable levels and characters
- Multiplayer support

## Installation

To get started with the project, follow these steps:

1.  Clone the repository:

    ```bash
    git clone https://github.com/hocvn/pacman.git
    ```

2.  The coordinates of ghosts in pacman game
    write here..

    `Pink ghost:`  
    Top-left corner:

    > Current memory usage: 0.146174MB;  
    > Peak: 0.153022MB  
    > Time taken: 33.29 seconds  
    > Expanded nodes: 118

    Top-right corner:

    > Current memory usage: 0.146174MB;  
    > Peak: 0.153022MB  
    > Time taken: 46.45 seconds  
    > Expanded nodes: 141

    Bottom-left corner:

    > Current memory usage: 0.146174MB  
    > Peak: 0.153022MB  
    > Time taken: 43.61 seconds  
    > Expanded nodes: 194

    Bottom-right corner:

    > Current memory usage: 0.146616MB  
    > Peak: 0.153464MB  
    > Time taken: 52.04 seconds  
    > Expanded nodes: 151

    Random position:

    > Current memory usage: 0.146174MB  
    > Peak: 0.153022MB  
    > Time taken: 47.38 seconds  
    > Expanded nodes: 140

    `Blue ghost:`

    Top-left corner:
    
    > Current memory usage: 0.106881MB
    > Peak: 0.113729MB
    > Time taken: 7.99 seconds
    > Expanded nodes: 104

    Top-right corner:

    > Current memory usage: 0.106563MB
    > Peak: 0.113411MB
    > Time taken: 8.01 seconds
    > Expanded nodes: 103
      
    Bottom-left corner:

    > Current memory usage: 0.106563MB
    > Peak: 0.113411MB
    > Time taken: 8.00 seconds
    > Expanded nodes: 112

    Bottom_right corner

    > Current memory usage: 0.106563MB
    > Peak: 0.113411MB
    > Time taken: 7.99 seconds
    > Expanded nodes: 100
    
    Random position:
    
    > Current memory usage: 0.106563MB
    > Peak: 0.113411MB
    > Time taken: 7.07 seconds
    > Expanded nodes: 111


# Record search time, memory usage, and number of expanded nodes.
`Pink Ghost - DFS`
1. ghost: Top-left corner, pacman: Center of maze
Current memory usage: 0.183794MB
Peak: 0.394721MB
Time taken: 32.92 seconds
Expanded nodes: 118

2. ghost: Top-right corner, pacman: Center-bottom of maze
Current memory usage: 0.178122MB
Peak: 0.388914MB
Time taken: 46.38 seconds
Expanded nodes: 173

3. ghost: bottom-left, pacman:  right-center of maze
Current memory usage: 0.178122MB
Peak: 0.388914MB
Time taken: 46.38 seconds
Expanded nodes: 173

4. ghost: bottom-right, pacman:  left-top of maze
Current memory usage: 0.181949MB
Peak: 0.392876MB
Time taken: 43.13 seconds
Expanded nodes: 185

5. ghost: center of maze, pacman: right-bottom of maze 
Current memory usage: 0.179742MB
Peak: 0.390669MB
Time taken: 44.95 seconds
Expanded nodes: 173

`Blue Ghost - BFS`
1. ghost: Top-left corner, pacman: Center of maze
Current memory usage: 0.188382MB
Peak: 0.399309MB
Time taken: 7.91 seconds
Expanded nodes: 104

2. ghost: Top-right corner, pacman: Center-bottom of maze
Current memory usage: 0.179135MB
Peak: 0.389927MB
Time taken: 12.08 seconds
Expanded nodes: 208

3. ghost: bottom-left, pacman:  right-center of maze
Current memory usage: 0.182488MB
Peak: 0.393415MB
Time taken: 13.92 seconds
Expanded nodes: 225

4. ghost: bottom-right, pacman:  left-top of maze
Current memory usage: 0.179675MB
Peak: 0.390512MB
Time taken: 16.24 seconds
Expanded nodes: 247

5. ghost: center of maze, pacman: right-bottom of maze 
Current memory usage: 0.182082MB
Peak: 0.392964MB
Time taken: 7.91 seconds
Expanded nodes: 238


`Orange Ghost - UCS`
1. ghost: Top-left corner, pacman: Center of maze
Current memory usage: 0.187842MB
Peak: 0.398769MB
Time taken: 7.91 seconds
Expanded nodes: 199

2. ghost: Top-right corner, pacman: Center-bottom of maze
Current memory usage: 0.181891MB
Peak: 0.392773MB
Time taken: 12.08 seconds
Expanded nodes: 407

3. ghost: bottom-left, pacman:  right-center of maze
Current memory usage: 0.184186MB
Peak: 0.395158MB
Time taken: 14.03 seconds
Expanded nodes: 452

4. ghost: bottom-right, pacman:  left-top of maze
Current memory usage: 0.181036MB
Peak: 0.391918MB
Time taken: 16.25 seconds
Expanded nodes: 490

5. ghost: center of maze, pacman: right-bottom of maze 
Current memory usage: 0.178355MB
Peak: 0.389147MB
Time taken: 7.91 seconds
Expanded nodes: 467


`Red Ghost - A*`
1. ghost: Top-left corner, pacman: Center of maze
Current memory usage: 0.186357MB
Peak: 0.397284MB
Time taken: 7.89 seconds
Expanded nodes: 42

2. ghost: Top-right corner, pacman: Center-bottom of maze
Current memory usage: 0.183209MB
Peak: 0.394181MB
Time taken: 12.07 seconds
Expanded nodes: 74

3. ghost: bottom-left, pacman:  right-center of maze
Current memory usage: 0.179069MB
Peak: 0.389906MB
Time taken: 13.91 seconds
Expanded nodes: 142

4. ghost: bottom-right, pacman:  left-top of maze
Current memory usage: 0.183659MB
Peak: 0.394586MB
Time taken: 16.25 seconds
Expanded nodes: 65

5. ghost: center of maze, pacman: right-bottom of maze 
Current memory usage: 0.179157MB
Peak: 0.390039MB
Time taken: 7.90 seconds
Expanded nodes: 42
