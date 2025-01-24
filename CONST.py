MODEL_NAMES = ["gemma2:2b", "qwen2.5:3b", "exaone3.5:2.4b"]

PROMPT_LIBRARY = {
    "USER_PROMPT": "\nQuestion: ",



    "DPI": """You are a helpful assistant specialized in gaming gear optimization, particularly in determining the best DPI settings for gaming. Your goal is to engage users in a series of well-structured questions along with four multiple-choice answers to help them find an optimal DPI for their gaming setup.

                              **User Profile**:
                              - **Game**: {game}
                              - **Mouse**: Logitech G502 Hero
                              - **Keyboard**: Logitech G Pro X

                              ### Guidelines:
                              1. Begin by asking the user their **current DPI**. Include a choice for "Not sure" if they don't know.
                              2. Always provide 4 choices along with the questions.
                              3. Ask if they are satisfied with their current DPI. If they are, conclude the session by affirming their settings.
                              4. If they are not satisfied, ask about the **specific issue** they are experiencing (e.g., too fast, too slow, or inconsistent tracking).
                              5. Follow up with targeted questions to dig deeper into their gaming style and preferences:
                                - The type of game they play and how they interact with it (e.g., fast reflex-based games, precision shooting, or strategy games).
                                - The size of their mousepad or available space for movement.
                                - Their preferred grip style (e.g., palm, claw, or fingertip grip).

                              ### Example Dialogue:
                              - "What is your current DPI setting?"
                                1. 800
                                2. 1200
                                3. 1600
                                4. Not sure

                              - "Are you happy with your current DPI?"
                                1. Yes, it feels just right.
                                2. No, it feels too slow.
                                3. No, it feels too fast.
                                4. No, it feels inconsistent.

                              - "What issue do you face with your current DPI?"
                                1. I overshoot targets often.
                                2. I struggle to make precise movements.
                                3. It feels inconsistent during gameplay.
                                4. Not sure.

                              Continue asking relevant questions, always providing 3 well-thought-out options, and adapt based on the user's responses to recommend a suitable DPI range or additional adjustments they can try.
 """,
    "MACROS": """You are a knowledgeable assistant specializing in gaming peripherals, particularly in setting up macros for gaming keyboards. Your objective is to guide users through a series of questions to understand their gaming needs and preferences, helping them create custom macros for enhanced gameplay.

              You can choose from the following MACROS:
              - CUSTOM TEXT OR EMOJIS: Assign a specific text or emoji sequence to a key for quick communication or emote usage.
              - DISCORD DEAFEN/MUTE: Set up a macro to quickly mute or deafen yourself
              - STREAMING FUNCTIONS: Macros for starting/stopping streams, switching scenes, or adjusting audio levels.
              - GAME-SPECIFIC MACROS RECOMMENDATIONS: IN-GAME POPULAR MACROS FOR GAMES LIKE FORTNITE, APEX LEGENDS, ETC.
              - CUSTOM MACROS: Create your own custom macros for specific in-game actions or commands.
""",
}


actions_macros = {
    "Copy": {
        "description": "Copies the selected text or item.",
        "default_keys": "Ctrl+C"
    },
    "Paste": {
        "description": "Pastes the copied text or item.",
        "default_keys": "Ctrl+V"
    },
    "Undo": {
        "description": "Reverses the last action performed.",
        "default_keys": "Ctrl+Z"
    },
    "Redo": {
        "description": "Reapplies the last undone action.",
        "default_keys": "Ctrl+Y"
    },
    "Volume Up": {
        "description": "Increases the system volume.",
        "default_keys": "None"
    },
    "Volume Down": {
        "description": "Decreases the system volume.",
        "default_keys": "None"
    },
    "Mute": {
        "description": "Mutes the system audio.",
        "default_keys": "None"
    },
    "Play/Pause": {
        "description": "Toggles media playback.",
        "default_keys": "Media Key"
    },
    "Next Track": {
        "description": "Skips to the next track in a playlist.",
        "default_keys": "Media Key"
    },
    "Previous Track": {
        "description": "Returns to the previous track in a playlist.",
        "default_keys": "Media Key"
    },
    "Open Calculator": {
        "description": "Launches the calculator application.",
        "default_keys": "None"
    },
    "Lock Screen": {
        "description": "Locks the computer screen.",
        "default_keys": "Windows+L"
    },
    "Show Desktop": {
        "description": "Minimizes all windows to show the desktop.",
        "default_keys": "Windows+D"
    },
    "Game Action - Reload": {
        "description": "Performs the reload action in FPS games.",
        "default_keys": "R"
    },
    "DPI Up": {
        "description": "Increases the mouse DPI setting.",
        "default_keys": "None"
    },
    "DPI Down": {
        "description": "Decreases the mouse DPI setting.",
        "default_keys": "None"
    },
    "Sniper DPI": {
        "description": "Temporarily reduces the DPI for precision aiming.",
        "default_keys": "None"
    },
    "Switch Profile": {
        "description": "Changes to a different device profile.",
        "default_keys": "None"
    },
    "Text Snippet": {
        "description": "Inserts a predefined text snippet.",
        "default_keys": "None"
    },
    "Start/Stop Recording": {
        "description": "Toggles recording in OBS or similar software.",
        "default_keys": "None"
    },
    "Switch Scene": {
        "description": "Switches scenes in OBS or similar software.",
        "default_keys": "None"
    },
    "Custom Macro": {
        "description": "Executes a user-defined macro sequence.",
        "default_keys": "None"
    },
    "Advanced Script": {
        "description": "Executes a custom LUA script for complex actions.",
        "default_keys": "None"
    },
    "Brush Size Increase": {
        "description": "Increases the brush size in graphic design tools.",
        "default_keys": "None"
    },
    "Brush Size Decrease": {
        "description": "Decreases the brush size in graphic design tools.",
        "default_keys": "None"
    },
    "Zoom In": {
        "description": "Zooms into the active window or application.",
        "default_keys": "Ctrl++"
    },
    "Zoom Out": {
        "description": "Zooms out of the active window or application.",
        "default_keys": "Ctrl+-"
    },
}

# Function-Compatible Dictionary
def get_actions():
    return actions_macros

# Example function to list all actions and descriptions
def list_actions():
    actions = get_actions()
    for name, details in actions.items():
        print(f"Action: {name}")
        print(f"  Description: {details['description']}")
        print(f"  Default Keys: {details['default_keys']}\n")

# Call the function to display all actions
if __name__ == "__main__":
    list_actions()
