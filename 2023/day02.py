from dataclasses import dataclass

@dataclass
class Game:
    id: int = 0

    red: int = 0
    blue: int = 0
    green: int = 0

games = []
with open("day2_test_input.txt") as f:
    for line in f:
        game_id, pulls = line.split(":")

        game = Game()
        game.id = int(game_id.replace("Game ", ""))

        for pull in pulls.split(";"):
            for color_pull in pull.split(","):
                number_str, color = color_pull.strip().split(" ")
                number = int(number_str)
                setattr(game, color, max(getattr(game, color), number))

        games.append(game)

# part 1
sum = 0
for game in games:
    if game.red <= 12 and game.green <= 13 and game.blue <= 14:
        sum += game.id
print(sum)

# part 2
sum = 0
for game in games:
    sum += game.red * game.green * game.blue
print(sum)
