# colourz
Print in colour, with no extra charge!

## Installation

`$ pipenv install colourz`

## Usage

```python
import colourz

# Print in bold text
print(colourz.bold("Bold text"))

# Print text in red
print(colourz.normal("Red text", "RED"))

# Print text in bold red
print(colourz.bold("Bold red text", "RED"))

# Use Bullets when waiting on a long task
import time

def main():
    s = colourz.Bullets()
    print("Doing long task...")
    s.start()
    long_task()
    s.stop()
    print("Success!")

# CAUTION: As Bullets is threaded, we need to watch out for exceptions
def long_task():
    raise LongTaskError

def main():
    s = colourz.Bullets()
    print("Doing long task...")
    s.start()
    try:
        long_task()
        msg = "Success!"
    except LongTaskError:
        msg = "Fail!"
    finally:
        s.stop()
        print(msg)
```
