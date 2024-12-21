#!/usr/bin/env python3

import os
from random import choice
from time import sleep

import vizdoom as vzd

if __name__ == "__main__":
    # Create DoomGame instance. It will run the game and communicate with you.
    game = vzd.DoomGame()

    # load_config could be used to load configuration instead of doing it here with code.
    # If load_config is used in-code configuration will also work - most recent changes will add to previous ones.
    game.load_config("../conf/common.cfg")

    # Sets path to additional resources wad file which is basically your scenario wad.
    # If not specified default maps will be used and it's pretty much useless... unless you want to play good old Doom.
    #game.set_doom_scenario_path(os.path.join(vzd.scenarios_path, "basic.wad"))

    # Sets map to start (scenario .wad files can contain many maps).
    #game.set_doom_map("map01")

    # Sets resolution. Default is 320X240
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)

    # Sets the screen buffer format. Not used here but now you can change it. Default is CRCGCB.
    #game.set_screen_format(vzd.ScreenFormat.RGB24)

    # Set available buttons
    game.set_available_buttons(
        [vzd.Button.MOVE_LEFT, vzd.Button.MOVE_RIGHT, vzd.Button.ATTACK]
    )

    # Debug options
    #game.set_labels_buffer_enabled(True)
    #game.set_automap_buffer_enabled(True)
    #game.set_objects_info_enabled(True)
    #game.set_sectors_info_enabled(True)
    #print("Available buttons:", [b.name for b in game.get_available_buttons()])
    #print("Available game variables:", [v.name for v in game.get_available_game_variables()])

    # Causes episodes to finish after 200 tics (actions)
    game.set_episode_timeout(200)

    # Makes episodes start after 10 tics (~after raising the weapon)
    game.set_episode_start_time(10)

    # Makes the window appear (turned on by default)
    game.set_window_visible(True)

    # Turns on the sound. (turned off by default)
    game.set_sound_enabled(True)
    # Because of some problems with OpenAL on Ubuntu 20.04, we keep this line commented,
    # the sound is only useful for humans watching the game.

    # Turns on the audio buffer. (turned off by default)
    # If this is switched on, the audio will stop playing on device, even with game.set_sound_enabled(True)
    # Setting game.set_sound_enabled(True) is not required for audio buffer to work.
    # game.set_audio_buffer_enabled(True)
    # Because of some problems with OpenAL on Ubuntu 20.04, we keep this line commented.

    # Sets the living reward (for each move) to -1
    game.set_living_reward(-1)

    # Sets ViZDoom mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR, PLAYER mode is default)
    game.set_mode(vzd.Mode.PLAYER)

    # Enables engine output to console, in case of a problem this might provide additional information.
    # game.set_console_enabled(True)

    # Initialize the game. Further configuration won't take any effect from now on.
    game.init()

    # Define some actions. Each list entry corresponds to declared buttons:
    # MOVE_LEFT, MOVE_RIGHT, ATTACK
    # game.get_available_buttons_size() can be used to check the number of available buttons.
    # 5 more combinations are naturally possible but only 3 are included for transparency when watching.
    actions = [
        [True, False, False],
        [False, True, False],
        [False, False, True]
    ]

    # Run this many episodes
    episodes = 10

    # Sets time that will pause the engine after each action (in seconds)
    # Without this everything would go too fast for you to keep track of what's happening.
    sleep_time = 1.0 / vzd.DEFAULT_TICRATE  # = 0.028

    for i in range(episodes):
        print(f"Episode #{i + 1}")

        # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
        game.new_episode()

        while not game.is_episode_finished():

            # Gets the state
            state = game.get_state()

            # Which consists of:
            n = state.number
            vars = state.game_variables

            # Different buffers (screens, depth, labels, automap, audio)
            # Expect of screen buffer some may be None if not first enabled.
            screen_buf = state.screen_buffer
            depth_buf = state.depth_buffer
            labels_buf = state.labels_buffer
            automap_buf = state.automap_buffer
            audio_buf = state.audio_buffer

            # List of labeled objects visible in the frame, may be None if not first enabled.
            labels = state.labels

            # List of all objects (enemies, pickups, etc.) present in the current episode, may be None if not first enabled
            objects = state.objects

            # List of all sectors (map geometry), may be None if not first enabled.
            sectors = state.sectors

            # Games variables can be also accessed via
            # (including the ones that were not added as available to a game state):
            # game.get_game_variable(GameVariable.AMMO2)

            # Makes an action (here random one) and returns a reward.
            r = game.make_action(choice(actions))

            # Makes a "prolonged" action and skip frames:
            # skiprate = 4
            # r = game.make_action(choice(actions), skiprate)

            # The same could be achieved with:
            # game.set_action(choice(actions))
            # game.advance_action(skiprate)
            # r = game.get_last_reward()

            # Prints state's game variables and reward.
            print(f"State #{n}")
            print("Game variables:", vars)
            print("Reward:", r)
            print("=====================")

            if sleep_time > 0:
                sleep(sleep_time)

        # Report on the episode
        print("Episode finished.")
        print("Total reward:", game.get_total_reward())
        print("************************")

    game.close()
