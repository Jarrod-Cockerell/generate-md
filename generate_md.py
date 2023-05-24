from os import path
import os
import openai
import sys

openai.api_key_path = '.key'


def get_completion(prompt, model="gpt-3.5-turbo"):
    """ Get a completion from the OpenAI API."""
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


def generate_markdown(code):
    """ Generate markdown documentation for a given code snippet."""
    example = f"""
    ## PlayerController Documentation

    ### Overview
    The `PlayerController` script is responsible for controlling the player character in a Unity game. It handles player locomotion, including movement, rotation, and jumping.

    ### Dependencies
    - UnityEngine
    - Rigidbody (required component)

    ### Public Properties

    #### `float Speed`
    - Description: The current speed of the player character.
    - Getter: `get;`
    - Setter: Private

    #### `Vector3 Direction`
    - Description: The direction the player character is facing.
    - Getter: `get;`
    - Setter: Private

    #### `Vector3 Velocity`
    - Description: The current velocity of the player character.
    - Getter: Returns the velocity of the Rigidbody component attached to the player.

    #### `bool MovingForward`
    - Description: Indicates whether the player character is currently moving forward.
    - Getter: `get;`
    - Setter: Private

    ### Serialized Fields

    #### `float minSpeed`
    - Description: The minimum speed of the player character.
    - Default Value: 2f

    #### `float maxSpeed`
    - Description: The maximum speed of the player character.
    - Default Value: 4f

    #### `float jumpForce`
    - Description: The force applied when the player character jumps.
    - Default Value: 1f

    ### Methods

    #### `void Start()`
    - Description: Called when the script instance is being loaded.
    - Usage: Initializes the `rb` variable by getting the `Rigidbody` component attached to the same game object.

    #### `void Update()`
    - Description: Called once per frame.
    - Usage: Handles player input and updates the player's rotation and movement.
    - Retrieves the mouse input for rotation.
    - Rotates the player character around the Y-axis based on the mouse input.
    - If the player is moving forward, moves the player character in the forward direction at the current speed.

    #### `void Jump()`
    - Description: Applies an upward force to make the player character jump.
    - Usage: Adds an upward force to the `Rigidbody` component to simulate jumping.

    #### `void MoveForward()`
    - Description: Sets the `MovingForward` property to true.
    - Usage: Used to indicate that the player character should move forward.

    #### `void DontMoveForward()`
    - Description: Sets the `MovingForward` property to false.
    - Usage: Used to indicate that the player character should stop moving forward.

    #### `void Run()`
    - Description: Sets the `Speed` property to the maximum speed.
    - Usage: Used to make the player character run.

    #### `void DontRun()`
    - Description: Sets the `Speed` property to the minimum speed.
    - Usage: Used to make the player character stop running.

    ### Required Components

    #### `Rigidbody`
    - Description: The Rigidbody component attached to the same game object.
    - Usage: Allows the player character to be affected by physics, such as applying forces for movement and jumping.
    """
    prompt = f"""
    write documentation for the code delimited by triple backticks.
    
    here is an example of the output for 'PlayerController.cs':
    {example}
    
    ```{code}```
    """
    return get_completion(prompt)


def get_all_files_in_dir(dir):
    """ Get all .cs files in a directory."""
    files = []
    for file in os.listdir(dir):
        if file.endswith(".cs"):
            files.append(os.path.join(dir, file))
    return files


if len(sys.argv) > 1:

    files = get_all_files_in_dir(sys.argv[1])

    for file in files:
        if path.exists('Docs/' + path.basename(file) + ".md"):
            print(f"Skipping {file}")
            continue
        print(f"Generating documentation for {file}")
        code = open(file, "r").read()
        md = generate_markdown(code)
        if path.exists('Docs') == False:
            os.mkdir('Docs')
        open('Docs/' + path.basename(file) + ".md", "w").write(md)
