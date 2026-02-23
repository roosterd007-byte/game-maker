def play_game(game_data):
    current_room = game_data["start"]

    while True:
        room = game_data["rooms"][current_room]
        print("\n" + room["text"])

        # if no choices, game ends
        if not room["choices"]:
            print("\nThe game is over.")
            break

        print("\nWhat do you do?")
        options = list(room["choices"].keys())
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt}")

        choice = input("> ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                choice_text = options[idx]
            else:
                print("Invalid choice. Try again.")
                continue
        else:
            print("Type the number of your choice.")
            continue

        next_room = room["choices"][choice_text]

        if next_room == "END":
            print("\nGame over.")
            break

        if next_room not in game_data["rooms"]:
            print(f"\nRoom '{next_room}' not found. Ending game.")
            break

        current_room = next_room


# >>> EDIT ONLY THIS PART TO MAKE YOUR OWN GAME <<<
game_data = {
    "start": "start_room",
    "rooms": {
        "start_room": {
            "text": "You are in a small room. There is a DOOR and a CHEST.",
            "choices": {
                "Open the door": "hallway",
                "Open the chest": "chest_room"
            }
        },
        "hallway": {
            "text": "You walk into a long hallway. There is a LIGHT ahead.",
            "choices": {
                "Walk toward the light": "outside",
                "Go back": "start_room"
            }
        },
        "chest_room": {
            "text": "The chest is full of gold! But the room starts shaking.",
            "choices": {
                "Grab the gold and run": "outside",
                "Stay with the gold": "END"
            }
        },
        "outside": {
            "text": "You made it outside. You win!",
            "choices": {
                "Celebrate": "END"
            }
        }
    }
}
# >>> STOP EDITING HERE <<<

if __name__ == "__main__":
    play_game(game_data)
