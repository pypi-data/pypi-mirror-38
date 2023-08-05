import json
import logging
import importlib.machinery as imm
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from abc import ABCMeta, abstractmethod

logging.basicConfig(level=logging.INFO)


def setup_task_manager(config_file_path, task_shared_data):
    manager = TaskManager(config_file_path, task_shared_data)
    manager.setup()
    manager.execute_tasks()


class TaskManager:
    def __init__(self, config_file_path, task_shared_data):
        self.config = self.__config_file_parse(config_file_path)
        self.task_shared_data = task_shared_data
        self.driver = None
        self.tasks = list()

    def __config_file_parse(self, config_file_path):
        with open(config_file_path, 'r', encoding='utf-8_sig') as file:
            return json.load(file)

    def setup(self):
        self.driver = self.__setup_driver()
        self.tasks = self.__setup_tasks()

    def __setup_driver(self):
        driver = Driver(self.config["driver"])
        return driver.setup()

    def __setup_tasks(self):
        tasks = list()
        for task in self.config["tasks"]:
            if task["action"] == "link":
                tasks.append(LinkTask(task, self.driver, self.task_shared_data))
            elif task["action"] == "input":
                tasks.append(InputTask(task, self.driver, self.task_shared_data))
            elif task["action"] == "shared_input":
                tasks.append(SharedInputTask(task, self.driver, self.task_shared_data))
            elif task["action"] == "enter":
                tasks.append(EnterTask(task, self.driver, self.task_shared_data))
            elif task["action"] == "click":
                tasks.append(ClickTask(task, self.driver, self.task_shared_data))
            elif task["action"] == "custom":
                tasks.append(CustomTask(task, self.driver, self.task_shared_data))

        return tasks

    def execute_tasks(self):
        for task in self.tasks:
            task.execute()


class Driver:
    def __init__(self, driver):
        self.driver = driver

    def setup(self):
        if self.driver["name"] == 'webdriver':
            if self.driver["browser"] == 'firefox':
                return webdriver.Firefox()
            elif self.driver["browser"] == 'chrome':
                return webdriver.Chrome()
        else:
            raise ValueError("Unsupported driver {0}".format(self.driver))


class Task:
    def __init__(self, task, driver, shared_data):
        self.driver = driver
        self.shared_data = shared_data
        self.description = task["description"]
        self.action = task["action"]
        self.before_sleep = int(task["before_sleep"]) if "before_sleep" in task else 1
        self.after_sleep = int(task["after_sleep"]) if "after_sleep" in task else 1
        self.before_implicitly_wait = int(task["before_implicitly_wait"]) if "before_implicitly_wait" in task else 0
        self.after_implicitly_wait = int(task["after_implicitly_wait"]) if "after_implicitly_wait" in task else 0

    def execute(self):
        self.before_execute()
        self.run()
        self.after_execute()

    def before_execute(self):
        logging.info("[>>>> Start task] {}".format(self.description))
        sleep(self.before_sleep)
        self.driver.implicitly_wait(self.before_implicitly_wait)

    def run(self):
        pass

    def after_execute(self):
        logging.info("[<<<< End task] {}".format(self.description))
        sleep(self.after_sleep)
        self.driver.implicitly_wait(self.after_implicitly_wait)

    def set_shared_data(self, key, value):
        self.shared_data.attributes[key] = value

    def get_shared_data(self, key):
        return self.shared_data.attributes[key]


class LinkTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.url = task["params"]["url"]

    @abstractmethod
    def run(self):
        self.driver.get(self.url)


class InputTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.selector_type = task["params"]["type"]
        self.path = task["params"]["path"]
        self.data = task["params"]["data"]

    @abstractmethod
    def run(self):
        if self.selector_type == "xpath":
            self.driver.find_element_by_xpath(self.path).send_keys(self.data)
        elif self.selector_type == "id":
            self.driver.find_element_by_id(self.path).send_keys(self.data)


class SharedInputTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.selector_type = task["params"]["type"]
        self.path = task["params"]["path"]
        self.data = task["params"]["data"]

    @abstractmethod
    def run(self):
        if self.selector_type == "xpath":
            self.driver.find_element_by_xpath(self.path).send_keys(self.get_shared_data(self.data))
        elif self.selector_type == "id":
            self.driver.find_element_by_id(self.path).send_keys(self.get_shared_data(self.data))


class EnterTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.selector_type = task["params"]["type"]
        self.path = task["params"]["path"]

    @abstractmethod
    def run(self):
        if self.selector_type == "xpath":
            self.driver.find_element_by_xpath(self.path).send_keys(Keys.RETURN)
        elif self.selector_type == "id":
            self.driver.find_element_by_id(self.path).send_keys(Keys.RETURN)


class ClickTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.selector_type = task["params"]["type"]
        self.path = task["params"]["path"]


    @abstractmethod
    def run(self):
        if self.selector_type == "xpath":
            self.driver.find_element_by_xpath(self.path).click()
        elif self.selector_type == "id":
            self.driver.find_element_by_id(self.path).click()


class CustomTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.type = task["params"]["type"]
        self.script_file = task["params"]["script_file"]
        self.class_name = task["params"]["class_name"]

    @abstractmethod
    def run(self):
        if self.type == "python":
            datam = imm.SourceFileLoader(self.class_name, self.script_file).load_module()
            cls = getattr(datam, self.class_name)
            custom = cls(self.driver, self.shared_data)
            custom.run()
