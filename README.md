# Random-Slot-Generator
Generates a random slot, bet size and spin count (supports weighted bet sizes and spin counts)

# Setup:
 This is a python script, so it requires python (tested with 3.13.3).
 It also requires the following modules:
 keyboard
 random

 module setup should be automatic with 
 pip install -r requirements.txt


# Configuration:
You can add new slots in slots.txt
You can configure bet sizes in bet.txt
You can configure  spin count sizes in spincount.txt

Format is the left side being the outcome, right side being the weight.

While it isn't mandatory for the weights to divide by 100, it does make calculating percentages easier. If everything is set to the same weight, it will act as equal chance of each outcome happening.


# Notes: 
Due to global keyboard input checking, this script requires root to function in POSIX environments (such as Linux). As far as I know, there is no workaround for this, and you will be prompted to run the script as root if you try to run it non root.

Currently, the slots list is configured for Stake and includes 498 slots. I will occasionally update the list with new slot releases.
