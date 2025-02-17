# Timeloop - with timeout
**This modified version is modified to take timeout as a decorator arg plus arguments passed to the jobs.**
modifications by tekn0ir

## Release of new version
Create tarball
```shell
python setup.py sdist
```

Create a release on github: https://github.com/tekn0ir/timeloop/releases
Upload the new version of the tarball to the release

## Install version
```shell
python -m pip install https://github.com/tekn0ir/timeloop/releases/download/v1.0.2/timeloop-1.0.2.tar.gz --upgrade
```
 
# Timeloop
Timeloop is a service that can be used to run periodic tasks after a certain interval.

Each job runs on a separate thread and when the service is shut down, it waits till all tasks currently being executed are completed.

Inspired by this blog [`here`](https://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/)

## Installation
```sh
pip install timeloop
```

## Writing jobs
```python
import time

from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

@tl.job(interval=timedelta(seconds=2), timeout=timedelta(milliseconds=500))
def sample_job_every_2s():
    print "2s job current time : {}".format(time.ctime())
sample_job_every_2s()

@tl.job(interval=timedelta(seconds=5), timeout=timedelta(milliseconds=500))
def sample_job_every_5s():
    print "5s job current time : {}".format(time.ctime())
sample_job_every_5s()

@tl.job(interval=timedelta(seconds=10), timeout=timedelta(milliseconds=500))
def sample_job_every_10s():
    print "10s job current time : {}".format(time.ctime())
sample_job_every_10s()
```

## Writing jobs with arguments
```python
@tl.job(interval=timedelta(seconds=5), timeout=timedelta(milliseconds=500))
def sample_job(idx):
    print "Task id: {} | time: {}".format(idx, time.ctime())
# example: queue jobs with different ids
for id in range(1, 3):
	sample_job(id)
```

## Start time loop in separate thread
By default timeloop starts in a separate thread.

Please do not forget to call ```tl.stop``` before exiting the program, Or else the jobs wont shut down gracefully.

```python
tl.start()

while True:
  try:
    time.sleep(1)
  except KeyboardInterrupt:
    tl.stop()
    break
```

## Start time loop in main thread
Doing this will automatically shut down the jobs gracefully when the program is killed, so no need to  call ```tl.stop```
```python
tl.start(block=True)
```

## Author
* **Sankalp Jonna**

Email me with any queries: [sankalpjonna@gmail.com](sankalpjonna@gmail.com).
