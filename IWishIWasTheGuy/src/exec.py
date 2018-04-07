import cx_Freeze

executables = [cx_Freeze.Executable("IWishIWasTheGuy.py")]

cx_Freeze.setup(
    name="I Wish I was the Guy",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":[
                               "__init__.py",
                               "cannon2.png",
                               "cannonball.png",
                               "canon.ogg",
                               "constants.py",
                               "double_jump_sound.ogg",
                               "eggman.png",
                               "eggman1.png",
                               "eggman2.png",
                               "eggman3.png",
                               "enemies.py",
                               "jump_sound.ogg",
                               "levels.py",
                               "platforms.py",
                               "player.py",
                               "projectiles.py",
                               "shoot.ogg",
                               "spritesheet_functions.py",
                               "TheKid.png"
                               ]}},
    executables = executables

    )
