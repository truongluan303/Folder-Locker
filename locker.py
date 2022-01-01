import base64
import json
import random
import os
import subprocess
from sys import platform
from typing import List


class LockerManager:

    _DATA_FILE = ".data.json"        # the name of the data json file
    _LOCKERS_FOLDER = ".lockers"     # the folder containing all hidden folders


    class Locker:
        """ save the data needed to access the hidden folder """

        def __init__(self, name: str, path: str, password: str) -> None:
            """
            :param name:        the name of the locker saved by the user
            :param path:        the path to the folder
            :param password:    the encrypted version of the password
            """
            self.name = name
            self.path = path
            self.password = password



    def __init__(self) -> None:
        self.lockers = dict()

        path = LockerManager._DATA_FILE
        if not os.path.exists(path) or os.stat(path).st_size == 0:
            return

        with open(LockerManager._DATA_FILE, "r") as file:
            lockers = json.load(file)

        for locker in lockers:
            name = locker["name"]
            path = locker["path"]
            password = locker["password"]
            self.lockers[name] = self.Locker(name, path, password)



    def save(self) -> None:
        """
        save all the current lockers to a json file
        """
        if len(self.lockers) == 0:
            return

        # convert each locker object in the list to dictionary
        lockers = list()
        for locker in self.lockers.values():
            lockers.append(locker.__dict__)

        # convert the lockers to json format
        objs = json.dumps(lockers)

        # write the saved data to file
        with open(LockerManager._DATA_FILE, "w") as file:
            for line in objs:
                file.write(line)

        # hide the file if in Windows
        if platform == "win32":
            subprocess.check_call(["attrib", "+H", LockerManager._DATA_FILE])



    def open_locker(self, name: str, password: str) -> tuple:
        """
        open a locker
        :param name:        the name of the locker to be opened
        :param password:    the password to access the locker
        :return: a tuple of a boolean to indicate whether the locker was
                 successfully opened and a message
        """
        if name not in self.lockers:
            return False, f"Unable to find the locker with name {name}"
        locker = self.lockers[name]

        if self.check_password(name, password):
            if platform == "win32":
                subprocess.check_call(["start", locker.path])
            elif platform == "linux" or platform == "linux2":
                subprocess.check_call(["xdg-open", locker.path])

            return True, "Access Granted"
        return False, f"Wrong password for locker with name {name}"



    def add_locker(self, name: str, password: str) -> bool:
        """
        create a new locker
        :param name:        the name for the new locker
        :param password:    the password to access the locker
        :return: true if the given name has not been taken
        """
        # return false if the given locker's name already exists
        if name in self.lockers:
            return False

        # generate a random id as the new folder's name
        rand_id = ""
        for i in range(10):
            rand_id += str(random.randint(0, 9))
        randname = f".locker{rand_id}"
        path = f"{LockerManager._LOCKERS_FOLDER}/{randname}"

        # create the folder
        if not os.path.exists(LockerManager._LOCKERS_FOLDER):
            os.mkdir(LockerManager._LOCKERS_FOLDER)

        os.mkdir(path)
        if platform == "win32":
            subprocess.check_call(["attrib", "+H", LockerManager._LOCKERS_FOLDER])
            subprocess.check_call(["attrib", "+H", path])

        # encode the given password
        e_pw = self.__encode_password(password)

        # map the name to the new locker created and return true
        self.lockers[name] = self.Locker(name, path, e_pw)
        return True



    def remove_locker(self, name) -> bool:
        """
        remove a locker
        :param name: the name of the locker to be removed
        :return: true if the given name exists
        """
        if name not in self.lockers:
            return False
        os.rmdir(self.lockers[name].path)
        del self.lockers[name]
        self.save()
        if len(self.lockers) == 0:
            os.remove(LockerManager._DATA_FILE)
        return True



    def get_lockers_names(self) -> List[str]:
        """
        get all the names of the lockers
        :return: the list of all lockers' names
        """
        result = list()
        for locker_name in self.lockers.keys():
            result.append(locker_name)
        return result



    def change_name(self, current_name: str, new_name: str) -> bool:
        """
        change the name of an existed locker
        :param current_name:    the current name of the locker
        :param new_name:        the new name
        :return: false if the name cannot be found
        """
        if current_name not in self.lockers:
            return False
        locker = self.lockers[current_name]
        locker.name = new_name
        return True



    def change_password(self, current_name: str, new_password: str) -> bool:
        """
        change the password of a locker
        :param current_name:    the name of the locker
        :param new_password:    the new password for the given locker
        :return: true if the name is valid and the password is successfully changed
        """
        if current_name not in self.lockers:
            return False
        locker = self.lockers[current_name]
        locker.password = self.__encode_password(new_password)
        return True



    def check_password(self, name: str, password: str) -> bool:
        """
        check if the given password is correct for a specific locker
        :param name:        name of the locker to check password
        :param password:    the password to be checked
        :return: true if the password matches with that of the locker
        """
        locker = self.lockers[name]
        return locker.password == self.__encode_password(password)



    @staticmethod
    def __encode_password(password: str) -> str:
        """
        encode a string password
        :param password: the password to be encoded
        :return: the encoded version of the given password
        """
        encoded = base64.b64encode(password.encode("utf-8"))
        return str(encoded)



    @staticmethod
    def __decode_password(encoded_password: bytes) -> str:
        """
        decode an encoded password
        :param encoded_password: the given encoded password
        :return: the normal version of the given password
        """
        decoded = base64.b64decode(encoded_password).decode()
        return decoded
