# StatCast

Cast stats from World of Warcraft to your LIFX smart lights! Please click the YouTube video below for a demo.

[![Video](http://i3.ytimg.com/vi/FFQVoTkSsx8/hqdefault.jpg)](https://youtu.be/FFQVoTkSsx8)


# Requirements

This initial version of StatCast requires World of Warcraft (retail or classic) and a LIFX multizone light. The one used for development, the LIFX Z, can be purchased [here](https://amzn.to/3kPzPdB).

# Setup

For this addon & script to work out-of-the box:

1. Ensure you have a single LIFX multizone light, such as the [LIFX Z](https://amzn.to/3kPzPdB), enabled on your network.
1. Clone this repository and place it into the Addons folder of either WoW retail or classic. **Note:** the directory name needs to be *statcast* in order for WoW to pick up the addon.
1. Make sure you have Python 3 installed.
1. Install the necessary Python dependencies: run `python3 -m pip install lifxlan`, `python3 -m pip install pyautogui`, and `python3 -m pip install mss`. Proper `setup.py` file hopefully coming soon.

# Using StatCast

Run `python3 statcast.py` from the _statcast_ directory. This script will run in the background while you play WoW. 

The default mode is HP, but you can run any of the below commands in-game to change the mode:

1. `/setmode 0`: Enables the HP mode.
1. `/setmode 1`: Enables the combo point mode.
1. `/setmode 2`: Enables the energy mode.
1. `/setmode 3`: Enables the rage mode.
1. `/setmode 4`: Enables the mode indicating when your character is in combat.

# Caveats

1. The current implementation of StatCast was only tested on a single-monitor setup. Multiple-monitor setups may be less reliable.
1. WoW must be in full-screen mode for StatCast to work properly.
1. Single-zone LIFX lights may work for HP, Energy, and Rage modes, but this has not been tested.

# How does it work?

StatCast is comprised of two main components: a WoW addon and a Python script.

The addon writes two pixels on the screen that encode the mode and corresponding value, e.g. "energy" and "72". The Python script reads these values from the screen and communicates with the LIFX lights.

# Future improvements

1. Support more smart light brands (e.g. Hue)
1. Multi-monitor setup support
1. Improve process for dependency installations
1. More modes (e.g. mana, chi)

# Questions, requests, or issues?

Feel free to submit a pull request or email me at minokar60@gmail.com.
