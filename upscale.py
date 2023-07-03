"""Performer Image Gigapixel Plugin"""
import json
import base64
import os
import re
import shutil
import sys
from io import BytesIO
from pathlib import Path
import requests
from gigapixel import Gigapixel, Scale, Mode
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from PIL import Image
import version_query
from config import STASH_URL, API_KEY, CUSTOM_MAPPED_FOLDER, CUSTOM_MAPPED_URL,\
     EXE_PATH, IMAGE_NAME, IMAGE_TYPES,\
     SCALE_MAPPING,\
     SET_TAG_IMAGE_GENERATION, OUTPUT_SUFFIX, VERSION
from log import *

# Global Gigapixel variables
scale_setting = []
scale_value = []
mode_setting = []
mode_value = []
# Global variable for performer tags to keep, with marker value
tag_ids = [None]


class MainGigapixel(Gigapixel):
    """
Gigapixel Sub Class to overide Gigapixel imported module class and add 
functionality to clear processed images.
As plugin will not work if there is any processed images in queue.
"""

    def __init__(self, executable_path: Path, output_suffix: str):
        log_instance = Logger()  # Create a new log instance
        self.my_log = log_instance # store the log object as an instance variable
        super().__init__(executable_path, output_suffix)  # Call parent __init__ method

    def start_gigapixel(self):
        """
        Function to start Gigapixel
        """
        app = MainGigapixel(EXE_PATH, OUTPUT_SUFFIX)
        app.restore().set_focus().maximize()
        if app is None:
            self.my_log.error(f"Cannot Start Gigapixel, check path variable & try again")  # added

class UpscaleWith:
    """
    Main plugin class
    """
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Connection": "keep-alive",
        "DNT": "1"
    }

    def __init__(self, STASH_URL, API_KEY):
        log_instance = Logger()  # Create a new log instance
        self.my_log = log_instance # store the log object as an instance variable
        self.STASH_URL = STASH_URL
        self.headers["ApiKey"] = API_KEY

    # If VERSION is empty, get the program version and write it to config.py
    def get_version(self):
        program_name = 'Topaz Gigapixel AI'
        program_version, install_location, exe_path = version_query.get_program_info(program_name)
        config_path = os.path.join(os.path.dirname(__file__), 'config.py')
        # Check if program version is already stored in config file and if not write values to config file
        version_found = False
        exe_path_found = False
        with open(config_path, 'r') as f:
            for line in f:
                if line.startswith('VERSION = '):
                    version = line.split('=')[1].strip()[1:-1] # Extract value between quotes
                    if version:
                        version_found = True
                    else:
                        version_found = False
                if line.startswith('EXE_PATH = '):
                    exe_path = line.split('=')[1].strip()[1:-1] # Extract value between quotes
                    if exe_path:
                        exe_path_found = True
                    else:
                        exe_path_found = False

        # If values not found in config file, query program for them
        if not version_found or not exe_path_found:
            program_version, install_location, exe_path = version_query.get_program_info(program_name)
            if not version_found:
                with open(config_path, 'r') as f:
                    lines = f.readlines()
                with open(config_path, 'w') as f:
                    for line in lines:
                        if line.startswith('VERSION = '):
                            line = f'VERSION = "{program_version.strip()}"\n'
                        f.write(line)
                self.my_log.info(f"The version of {program_name} is {program_version}. This has been written to config.py.")
            if not exe_path_found:
                with open(config_path, 'r') as f:
                    lines = f.readlines()
                with open(config_path, 'w') as f:
                    for line in lines:
                        if line.startswith('EXE_PATH = '):
                            line = f'EXE_PATH = "{exe_path.strip()}"\n'
                        f.write(line)
                self.my_log.info(f"The exe path for {program_name} is {exe_path}. This has been written to config.py.")
        else:
            program_version = version

        mode = None
        # Check if the version is at least 6.3.0
        if VERSION >= '6.3.0':
            # Import MODE, TAG_NAMES and TAG_MAPPING from config.py
            from config import MODE_EqualAbove6_3 as mode, MODE_MAPPING_EqualAbove6_3 as MODE_MAPPING, TAG_NAMES_EqualAbove6_3 as TAG_NAMES, TAG_MAPPING_EqualAbove6_3 as TAG_MAPPING
        else:
            # Import MODE from Gigapixel
            from gigapixel import Mode
            
            # Import TAG_NAMES and TAG_MAPPING from Gigapixel
            from config import MODE_MAPPING, TAG_NAMES, TAG_MAPPING
        return mode, MODE_MAPPING, TAG_NAMES, TAG_MAPPING

    def __callGraphQL(self, query, variables=None):
        json = {}
        json['query'] = query
        if variables != None:
            json['variables'] = variables

        # handle cookies
        response = requests.post(
            self.STASH_URL, json=json, headers=self.headers)

        if response.status_code == 200:
            result = response.json()
            if result.get("error", None):
                for error in result["error"]["errors"]:
                    raise Exception("GraphQL error: {}".format(error))
            if result.get("data", None):
                return result.get("data")
        elif response.status_code == 401:
            self.my_log.error(
                "[ERROR][GraphQL] HTTP Error 401, Unauthorised. You can add a API Key in at top of the script")
            return None
        else:
            raise Exception(
                "GraphQL query failed:{} - {}. Query: {}. Variables: {}".format(response.status_code, response.content,
                                                                                query, variables))

    def findTagIdWithName(self, tag_name):
        query = """
            query {
                allTags {
                    id
                    name
                }
            }
        """
        result = self.__callGraphQL(query)
        for tag in result["allTags"]:
            if tag["name"] == tag_name:
                return tag["id"]
        return None

    def createTagWithName(self, name, MODE_DESCRIPTION):
        query = """
mutation tagCreate($input:TagCreateInput!) {
  tagCreate(input: $input){
    id
    description
  }
}
"""
        variables = {'input': {
            'name': name,
            'description': MODE_DESCRIPTION
        }}
        result = self.__callGraphQL(query, variables)
        return result["tagCreate"]["id"]

    def removeTagWithID(self, id):
        query = """
mutation tagDestroy($input: TagDestroyInput!) {
  tagDestroy(input: $input)
}
"""
        variables = {'input': {
            'id': id
        }}
        self.__callGraphQL(query, variables)

    def updateTagImage(self, tag_id, base64_data):
        query = """
mutation tagUpdate($input: TagUpdateInput!){
  tagUpdate(input: $input){
    id
    image_path
  }
  
}
"""
        variables = {'input': {
            'id': tag_id,
            'image': base64_data
        }}
        self.__callGraphQL(query, variables)

    def updatePerformerIDTagsWithID(self, id, tag_ids):
        query = """
mutation performerUpdates($input: PerformerUpdateInput!){
  performerUpdate(input: $input)
  {
    id
		tags{
      id
    }
  }
}
"""
        variables = {'input': {
            'id': id,
            'tag_ids': tag_ids
        }}
        self.__callGraphQL(query, variables)

    def findPerformersByTag(self, id):
        query = """query performer_images($performer_filter: PerformerFilterType!) {
  findPerformers(performer_filter: $performer_filter filter: {per_page: -1}){

  performers{
    id
    name
    image_path
    tags{
      name
    }
  }
}
}"""
        variables = {'performer_filter': {
            'tags': {
                'value': id, 'modifier': 'INCLUDES', 'depth': 1

            }
        }}
        result = self.__callGraphQL(query, variables)
        performers = result["findPerformers"]["performers"]
        image_paths_tags = [(performer["image_path"], performer["id"],
                             performer["name"]) for performer in performers]
        return image_paths_tags

    def findPerformersTagsbyID(self, id):
        query = """query findPerformer($id: ID!){
      findPerformer(id: $id){
        tags{
          name
        }
      }
    }"""
        variables = {'id': id}
        result = self.__callGraphQL(query, variables)
        performers_tags = result["findPerformer"]["tags"]
        performers_tags_names = [performer["name"]
                                 for performer in performers_tags]
        return performers_tags_names

    def processPerformerImage(self, app, image_path, performer_id, mode, scale, tag):
        global tag_ids
        global app_keys
        tag_ids = []
        # Find and delete the image and output files
        for file_name in os.listdir(CUSTOM_MAPPED_FOLDER):
            file_name_without_ext, ext = os.path.splitext(file_name)
            if file_name_without_ext == IMAGE_NAME or file_name_without_ext == IMAGE_NAME + OUTPUT_SUFFIX:
                file_path = os.path.join(CUSTOM_MAPPED_FOLDER, file_name)
                os.remove(file_path)
        # Download the image
        try:
            r = requests.get(image_path, stream=True, headers=self.headers)
            r.raise_for_status()
            img = Image.open(BytesIO(r.content))
            file_format = img.format.lower()
            
            if file_format not in IMAGE_TYPES:
                self.my_log.error(
                    "file_format not in IMAGE_TYPES: converting to JPEG")
                img = img.convert('RGB')
                file_format = 'jpeg'

            image_name_process = f"{IMAGE_NAME}.{file_format}"
            image_saved = Path(CUSTOM_MAPPED_FOLDER) / image_name_process
       
            # Save the image
            with open( image_saved, "wb") as f:
                img.save(f, format=file_format)

        except requests.exceptions.RequestException as e:
            self.my_log.error(
                "An error occurred while trying to download the image:{}".format(e))
            return
        except Exception as e:
            self.my_log.error(
                "An error occurred while trying to convert the image:{}".format(e))
            return
        # Process the image
        output_path = app.process(image_saved, scale=scale, mode=mode)
        # Find the first matching file
        output_file_path = None
        output_file_name = None
        for file_name in os.listdir(CUSTOM_MAPPED_FOLDER):
            file_name_without_ext, ext = os.path.splitext(file_name)
            if file_name_without_ext == IMAGE_NAME + OUTPUT_SUFFIX:
                output_file_path = os.path.join(CUSTOM_MAPPED_FOLDER, file_name)
                image_processed = file_name
                break

        if output_file_path is not None:
            self.my_log.debug(f"Found output file: {output_file_path}")
        else:
            self.my_log.error("No matching output file found.")
        image_upload_url = f"{CUSTOM_MAPPED_URL}/{image_processed}"
        # Perform the mutation to upload the image
        query = """
            mutation PerformerUpdate($performer_update_input: PerformerUpdateInput!){
                performerUpdate(input: $performer_update_input){
                    id
                    image_path
                }
            }
                """
        variables = {"performer_update_input": {
            "id": performer_id,
            "image": image_upload_url,
            }}
            
        result = self.__callGraphQL(query, variables)
        # Update Performer Tags
        tags_remove_checks = self.findPerformersTagsbyID(performer_id)
        tag_to_remove = f"Upscale {tag}"
        tag_to_remove_id = self.findTagIdWithName(tag_to_remove)
        tag_ids_keep = []

        for tags_remove_check in tags_remove_checks:
            tags_remove_check_id = self.findTagIdWithName(tags_remove_check)
            if tag_to_remove_id not in tags_remove_check_id:
                tag_ids_keep.append(tags_remove_check_id)

        upscaled_name = "Upscaled: Performer Image"
        upscaled = self.findTagIdWithName(upscaled_name)
        tag_ids_keep.append(upscaled)
        # remove the marker value
        self.updatePerformerIDTagsWithID(performer_id, tag_ids_keep)

    def setup_tags(self):
        _, _, TAG_NAMES, TAG_MAPPING = self.get_version()
        from config import MODE_DESCRIPTIONS
        
        for tag_name in TAG_NAMES:
            tag_id = self.findTagIdWithName(tag_name)
            if tag_id == None:
                 # Iterate over the keys of MODE_DESCRIPTIONS
                for key in MODE_DESCRIPTIONS.keys():
                    # Use regular expressions to check if tag_name matches with any part of the key
                    if re.search(key, tag_name):
                        # If there is a match, print the value corresponding to the key
                        tag_id = self.createTagWithName(tag_name, MODE_DESCRIPTIONS[key])
                        self.my_log.debug(f"Adding tag: {tag_name}")
                        self.setup_tag_images(tag_id, tag_name, TAG_MAPPING)
            else:
                self.my_log.error(f"Tag: {tag_name} : already exists")

    def setup_tag_images(self, tag_id, tag_name, TAG_MAPPING):
        # Get the folder path of the current running script
        script_path = os.path.dirname(os.path.abspath(__file__))
        # Join the assets folder path to the script path
        assets_path = os.path.join(script_path, 'assets')
        if SET_TAG_IMAGE_GENERATION == 'Yes':
            key = next((k for k, v in TAG_MAPPING.items()
                       if v == tag_name), None)
            if key:
                self.my_log.debug(f"Key: {key}")
                tag_image = os.path.join(assets_path, key)
                with open(tag_image, "rb") as image_file:
                    encoded_string = base64.b64encode(
                        image_file.read()).decode("utf-8")
                    data_url = f"data:image/jpeg;base64,{encoded_string}"
                self.updateTagImage(tag_id, data_url)
            else:
                self.my_log.error("Setup Tag Images: Value not found in mapping.")

    def remove_tags(self):
        _, _, TAG_NAMES, _ = self.get_version()
        for tag_name in TAG_NAMES:
            tag_id = self.findTagIdWithName(tag_name)
            if tag_id == None:
                self.my_log.error(f"Error Tag: {tag_name} doesn't exist")
            else:
                self.my_log.debug(f"Removing tag: {tag_name}")
                tag_id = self.removeTagWithID(tag_id)

    def get_gigapixel_setting(self, tag, MODE_MAPPING):
        split_list = tag.split(":")
        first_half_mode = split_list[0]
        second_half_scale = split_list[1]
        mode = MODE_MAPPING.get(first_half_mode, None)
        scale = SCALE_MAPPING.get(second_half_scale, None)
        return mode, scale

    def check_tag_names_not_empty(self, TAG_NAMES):
        if not TAG_NAMES:
            raise ValueError("TAG_NAMES is empty")

    def check_tags_not_empty(self, tags):
        if not tags:
            raise ValueError("tags is empty")

    def check_tag_in_tag_names(self, tags, TAG_NAMES):
        for tag in tags:
            if tag not in TAG_NAMES:
                return False
        return True

    def check_performer_tagged_once(self, tags, TAG_NAMES):
        if not set(tags).intersection(TAG_NAMES):
            return

    def upscale_PerformerImage(self):
        global app_keys
        mode, MODE_MAPPING, TAG_NAMES, TAG_MAPPING = self.get_version()
        # Start Gigapixel instance through thread
        app = MainGigapixel(EXE_PATH, OUTPUT_SUFFIX)
        # Continue
        self.check_tag_names_not_empty(TAG_NAMES)
        for tag_name in TAG_NAMES:
            tag_id = self.findTagIdWithName(tag_name)
            if not tag_id:
                self.my_log.error("tag_id: Is none, Removing tag: "+tag_name)
            performers = self.findPerformersByTag(tag_id)
            for performer in performers:
                self.process_performer_image(app, performer, mode, MODE_MAPPING, TAG_NAMES, TAG_MAPPING)

    def process_performer_image(self, app, performer, mode, MODE_MAPPING, TAG_NAMES, TAG_MAPPING):
        performer_id = performer[1]  # Initialize performer_id here
        performer_name = performer[2]
        tags = self.findPerformersTagsbyID(performer_id)
        self.check_performer_tagged_once(tags, TAG_NAMES)
        self.check_tags_not_empty(tags)

        for tag in tags:
            if tag != "Upscaled: Performer Image" and tag in TAG_NAMES:
                tag = tag.replace("Upscale ", "")
                mode, scale = self.get_gigapixel_setting(tag, MODE_MAPPING)
                performer_id = performer[1]
                image_path = performer[0]
                self.processPerformerImage(
                    app, image_path, performer_id, mode, scale, tag)

log = Logger() # create an instance of Log

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            STASH_URL = sys.argv[2]
            API_KEY = sys.argv[3]
        if sys.argv[1] == "setup":
            client = UpscaleWith(STASH_URL, API_KEY)
            client.setup_tags()
        elif sys.argv[1] == "upscale_all":
            client = UpscaleWith(STASH_URL, API_KEY)
            client.upscale_PerformerImage()
        elif sys.argv[1] == "remove_tags":
            client = UpscaleWith(STASH_URL, API_KEY)
            client.remove_tags()
        elif sys.argv[1] == "api":
            fragment = json.loads(sys.stdin.read())
            scheme = fragment["server_connection"]["Scheme"]
            port = fragment["server_connection"]["Port"]
            domain = "localhost"
            if "Domain" in fragment["server_connection"]:
                domain = fragment["server_connection"]["Domain"]
            if not domain:
                domain = 'localhost'
            url = scheme + "://" + domain + ":" + str(port) + "/graphql"

            client = UpscaleWith(STASH_URL, API_KEY)
            mode = fragment["args"]["mode"]
            client.my_log.debug("Mode: "+mode)
            if mode == "setup":
                client.setup_tags()
            elif mode == "upscale_all":
                client.upscale_PerformerImage()
            elif mode == "remove_tags":
                client.remove_tags()
    else:
        print("")
