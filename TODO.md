# TODO

What I plan to do with a few thoughts behind some features

- [x] generate terrain
    - [x] implement feature tile bonuses - boost chances of same features near each other
        - [x] make the last tile of old line not impact the first tile of new line
    - [x] clean up all 1-tile land features
- [x] make a loop asking user if he wants to re-generate the map
- [x] make a pathfinding algorithm from point A to B
    - [x] display start and stop points on board
    - [x] find any path from point A to B
    - [x] find a smarter path
    - [x] check if end goal is reachable
- [ ] implement more map features, 
    - [ ] natural food trees and bushes (W - w)
        - [ ] change on collection (V - v)
    - [ ] wetland bonus (every tile near RIVER has increased farmland yields)
    - [ ] minerals (accelerating village transformation, spawning after set amount of time or increasing possibility with the number of NPCs)
- [ ] make working NPCs
    - [ ] make them roam around
    - [ ] multiply them over time
    - [ ] building houses (which with appropriate food quantities increases the number of NPCs)
    - [ ] making farmlands (granting additional food source)
- [ ] make cool counters
    - [ ] running simulation time
    - [ ] number of NPCs (big and small)
- [ ] end of loop - when the NPCs take over whole board the program asks if you want to continue
    - [ ] "postgame" - weird scifi futuristic city development?  