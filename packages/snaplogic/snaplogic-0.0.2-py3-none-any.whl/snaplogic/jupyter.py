import base64
import decimal
import errno
import json
import os
import shutil
import struct
import sys
import time
import traceback
import urllib
import uuid
from datetime import datetime
from io import StringIO
from multiprocessing import Process, Queue

import clipboard
import ipywidgets as widgets
import numpy
import requests
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Util import Counter
from Crypto.Util.number import long_to_bytes, bytes_to_long
from IPython import get_ipython
from IPython.display import clear_output
from IPython.display import display, HTML
from IPython.utils.py3compat import str_to_bytes, bytes_to_str
from ipywidgets import Layout

"""
This module provides interface integrating Jupyter Notebook with SnapLogic platform.
"""


class SnapLogic(object):
    ENV_ELASTIC = os.environ.get("POD_URL", "https://elastic.snaplogic.com/")

    ENCRYPTION_KEY_BLOCK_SIZE = 16

    SNAP_CLASS_ID_PYTHON = "com-snaplogic-snaps-mlcore-remotepythonscript"

    SCRIPT_CELL_HEADER = "##### The first cell with this header will be saved and published. " \
                         "Do not remove or modify this header. #####\\n"

    # Message
    MSG_LOGIN_SUCCESS = "Logged in successfully!\nExecute \"sl.display_main_menu()\" to start the main menu."
    MSG_CONNOT_FIND_LOGIN_INFO = "Cannot find login information. Please use \"SnapLogic(username, password).\""
    MSG_LOGIN_FAIL = "Failed to log in. Please try again."
    MSG_CANNOT_FIND_SNAP = "Cloud pipeline has been changed. Please \"Copy Info\" and \"Paste Info\" again."
    MSG_SNAPLEX_NOT_VALID = "Cannot fetch Snaplex info. " \
                            "Please try validating this pipeline on SnapLogic and copy the Snap info again."
    MSG_CANNOT_FIND_AVAI_CC = "Cannot find available JCC. Please check the status of the Snaplex."

    # API
    API_USER_INFO = "/api/1/rest/public/users/"
    API_TREE = "/api/1/rest/asset/tree/"
    API_LIST_PIPELINE = "/api/1/rest/asset/list/"
    API_LIST_PLEX = "/api/1/rest/plex/org/"
    API_GET_PIPELINE = "/api/1/rest/pipeline/fetch/"
    API_UPDATE_PIPELINE = "/api/2/{0}/rest/pipeline/update/"
    API_GET_CCINFO = "/api/1/rest/slserver/ccinfo/"
    API_PIPELINE_PREPARE = "/api/1/rest/pipeline/prepare/"
    API_GET_RT = "/api/2/{0}/rest/pm/runtime/"
    API_GET_PREVIEW_DATA = "/api/1/rest/slfs/{0}/fsx/"

    # Layout and Style
    CHAR_WID = 7.5
    LAY_100_WID = Layout(width="100%")
    LAY_100_WID_100_HEI = Layout(width="100%", height="100%")
    LAY_70_WID = Layout(width="70%")
    LAY_98_WID = Layout(width="98%")
    LAY_98_WID_100_HEI = Layout(width="98%", height="100%")
    LAY_50_WID = Layout(width="50%")
    LAY_BUTTON = Layout(width="98%")
    LAY_BUTTON_HIDDEN = Layout(width="98%", visibility="hidden")
    LAY_LOGIN = Layout(width="240px")

    def __init__(self, username=None, password=None, env=None):
        """
        Initialize the session. If not all required parameters are provided, log in form will be rendered.
        """
        self.__login_info = {}
        self.__snap_info = {}
        self.__ui = {}
        self.__js_script = {}
        self._secret_key = None
        self.__python_script = None
        self.input_data = None
        self.output_data = None
        self.error_data = None
        self.console_date = None
        self.ipython = get_ipython()
        self.login(env, username, password)

    def display_login_form(self, env, username, password):
        """
        Render log in form.
        """
        env_input = widgets.Text(description="Environment", value=env, layout=self.LAY_LOGIN)
        username_input = widgets.Text(description="Username", value=username, layout=self.LAY_LOGIN)
        password_input = widgets.Password(description="Password", value=password, layout=self.LAY_LOGIN)
        login_button = widgets.Button(description="Log in")

        def on_login_button_clicked(_button):
            self.login(env_input.value, username_input.value, password_input.value)

        login_button.on_click(on_login_button_clicked)
        username_input.on_submit(on_login_button_clicked)
        password_input.on_submit(on_login_button_clicked)

        self.execute_js("assets/login.html")

        display(env_input, username_input, password_input, login_button)

        return env_input, username_input, password_input

    def render_button_group(self):
        """
        Render buttons in the main menu.
        """
        paste_info_button = widgets.Button(description="Paste Info", layout=self.LAY_BUTTON)
        paste_info_button.add_class("snaplogic-menu-btn")
        paste_info_button.add_class("snaplogic-paste-info-btn")

        def on_paste_info_button_clicked(_button):
            """
            Set information from clipboard to dropdown boxes.
            """
            info = clipboard.paste()
            try:
                info = json.loads(info)
                self.__snap_info["org"] = info["org"]
                self.__login_info["org"] = info["org"]
                self.__snap_info["org_snode_id"] = info["org_snode_id"]
                self.__login_info["org_snode_id"] = info["org_snode_id"]
                self.__snap_info["proj"] = info["proj"]
                self.__snap_info["pipe_label"] = info["pipe"]
                self.__snap_info["pipe_snode_id"] = info["pipe_snode_id"]
                self.__snap_info["snap_label"] = info["snap_label"]
                self.__snap_info["snap_id"] = info["snap_id"]
                self.__snap_info["plex"] = info["plex"]
                self.__snap_info["plex_path_id"] = info["plex_path_id"]
            except Exception:  # pylint: disable=W0703
                self.__snap_info = {}
                self.log("Snap Not Linked", "danger")
                self.execute_js("assets/snap-info-alert.html")
                return

            self.execute_js("assets/paste-info.html",
                            (base64.b64encode(self.__snap_info["org"].encode("utf-8")).decode("utf-8"),
                             base64.b64encode(self.__snap_info["proj"].encode("utf-8")).decode("utf-8"),
                             base64.b64encode(self.__snap_info["pipe_label"].encode("utf-8")).decode("utf-8"),
                             base64.b64encode(self.__snap_info["snap_label"].encode("utf-8")).decode("utf-8"),
                             base64.b64encode(self.__snap_info["plex"].encode("utf-8")).decode("utf-8")))

            self.log("Linked", "success")

        paste_info_button.on_click(on_paste_info_button_clicked)
        self.__ui["paste_info_button"] = paste_info_button

        load_python_script_button = widgets.Button(description="Fetch Script", layout=self.LAY_BUTTON_HIDDEN)
        load_python_script_button.add_class("snaplogic-menu-btn")
        load_python_script_button.add_class("snaplogic-load-script-btn")

        def on_load_script_button_clicked(_button):
            """
            Load Python script from linked Python Snap from SnapLogic platform.
            """
            selected_snap = self.__snap_info["snap_id"]
            selected_pipe = self.__snap_info["pipe_snode_id"]
            try:
                self.log("Fetching", "info")
                pipe_obj = self.get_pipeline(selected_pipe)
            except Exception:  # pylint: disable=W0703
                self.log("Failed to Fetch", "danger", "Failed to Fetch Script",
                         "Please check the internet connection and verify that the Snap exists.")
                return
            snap_map = pipe_obj["snap_map"]
            if selected_snap not in snap_map:
                self.log("Snap Not Found", "danger", "Failed to Find Snap",
                         "Please verify that the Snap exists in the pipeline.")
                return
            python_snap_obj = snap_map[selected_snap]
            python_script = python_snap_obj["property_map"]["settings"]["editable_content"]["value"]
            self.create_script_cell(python_script)
            self.log("Fetched", "success")

        load_python_script_button.on_click(on_load_script_button_clicked)
        self.__ui["load_python_script_button"] = load_python_script_button

        save_script_button = widgets.Button(description="Save Script", layout=self.LAY_BUTTON_HIDDEN)
        save_script_button.add_class("snaplogic-menu-btn")
        save_script_button.add_class("snaplogic-save-script-btn")

        def on_save_script_button_clicked(_button):
            """
            Locally save the script.
            """
            self.log("Saving", "info")
            self.export_script()
            self.log("Saved", "success")

        save_script_button.on_click(on_save_script_button_clicked)
        self.__ui["save_script_button"] = save_script_button

        publish_button = widgets.Button(description="Publish", layout=self.LAY_BUTTON_HIDDEN)
        publish_button.add_class("snaplogic-menu-btn")
        publish_button.add_class("snaplogic-menu-critical-btn")
        publish_button.add_class("snaplogic-publish-btn")

        def on_publish_button_clicked(_button):
            """
            Publish script to linked Python Snap on SnapLogic platform.
            """
            self.log("Publishing", "info")
            python_script = self.get_script()
            if python_script is None or len(python_script.strip()) == 0:
                self.log("Script Not Found", "danger", "Failed to Find Script", "Please save the script and try again.")
                return
            try:
                self.update_pipeline()
            except Exception:  # pylint: disable=W0703
                self.log("Failed to Publish", "danger", "Failed to Publish Script",
                         "Please check the internet connection and try again.")
                return
            self.log("Published", "success")

        publish_button.on_click(on_publish_button_clicked)
        self.__ui["publish_button"] = publish_button

        cloud_validate_button = widgets.Button(description="Cloud Validate", layout=self.LAY_BUTTON_HIDDEN)
        cloud_validate_button.add_class("snaplogic-menu-btn")
        cloud_validate_button.add_class("snaplogic-menu-critical-btn")
        cloud_validate_button.add_class("snaplogic-publish-and-validate-btn")

        def on_cloud_val_button_clicked(_button):
            """
            Publish script to linked Python Snap on SnapLogic platform and validate.
            Preview input, output and error will be fetched and rendered inside the notebook.
            """
            self.log("Publishing", "info")
            python_script = self.get_script()
            if python_script is None or len(python_script.strip()) == 0:
                self.log("Script Not Found", "danger", "Failed to Find Script", "Please save the script and try again.")
                return
            python_snap_id = self.__snap_info["snap_id"]
            try:
                pipe_old = self.update_pipeline()
            except Exception:  # pylint: disable=W0703
                self.log("Failed to Publish", "danger", "Failed to Publish Script"
                                                        "Please check the internet connection and try again.")
                return
            prev_snap_id, prev_snap_output_view_id = self.get_prev_snap(python_snap_id, pipe_old)
            default_plex_rt_path_id = self.__snap_info["plex_path_id"]
            default_plex_label = self.plex_rt_path_id_to_label(default_plex_rt_path_id)
            self.log("Connecting", "info")
            try:
                cc_info_data = self.get_ccinfo(default_plex_rt_path_id)
            except Exception:  # pylint: disable=W0703
                self.log("Failed to Connect", "danger", "Failed to Connect to Snaplex",
                         "Please check the internet connection and verify that the Snaplex is running.")
                return
            encryption_keys = self.generate_encryption_keys(cc_info_data)

            self.log("Validating", "info")
            try:
                prepare_resp = self.prepare_pipeline(default_plex_rt_path_id, default_plex_label, encryption_keys,
                                                     use_cache=False)
            except Exception:  # pylint: disable=W0703
                self.log("Failed to Validate", "danger", "Failed to Validate Pipeline",
                         "Please check the internet connection and verify that the Snaplex is running.")
                return
            rt_id = prepare_resp["runtime_id"]

            sleep_count = 0
            while True:
                time.sleep(1)
                try:
                    rt = self.get_rt(rt_id)
                except Exception:  # pylint: disable=W0703
                    self.log("Failed to Validate", "danger", "Failed to Validate Pipeline",
                             "Please check the internet connection and verify that the Snaplex is running.")
                    return
                state = rt["state"]
                self.log(state, "success" if state == "Completed" else "info")
                if state in ["Completed", "Failed", "Stopped"]:
                    break
                sleep_count += 1
                if sleep_count == 600:
                    self.log("Timeout", "danger", "Timeout",
                             "The validation takes longer than expected. " +
                             "Please try validating in the designer and try again.")
                    return

            snap_map = rt["snap_map"]

            input_data = self.get_preview_data_helper(snap_map, prev_snap_id, prev_snap_output_view_id, "input")
            if input_data is None:
                return

            output_data = self.get_preview_data_helper(snap_map, python_snap_id, "output0", "output")
            if output_data is None:
                return

            console_data = "Please add the second output view of the Snap to get console data."
            if len(snap_map[python_snap_id]["suggest_uris"]["output"]) > 0:
                for output_view_id in snap_map[python_snap_id]["suggest_uris"]["output"]:
                    if output_view_id != "output0":
                        console_data = self.get_preview_data_helper(snap_map, python_snap_id, output_view_id, "console")
                        if console_data is None:
                            return
                        if len(console_data) == 0:
                            console_data = ""
                        else:
                            console_data = console_data[0]["content"]
                        break

            error_data = self.get_preview_data_helper(snap_map, python_snap_id, "error0", "error")
            if error_data is None:
                return

            self.input_data = input_data

            if state == "Completed":
                self.log("Completed", "success")
            else:
                self.log("Completed (Error)", "success")

            self.render_preview_data(input_data, output_data, error_data, console_data)

        cloud_validate_button.on_click(on_cloud_val_button_clicked)
        self.__ui["cloud_validate_button"] = cloud_validate_button

        local_validate_button = widgets.Button(description="Local Validate", layout=self.LAY_BUTTON_HIDDEN)
        local_validate_button.add_class("snaplogic-menu-btn")
        local_validate_button.add_class("snaplogic-local-validate-btn")

        def on_local_val_button_clicked(_button):
            """
            Locally validate the script against input fetched by cloud validation.
            """
            python_script = self.get_script()
            if python_script is None or len(python_script.strip()) == 0:
                self.log("Script Not Found", "danger", "Failed to Find Script", "Please save the script and try again.")
                return
            if self.input_data is None:
                self.log("Input Not Found", "danger", "Failed to Find Input",
                         "Please perform cloud validation before local validation.")
                return
            self.local_validate(self.input_data, python_script)

        local_validate_button.on_click(on_local_val_button_clicked)
        self.__ui["local_validate_button"] = local_validate_button

    def get_preview_data_helper(self, snap_map, snap_id, view_id, data_type):
        try:
            if snap_id is None:
                return []
            else:
                self.log("Fetching {:s}".format(data_type.capitalize()), "info")
                data_uri = snap_map[snap_id]["suggest_uris"]["output" if data_type != "error" else "error"][
                    view_id]["data_uris"][0]
                data = self.get_preview_data(data_uri)
                return self.decrypt_chunk(data)
            self.log("{:s} Fetched".format(data_type.capitalize()), "success")

        except IndexError:
            self.log("{:s} Fetched".format(data_type.capitalize()), "success")
            return []
        except Exception:  # pylint: disable=W0703
            self.log("Failed to Fetch {:s}".format(data_type.capitalize()), "danger",
                     "Failed to Fetch {:s} Preview Data".format(data_type.capitalize()),
                     "Please check the internet connection and verify that the Snaplex is running.")
            return None

    def local_validate(self, input_data, script):
        """
        Validate the script locally based on the input_data.
        """
        self.log("Prepared", "info")
        pipe_info = {"label": str(uuid.uuid4()), "instanceId": str(uuid.uuid4()),
                     "ruuid": str(uuid.uuid4()), "projectPath": str(uuid.uuid4())}
        queue = Queue()
        stdout_ori = sys.stdout
        stdout_result = Queue()
        process = SnapLogicExecutor(input_data, script, pipe_info, queue, stdout_result)
        process.daemon = True
        self.log("Started", "info")
        process.start()
        sys.stdout = stdout_ori
        output_data = queue.get()
        error_data = queue.get()
        self.render_preview_data(self.input_data, output_data, error_data, stdout_result.get())
        if len(error_data) > 0:
            self.log("Completed (Error)", "success")
        else:
            self.log("Completed", "success")

    def display_main_menu(self):
        """
        Render main menu.
        """
        if len(self.__login_info) == 0:
            print("Please log in using \"sl = SnapLogic()\" before starting the main menu.")
            return

        self.__ui = {}
        self.__python_script = None

        self.render_button_group()

        self.execute_js("assets/render-main-menu.html")

        with open(os.path.join(os.path.dirname(__file__), "assets/snaplogic_logo.png"), "rb") as image_file:
            image = image_file.read()
            snaplogic_logo = widgets.Image(value=image, format='png')
            snaplogic_logo.add_class("snaplogic-menu-logo")

        bottom_box = widgets.VBox([
            widgets.HBox([self.__ui["paste_info_button"],
                          self.__ui["load_python_script_button"],
                          self.__ui["save_script_button"],
                          self.__ui["publish_button"],
                          self.__ui["cloud_validate_button"],
                          self.__ui["local_validate_button"],
                          snaplogic_logo])], layout=self.LAY_100_WID)
        display(bottom_box)

    def login(self, env=None, username=None, password=None):
        """
        Log in using the given credential information.
        """
        self.logout()
        env = self.ENV_ELASTIC if env is None else env
        env = env if not env.endswith("/") else env[0:len(env) - 1]
        username = "" if username is None else username
        password = "" if password is None else password
        if len(username) == 0 or len(password) == 0:
            clear_output()
            self.display_login_form(env, username, password)
            print("Please enter username and password.")
        else:
            self.__login_info["env"] = env
            self.__login_info["username"] = username
            self.__login_info["password"] = password
            clear_output()
            error_msg = None
            try:
                my_info = self.get_my_info()
                self.__login_info["org_map"] = {}
                for org_obj in my_info["organizations"]:
                    self.__login_info["org_map"][org_obj["name"]] = org_obj["id"]
                print(self.MSG_LOGIN_SUCCESS)
            except Exception:  # pylint: disable=W0703
                self.__login_info = {}
                self.display_login_form(env, username, password)
                if error_msg is None:
                    error_msg = self.MSG_LOGIN_FAIL
                print(error_msg)

    def logout(self):
        self.__login_info = {}
        self.__ui = {}

    def is_login(self):
        if self.__login_info is None:
            raise Exception(self.MSG_CONNOT_FIND_LOGIN_INFO)

    def get_username(self):
        self.is_login()
        return self.__login_info["username"]

    def get_org(self):
        self.is_login()
        return self.__login_info["org"]

    def get_org_snode_id(self):
        self.is_login()
        return self.__login_info["org_snode_id"]

    def get_my_info(self):
        return self.get_user_info(self.get_username())

    def get_user_info(self, username):
        return self.api_request(self.API_USER_INFO + username)

    def get_tree(self):
        org = self.get_org()
        return self.api_request(self.API_TREE + org, {"perm_filter": "R"})["response_map"]

    def get_plexes(self, org):
        return self.api_request(self.API_LIST_PLEX + org)["response_map"]

    def get_preview_data(self, uri):
        return self.api_request(self.API_GET_PREVIEW_DATA.format(self.__login_info["org"]) + uri, resp_type="raw")

    def plex_rt_path_id_to_label(self, plex_runtime_path_id):
        plex_list = self.get_plexes(self.__login_info["org"])
        for plex in plex_list:
            if plex_runtime_path_id == plex["runtime_path_id"]:
                return plex["label"]
        raise Exception(self.MSG_SNAPLEX_NOT_VALID)

    def get_pipeline(self, snode_id):
        return self.api_request(self.API_GET_PIPELINE + snode_id, {"snap_history": "true", "include_rbin": "true"})[
            "response_map"]

    def get_ccinfo(self, runtime_path_id):
        return self.api_request(self.API_GET_CCINFO, {"runtime_path_id": runtime_path_id})["response_map"]

    def prepare_pipeline(self, runtime_path_id, runtime_label, encryption_keys, use_cache=False):
        pipe_snode_id = self.__snap_info["pipe_snode_id"]
        data = {
            "runtime_path_id": runtime_path_id,
            "runtime_label": runtime_label,
            "do_start": True,
            "async": True,
            "priority": 10,
            "queueable": False,
            "is_suggest": True,
            "flags": {
                "is_suggest": True,
                "use_cache": use_cache
            },
            "encryption_keys": encryption_keys
        }
        return self.api_request(self.API_PIPELINE_PREPARE + pipe_snode_id, method="POST", data=data)["response_map"]

    def api_request(self, api, params=None, method="GET", headers=None, data=None, resp_type="json"):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        self.is_login()
        url = self.__login_info["env"] + api
        if len(params) > 0 and url.endswith("/"):
            url = url[0:len(url) - 1]
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params,
                                auth=(self.__login_info["username"], self.__login_info["password"]))
        elif method == "POST":
            resp = requests.post(url, headers=headers, params=params, json=data,
                                 auth=(self.__login_info["username"], self.__login_info["password"]))
        resp.raise_for_status()
        if resp_type == "json":
            return resp.json()
        elif resp_type == "text":
            return resp.text
        elif resp_type == "raw":
            return resp.content

    def create_script_cell(self, script=''):
        """
        Create a new call with the given script.
        """
        encoded_code = bytes_to_str(base64.b64encode(str_to_bytes(script)))
        self.execute_js("assets/load-script.html", (self.SCRIPT_CELL_HEADER, encoded_code))

    def set_script(self, text):
        python_script = urllib.parse.unquote(text)  # pylint: disable=E1101
        if len(python_script.strip()) == 0:
            self.__python_script = None
            self.log("Script Not Found", "danger", "Failed to Find Script", "Please save the script and try again.")
        else:
            self.__python_script = python_script

    def get_script(self):
        return self.__python_script

    def export_script(self):
        """
        Render saved script in the UI and save internally in memory.
        """
        self.execute_js("assets/save-script.html", (self.SCRIPT_CELL_HEADER))

    def update_pipeline(self):
        """
        Publish script to the pipeline on SnapLogic platform.
        """
        update_map = {"create": {"snap": {}, "link": {}},
                      "delete": {"snap": [], "link": []},
                      "update": {"snap": {}, "link": {}, "render_map": {}, "pipeline": {}}}
        pipe_snode_id = self.__snap_info["pipe_snode_id"]
        pipe = self.get_pipeline(pipe_snode_id)
        snap_id = self.__snap_info["snap_id"]
        snap_map = pipe["snap_map"]
        if snap_id not in snap_map:
            raise Exception(self.MSG_CANNOT_FIND_SNAP)
        update_map["link_serial"] = pipe["link_serial"]
        update_map["update"]["render_map"] = pipe["render_map"]
        update_map["update"]["pipeline"]["info"] = pipe["property_map"]["info"]
        update_map["update"]["pipeline"]["input"] = pipe["property_map"]["input"]
        update_map["update"]["pipeline"]["output"] = pipe["property_map"]["output"]
        update_map["update"]["pipeline"]["error"] = pipe["property_map"]["error"]
        update_map["update"]["pipeline"]["settings"] = pipe["property_map"]["settings"]
        try:
            update_map["update"]["pipeline"]["instance_version"] = pipe["property_map"]["instance_version"] + 1
        except KeyError:
            update_map["update"]["pipeline"]["instance_version"] = pipe["instance_version"] + 1
        try:
            update_map["update"]["pipeline"]["snap_history"] = pipe["snap_history"]
        except KeyError:
            pass
        script_snap = snap_map[snap_id]
        script_snap["property_map"]["settings"]["editable_content"]["value"] = self.get_script()
        update_map["update"]["snap"][snap_id] = script_snap
        data = {"update_map": update_map}
        self.api_request(self.API_UPDATE_PIPELINE.format(self.get_org_snode_id()) + pipe_snode_id,
                         {"duplicate_check": "True"},
                         method="POST", data=data)
        return pipe

    def get_rt(self, rt_id):
        return self.api_request(self.API_GET_RT.format(self.get_org_snode_id()) + rt_id,
                                {"level": "detail", "is_suggest": True})["response_map"]

    def get_prev_snap(self, current_snap_id, pipe):
        link_map = pipe["link_map"]
        for link_id in link_map:
            link = link_map[link_id]
            src_view_id = link["src_view_id"]
            src_id = link["src_id"]
            dst_id = link["dst_id"]
            if dst_id == current_snap_id:
                return src_id, src_view_id
        return None, None

    def render_preview_data(self, input_data, output_data, error_data, console_data=""):
        self.input_data = input_data
        self.output_data = output_data
        self.error_data = error_data
        self.console_date = console_data

        input_data = json.dumps(input_data, cls=SnapLogicJsonEncoder)
        output_data = json.dumps(output_data, cls=SnapLogicJsonEncoder)
        error_data = json.dumps(error_data, cls=SnapLogicJsonEncoder)
        console_data = json.dumps({"content": console_data.strip()}, cls=SnapLogicJsonEncoder)

        self.execute_js("assets/show-preview-data.html", (base64.b64encode(input_data.encode("utf-8")).decode("utf-8"),
                                                          base64.b64encode(output_data.encode("utf-8")).decode("utf-8"),
                                                          base64.b64encode(error_data.encode("utf-8")).decode("utf-8"),
                                                          base64.b64encode(console_data.encode("utf-8")).decode(
                                                              "utf-8")))

    def log(self, text, style="", title=None, message=None):
        """
        Log info to the status bar.
        """
        self.execute_js("assets/show-status.html", (style, text))
        if style == "danger" and title is not None and message is not None:
            self.execute_js("assets/show-error-message.html", (title, message))

    def execute_js(self, path, params=None):
        """
        Load html/js file and execute.
        """
        path = os.path.join(os.path.dirname(__file__), path)
        if path not in self.__js_script:
            with open(path, "r") as script_file:
                self.__js_script[path] = script_file.read()
        if params is None:
            display(HTML(self.__js_script[path]))
        else:
            display(HTML(self.__js_script[path] % params))

    def generate_encryption_keys(self, cc_info_data=None):
        if cc_info_data is None:
            cc_info_data = {}
        self._secret_key = os.urandom(self.ENCRYPTION_KEY_BLOCK_SIZE)
        key_id = str(uuid.uuid4())
        encryption_keys = {'key_id': key_id}
        cc_keys = {}
        for cc_id, cc_info in cc_info_data.items():
            container_type = cc_info["container_type"]
            if container_type == "regular":
                cc_key_map = cc_info.get("info_map", {}).get("keys", {})
                for key_alias, key_info in cc_key_map.items():
                    keyvalue = key_info.get('key')
                    key_der = base64.b64decode(keyvalue)
                    key_actual = RSA.importKey(key_der)
                    cipher = PKCS1_OAEP.new(key_actual, hashAlgo=SHA256)
                    encrypted_key = base64.b64encode(cipher.encrypt(self._secret_key)).decode("utf-8")
                    cc_keys[cc_id] = {"alias": key_alias,
                                      "value": encrypted_key}
        if len(cc_keys) == 0:
            raise Exception(self.MSG_CANNOT_FIND_AVAI_CC)
        encryption_keys["cc"] = cc_keys
        return encryption_keys

    def decrypt_chunk(self, chunk):
        _key_id, _chunk_size, iv = struct.unpack('36si12s', chunk[:52])
        iv = bytes_to_long(iv)
        ciphertext = chunk[52:-16]
        auth_tag = bytes_to_long(chunk[-16:])
        cipher = AES_GCM(self._secret_key)
        return json.loads(cipher.decrypt(iv, ciphertext, auth_tag).decode("utf-8"))


class AES_GCM:  # pylint: disable=C0103
    def __init__(self, master_key):
        self.__aes_ecb = None
        self.__auth_key = None
        self.__master_key = None
        self.__pre_table = None
        self.prev_init_value = None
        self.change_key(master_key)

    def change_key(self, master_key):
        self.__master_key = master_key
        self.__aes_ecb = AES.new(self.__master_key, AES.MODE_ECB)
        self.__auth_key = bytes_to_long(self.__aes_ecb.encrypt(b'\x00' * 16))

        # precompute the table for multiplication in finite field
        table = []  # for 8-bit
        for i in range(16):
            row = []
            for j in range(256):
                row.append(AES_GCM.gf_2_128_mul(self.__auth_key, j << (8 * i)))
            table.append(tuple(row))
        self.__pre_table = tuple(table)

        self.prev_init_value = None  # reset

    def decrypt(self, init_value, ciphertext, auth_tag, auth_data=b''):
        if init_value >= (1 << 96):
            raise Exception("IV should be 96-bit")
        if auth_tag >= (1 << 128):
            raise Exception("Tag should be 128-bit")

        if auth_tag != self.__ghash(auth_data, ciphertext) ^ \
                bytes_to_long(self.__aes_ecb.encrypt(
                    long_to_bytes((init_value << 32) | 1, 16))):
            raise Exception("The authentication tag is invalid.")

        len_ciphertext = len(ciphertext)
        if len_ciphertext > 0:
            counter = Counter.new(
                nbits=32,
                prefix=long_to_bytes(init_value, 12),
                initial_value=2,
                allow_wraparound=True)
            aes_ctr = AES.new(self.__master_key, AES.MODE_CTR, counter=counter)

            if 0 != len_ciphertext % 16:
                padded_ciphertext = ciphertext + \
                                    b'\x00' * (16 - len_ciphertext % 16)
            else:
                padded_ciphertext = ciphertext
            plaintext = aes_ctr.decrypt(padded_ciphertext)[:len_ciphertext]

        else:
            plaintext = b''

        return plaintext

    def __ghash(self, aad, txt):
        len_aad = len(aad)
        len_txt = len(txt)

        # padding
        if 0 == len_aad % 16:
            data = aad
        else:
            data = aad + b'\x00' * (16 - len_aad % 16)
        if 0 == len_txt % 16:
            data += txt
        else:
            data += txt + b'\x00' * (16 - len_txt % 16)

        tag = 0
        assert len(data) % 16 == 0
        for i in range(len(data) // 16):
            tag ^= bytes_to_long(data[i * 16: (i + 1) * 16])
            tag = self.__times_auth_key(tag)
            # print 'X\t', hex(tag)
        tag ^= ((8 * len_aad) << 64) | (8 * len_txt)
        tag = self.__times_auth_key(tag)

        return tag

    def __times_auth_key(self, val):
        res = 0
        for i in range(16):
            res ^= self.__pre_table[i][val & 0xFF]
            val >>= 8
        return res

    @staticmethod
    def gf_2_128_mul(val1, val2):
        assert val1 < (1 << 128)
        assert val2 < (1 << 128)
        res = 0
        for i in range(127, -1, -1):
            res ^= val1 * ((val2 >> i) & 1)  # branchless
            val1 = (val1 >> 1) ^ ((val1 & 1) * 0xE1000000000000000000000000000000)
        assert res < 1 << 128
        return res


class SnapLogicExecutor(Process):
    def __init__(self, input_data, script, pipe_info, queue, stdout_result):
        Process.__init__(self)
        self.input_data = input_data
        self.script = script
        self.pipe_info = pipe_info
        self.local_scope = {}
        self.tmp_dir = None
        self.result = []
        self.error = []
        self.queue = queue
        self.stdout_result = stdout_result

    def run(self):
        stdout_ori = sys.stdout
        sys.stdout = stdout_buffer = StringIO()
        try:
            snaplogic_pipe = self.pipe_info
            self.local_scope["snaplogic_pipe"] = snaplogic_pipe

            self.tmp_dir = "/tmp/snaplogic_jupyter_notebook_integration_tmp_" + \
                           snaplogic_pipe["instanceId"] + "_" + \
                           snaplogic_pipe["ruuid"] + "_" + uuid.uuid4().hex + "/"
            while True:
                try:
                    os.makedirs(self.tmp_dir)
                    break
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                    self.tmp_dir = "/tmp/snaplogic_jupyter_notebook_integration_tmp_" + \
                                   snaplogic_pipe["instanceId"] + "_" + \
                                   snaplogic_pipe["ruuid"] + "_" + uuid.uuid4().hex + "/"

            snaplogic_pipe["tmp_root"] = self.tmp_dir
            self.local_scope["tmp_root"] = self.tmp_dir

            self.local_scope["snaplogic_pipe"] = snaplogic_pipe

            exec(self.script, self.local_scope)  # pylint: disable=W0122
            exec("snaplogic_init_result = snaplogic_init()", self.local_scope)  # pylint: disable=W0122

            snaplogic_init_result = self.local_scope["snaplogic_init_result"]
            self.append_result(snaplogic_init_result)

            for input_data_row in self.input_data:
                self.local_scope["snaplogic_input_data_row"] = input_data_row
                exec("snaplogic_row_result = snaplogic_process(snaplogic_input_data_row)",  # pylint: disable=W0122
                     self.local_scope)  # pylint: disable=W0122
                snaplogic_row_result = self.local_scope["snaplogic_row_result"]
                self.append_result(snaplogic_row_result)

            exec("snaplogic_final_result = snaplogic_final()", self.local_scope)  # pylint: disable=W0122
            snaplogic_final_result = self.local_scope["snaplogic_final_result"]
            self.append_result(snaplogic_final_result)

        except Exception as exception:  # pylint: disable=W0703
            error = [{"snaplogic_remote_python_execution_error": "Python script error: " + repr(
                exception) + " " + traceback.format_exc()}]
            self.append_result(error, "error")

        # Remove tmp directory.
        if self.tmp_dir.startswith("/tmp/snaplogic_jupyter_notebook_integration_tmp_"):
            shutil.rmtree(self.tmp_dir, ignore_errors=True)

        self.queue.put(self.result)
        self.queue.put(self.error)

        stdout_buffer.seek(0)
        self.stdout_result.put(str(stdout_buffer.read()))
        sys.stdout = stdout_ori

    def append_result(self, row_result, mode="result"):
        if mode == "result":
            output = self.result
        elif mode == "error":
            output = self.error
        if row_result is None:
            return
        if isinstance(row_result, dict):
            output.append(row_result)
        elif isinstance(row_result, list):
            for sub_row_result in row_result:
                if not isinstance(sub_row_result, dict):
                    raise Exception("The result can only be \"dict\" or \"list of dicts\".")
                output.append(sub_row_result)
        else:
            raise Exception("The result can only be \"dict\" or \"list of dicts\".")


class SnapLogicJsonEncoder(json.JSONEncoder):
    """
    This helper class is used to parse datetime.
    """

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, datetime):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (numpy.int_, numpy.intc, numpy.intp, numpy.int8, numpy.int16, numpy.int32, numpy.int64,
                            numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64)):
            return int(obj)
        if isinstance(obj, (numpy.float_, numpy.float16, numpy.float32, numpy.float64)):
            return float(obj)
        if isinstance(obj, (numpy.ndarray,)):
            return obj.tolist()
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)
