# simple_text_game_engine.py

class Scene:
    def __init__(self, description, choices):
        """
        description: str - what the player sees
        choices: dict - option_text -> next_scene_name or 'END'
        """
        self.description = description
        self.choices = choices


class Game:
    def __init__(self):
        self.scenes = {}
        self.start_scene = None

    def add_scene(self, name, scene, start=False):
        self.scenes[name] = scene
        if start or self.start_scene is None:
            self.start_scene = name

    def play(self):
        current = self.start_scene

        while True:
            scene = self.scenes[current]
            print("\n" + scene.description)

            if not scene.choices:
                print("\nThe game has ended.")
                break

            print("\nWhat do you do?")
            options = list(scene.choices.keys())
            for i, opt in enumerate(options, start=1):
                print(f"{i}. {opt}")

            choice = input("> ").strip()

            # handle numeric or text input
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    choice_text = options[idx]
                else:
                    print("Invalid choice. Try again.")
                    continue
            else:
                # match by text
                matches = [opt for opt in options if opt.lower() == choice.lower()]
                if not matches:
                    print("Invalid choice. Try again.")
                    continue
                choice_text = matches[0]

            next_scene = scene.choices[choice_text]

            if next_scene == "END":
                print("\n" + "-" * 30)
                print("Game over.")
                print("-" * 30)
                break

            if next_scene not in self.scenes:
                print(f"\nScene '{next_scene}' not found. Ending game.")
                break

            current = next_scene


def build_sample_game():
    game = Game()

    # Scene: intro
    intro = Scene(
        description=(
            "You wake up in a dark room. There is a door to the NORTH "
            "and a small window to the EAST."
        ),
        choices={
            "Go north through the door": "hall",
            "Look through the window": "window",
        },
    )

    # Scene: hall
    hall = Scene(
        description=(
            "You are in a narrow hall with faded portraits. A stairwell leads up."
        ),
        choices={
            "Climb the stairs": "treasure",
            "Go back to the dark room": "intro",
        },
    )

    # Scene: window
    window = Scene(
        description=(
            "The window is small but open to a courtyard below. You could try to climb out."
        ),
        choices={
            "Climb out the window": "END",
            "Return to the room": "intro",
        },
    )

    # Scene: treasure
    treasure = Scene(
        description=(
            "At the top of the stairs you find a locked chest on a pedestal."
        ),
        choices={
            "Open the chest": "END",
            "Go back down": "hall",
        },
    )

    # register scenes
    game.add_scene("intro", intro, start=True)
    game.add_scene("hall", hall)
    game.add_scene("window", window)
    game.add_scene("treasure", treasure)

    return game


def _choose_from_options(options, choice):
    # Accept numeric index or exact text (case-insensitive)
    if isinstance(choice, int):
        idx = choice
        if 0 <= idx < len(options):
            return options[idx]
        return None

    s = str(choice).strip()
    if s.isdigit():
        idx = int(s) - 1
        return _choose_from_options(options, idx)

    matches = [opt for opt in options if opt.lower() == s.lower()]
    return matches[0] if matches else None


def play_with_choices(game, choices_list):
    """Programmatically play a game using a list of choices.

    `choices_list` can contain 1-based numeric strings/ints or option text.
    Returns 'END' if the play reached an end, or the last scene name.
    """
    current = game.start_scene
    it = iter(choices_list)

    while True:
        scene = game.scenes[current]
        if not scene.choices:
            return current

        options = list(scene.choices.keys())
        try:
            choice = next(it)
        except StopIteration:
            return current

        choice_text = _choose_from_options(options, choice)
        if choice_text is None:
            return current

        next_scene = scene.choices[choice_text]
        if next_scene == "END":
            return "END"

        if next_scene not in game.scenes:
            return None

        current = next_scene


if __name__ == "__main__":
    g = build_sample_game()
    print("Sample game built. Run `python -c \"from simple_text_game_engine import build_sample_game; g=build_sample_game(); print(g.start_scene)\"` to inspect.")
 