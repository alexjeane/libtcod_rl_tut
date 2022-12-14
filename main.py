#!/usr/bin/env python3

# This is a module with which python program (in our case, file) is calling which program.
# This can be mighty useful in detecting the sources of errors.
import traceback

# This is a roguelike centered module.  It aids in the use of things like pathfinding/field of view, etc.
import tcod

# These are references to other files in the project.  Doing this gets us the ability to make use of them.
import color
import exceptions
import setup_game
import input_handlers

# Here is our first written function (and it's a very important one at that).  It has two parameters: a request and a response.
# It passes in a request.  In this case, there's the BaseEventHandler passed in from input_handlers.  It responds (or can respond)
# with a filename so as to save the game.
def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    screen_width = 80
    screen_height = 50
    
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException: # Save on any other unexpected exception.
            save_game(handler, "save_game.sav")
            raise   


if __name__ == "__main__":
    main()