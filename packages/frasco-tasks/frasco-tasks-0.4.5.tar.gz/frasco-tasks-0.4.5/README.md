# Frasco-Tasks

Adds the possibility to run actions in the background using [celery](http://www.celeryproject.org/).

## Installation

    pip install frasco-tasks

## Setup

Feature name: tasks

Options:

 - *broker_url*: celery's broker url
 - *result_backend*: celery's result backend
 - *schedule*: see below
 - all other options will be added to the celery config

*broker_url* is optional and if not provided will be localhost. However, if
[Frasco-Redis]() is available, it will automatically use the same redis server.
When the broker is automatically selected, the result backend will also use
the same redis server.

## Actions

### enqueue

The *enqueue* action allows you to enqueue actions to be run later by a worker.
These actions will be run out of a request context and thus cannot depend on it.

Options:

 - *action*: the action name (default option)
 - all other options will be forwarded to the enqueued action

## Running a worker

The feature provides a *worker* command which allows to start a worker. Multiple
workers can be started if the work is heavy.

    $ frasco worker

Note that a worker is automatically started with *frasco run*.

## Scheduling

You can schedule task to be executed at certain times using Celery Beat.
The *schedule* option is a hash where keys are action names and their value
a [crontab](http://en.wikipedia.org/wiki/Cron) schedule.

In the following example, the action named *my_action* will be executed every
30 minutes.

    features:
      - tasks:
          schedule:
            my_action: */30 * * * *

## Data serialization

The data will be serialied to json when enqueued. This can create problems when
passing objects. To ensure that an object is encoded and decoded properly to/from
json, define the `__taskdump__` and `__taskload__` method on your objects.

`__taskdump__` must return a tuple containing the class name and a state object
which must be JSON compatible.

`__taskload__` is a class method which takes as argument the state object and must
return an object.

```python
class MyObject(object):
    def __init__(self, id):
        self.id = id

    def __taskdump__(self):
        return 'MyObject', self.id

    @classmethod
    def __taskload__(cls, id):
        return MyObject(id)
```