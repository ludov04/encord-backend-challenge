## Challenge submission

Hey Encord Team!

Enjoyed coding this fun little challenge.
The implementation is optimised to be compute and memory efficient as the engine only ever keeps the 'reachable' rows in memory and maintain a 'profile' of the current state of the game to easily compute where the next piece would drop.

### Usage

There is a thin shell wrapper so that it's easy to call from the provided sample tests, simply call:

```
./tetris < input.txt
```

The program will output the result on each line on stdout.

### Debug

The program also output some debug information on stderr, you can change the debug level in order to observe the game state as it iterates through the move.

