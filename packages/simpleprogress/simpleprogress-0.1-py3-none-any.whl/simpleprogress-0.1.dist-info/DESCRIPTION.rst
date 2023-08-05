## simpleprogress

Simple progress indicator for python. Internally tracks time for updates.

```python
from simpleprogress import Progress

max_val = 100
p = Progress(max_val, poll_time=2.0) # default poll time is 1 second

for i in range(0, 100):

    if p.should_update:
        p.update(i)
        print(p.pretty_print())

    time.sleep(1)

```


