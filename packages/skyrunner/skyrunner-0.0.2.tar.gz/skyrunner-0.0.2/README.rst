Skyrunner
===========


Introduction
--------------
Skyrunner scrapes with json definition


Installation
--------------
.. code-block:: sh

   $ pip install skyrunner


How to use
--------------

1) Import skyrunner package at your project.
2) You define steps of scraping in json file.
3) You create class for share on scraping tasks and define `self.attributes = dict()` at constructor.

.. code-block:: python

   class TaskSharedData:
       def __init__(self):
           self.attributes = dict()

4) You call `skyrunner.setup_task_manager('scraping_steps_defined.json', TaskSharedData())` at your program.


sample of Scraping task definition json
------------------------------------------
.. code-block:: json

   {
      "description": "tasks description",
      "driver": {
        "name": "webdriver",
        "browser": "firefox"
      },
      "tasks": [
        {
          "description": "access to google",
          "action": "link",
          "params": {
            "url": "https://google.com"
          }
        },
        {
          "description": "search for mileshare",
          "action": "input",
          "params": {
            "type": "id",
            "path": "lst-ib",
            "data": "mileshare"
          }
        },
        {
          "description": "search(press the enter key)",
          "action": "enter",
          "params": {
            "type": "id",
            "path": "lst-ib"
          }
        }
      ]
    }

other support actions
=======================

- click

.. code-block:: json

    {
      "description": "click task",
      "action": "click",
      "params": {
        "type": "id or xpath",
        "path": "target id or xpath"
      }
    }

- custom

.. code-block:: json

   {
      "description": "custom task for complex process, update the shared data etc..",
      "action": "custom",
      "params": {
        "type": "python",
        "script_file": "custom python script(class) path",
        "class_name": "custom python class name"
      }
    }

- shared_input

.. code-block:: json

    {
      "description": "shared input task",
      "action": "shared_input",
      "params": {
        "type": "id or xpath",
        "path": "target id or xpath",
        "data": "dict key of shared data"
      }
    }
