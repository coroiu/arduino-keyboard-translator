# Arduino Keyboard Translator
This repository contains the host part of a keyboard emulator. Changes in switch-states are received over a serial interface and transformed into uinput events.
On second thought, the solution here might not be the best. If I had to re-do it, I probably would have just sent over the changes, instead of all the button states.

## Why
This was made as part of a custom-built arcade cabinet.
