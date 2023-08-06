# error-counter
Error Counter: Count error (e.g. network error) beyond process boundary, then issue fix command when exceeded threshold.

## How to use

```python:
import requests
from error_counter import Counter

# reboot system when error accumulate 3 times in a low
network_error_counter = Counter("/tmp/network_error.txt")

try:
	r = requests.post(somowhere, somewhat)
except requests.ConnectionError as e:
	network_error_counter.inc_error()

if not r is None:
	# send succeeded.
	network_error_counter.reset_error()
```

## Counter class
```python:
class Counter:
  def __init__(self, counterfile, reset_task="sudo reboot", reset_threshold=3):

#  counterfile: file name to use counter. The file is owned jointly by sevelal Counter beyond process boundary.

#  reset_task: shell command which is issued when error count is over the threshold.

#  reset_threshold: Threshold for reset_task.

  def inc_error(self):
  #	Increment error count then issue reset_task if count is over threshold

  def dec_error(self):
  # Decrement error count as 0

  def reset_error(self):
  # Reset error count as 0
```
## downloads
[![Downloads](https://pepy.tech/badge/error-counter)](https://pepy.tech/project/error-counter)
[![Downloads](https://pepy.tech/badge/error-counter/month)](https://pepy.tech/project/error-counter)
[![Downloads](https://pepy.tech/badge/error-counter/week)](https://pepy.tech/project/error-counter)

## history
- 0.1.0  2018.11.18  first version
