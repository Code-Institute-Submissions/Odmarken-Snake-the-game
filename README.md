# Snake 

[Deployed Game](https://snakethegame-c89237210006.herokuapp.com/)

## How to Play

In the classic game Snake, your objective is to control a snake and guide it to eat the food that appears on the screen. Each time the snake eats the food, it grows longer. The challenge is to keep the snake from crashing into itself, as the game will end if that happens.

To control the snake, you can use the arrow keys or the W, A, S, D keys on your keyboard.

The game starts when you press the designated start key or button. As you navigate the snake towards the food, make sure to avoid collisions. Each time the snake eats the food, your score increases, and the snake grows longer. The goal is to achieve the highest score possible by eating as much food as you can.

Additionally, you can control the speed of the snake. Press the P key to increase the speed, making the game more challenging, or press the O key to decrease the speed if you need more time to plan your moves.

Be strategic with your movements to avoid trapping yourself, and keep an eye on the entire length of the snake to prevent accidental collisions. The game ends when the snake crashes into itself, but you can always restart and try to beat your previous high score.

Enjoy playing Snake and see how long you can grow your snake while mastering the controls and speed adjustments!

## Features

### Existing Features

- Snake Movement: The snake can be controlled using W, A, S, D keys for movement in respective directions.
- Food Generation: Food appears at random positions on the screen, and eating food increases the snake's length.
- Score Tracking: The game keeps track of the score, which increases every time the snake eats the food.
- High Score: The game saves and displays the highest score achieved in a session.
- Speed Control: Players can control the speed of the snake using the P (increase speed) and O (decrease speed) keys.
- Game Over: The game ends when the snake collides with itself, and a "Game Over" message is displayed.
- Start Screen: The game starts after pressing any key on the start screen.
- Data Model

## Data Model

- Snake: Represented by a list of coordinates where each segment of the snake resides.
- Food: Represented by a single coordinate where the food is located.
- Score: An integer value tracking the player's current score.
- High Score: An integer value tracking the highest score achieved across sessions, stored in a text file.

## Testing

### Manual Testing:

- Verify snake movement using W, A, S, D keys.
- Check food consumption and score increment.
- Confirm the snake grows in length after eating food.
- Test speed increase with P key and decrease with O key.
- Ensure game over condition works when the snake collides with itself.
- Validate high score is saved and loaded correctly localy.

## Bugs

### Solved Bugs

1. Collision Detection: Initially, the snake would not always detect collisions correctly. This was fixed by ensuring the collision logic checks all segments of the snake's body.
2. Speed Adjustment: There was an issue with the speed adjustment keys (P and O) not affecting the game's speed correctly. This was resolved by ensuring the speed variable updates were correctly applied in the game loop.
3. Food Generation: The food sometimes spawned inside the snake. This was fixed by checking the food's position against the snake's body and regenerating it if necessary.

### Validators

1. PEP8 Compliance: Code was checked using flake8 for PEP8 compliance to ensure readability and maintainability.
2. Functionality Tests: All game functionalities were manually tested to confirm they work as expected.

## Deployment

The requirements.txt file in the IDE must be updated to package all dependencies. To do this:
    1. Enter the following into the terminal: 'pip3 freeze > requirements.txt'
    1. Commit the changes and push to GitHub

* Next, follow the steps below:
    1. Login to [Heroku](https://heroku.com/)
    1. Once at your Dashboard, click 'Create New App'
    1. Enter a name for your application, this must be unique, and select a region
    1. Click 'Create App'
    1. At the Application Configuration page, apply the following to the Settings and Deploy sections:
    1. Deployment will configure and give you a viewable link

## Credits