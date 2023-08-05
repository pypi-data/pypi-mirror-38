import errno
import json
import os
import subprocess
import uuid

import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy

jsonpickle_numpy.register_handlers()
import jsonpickle.ext.pandas as jsonpickle_pandas  # pylint: disable=E0611

jsonpickle_pandas.register_handlers()

import requests


class SLTool:  # pylint: disable=W0232
    # Execute command with subprocess.
    @staticmethod
    def execute(command, verbose=False):
        if verbose:
            print("Executing: {:s}".format(command))
        command_list = command.split(" ")
        result = subprocess.run(command_list, stdout=subprocess.PIPE,  # pylint: disable=E1101
                                stderr=subprocess.PIPE, universal_newlines=True)
        result.check_returncode()
        if verbose:
            print(result.stdout)
        return result.stdout

    # Install python library if missing. This is done by executing "pip3 install" in subprocess.
    @staticmethod
    def ensure(name, version=None, update=False, verbose=False):
        if verbose:
            print("Ensuring {:s}".format(name))
        args = ["pip3", "install"]
        if version is not None:
            args.append(name.strip() + "==" + version.strip())
        else:
            if update:
                args.append("-U")
            args.append(name.strip())
        result = subprocess.run(args, stdout=subprocess.PIPE,  # pylint: disable=E1101
                                stderr=subprocess.PIPE, universal_newlines=True)
        result.check_returncode()
        if verbose:
            print(result.stdout)
        return result.stdout

    # Get random path under temporary directory root.
    @staticmethod
    def get_random_path(tmp_root):
        tmp_path = os.path.join(tmp_root, uuid.uuid4().hex)
        while True:
            try:
                os.makedirs(tmp_path)
                break
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                tmp_path = os.path.join(tmp_root, uuid.uuid4().hex)
        return tmp_path

    # Encode object with jsonpickle.
    @staticmethod
    def encode(obj):
        return jsonpickle.encode(obj)

    # Decode object with jsonpickle.
    @staticmethod
    def decode(obj):
        return jsonpickle.decode(obj)

    # Get a document that will be dropped to preserve lineage property for ultra task.
    @staticmethod
    def get_drop_doc():
        return {"snaplogic_flag": "drop"}

    # Download file using wget.
    @staticmethod
    def download_file(url, out_path):
        resp = requests.get(url, stream=True)
        with open(out_path, "wb") as out_file:
            for chunk in resp.iter_content(chunk_size=4096):
                if chunk:
                    out_file.write(chunk)

    # Send request to ultra task.
    @staticmethod
    def ultra(url, token=None, data=None, fmt="json"):
        headers = {"Content-Type": "application/json"}
        if data is None:
            data = {}
        if token is not None:
            token = token.strip()
            if token.startswith("Authorization: Bearer"):
                token = token[21:]
            elif token.startswith("Bearer"):
                token = token[6:]
            headers["Authorization"] = "Bearer {:s}".format(token.strip())
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        if fmt == "json":
            return resp.json()
        elif fmt == "text":
            return resp.text
        else:
            return resp

    # Send request to triggered task.
    @staticmethod
    def trigger(url, token=None, data=None, params=None, fmt="json"):
        headers = {"Content-Type": "application/json"}
        if data is None:
            data = []
        if params is None:
            params = {}
        if token is not None:
            token = token.strip()
            if token.startswith("Authorization: Bearer"):
                token = token[21:]
            elif token.startswith("Bearer"):
                token = token[6:]
            headers["Authorization"] = "Bearer {:s}".format(token.strip())
        if data is not None and len(data) != 0:
            resp = requests.post(url, headers=headers, data=json.dumps(data), params=params)
        else:
            resp = requests.get(url, headers=headers, params=params)
        if fmt == "json":
            return resp.json()
        elif fmt == "text":
            return resp.text
        else:
            return resp
