import os
from .githelper import get_tag, get_project_name_from_url
from .config_data import load_config
from codegenhelper import debug
import demjson

def init_tag_for_project(giturl, tag, config_name, location=os.getcwd(), key_file_path = None):
    get_tag(giturl, tag, location, key_file_path)

    def load_tag(dep_config):
        get_tag(dep_config["giturl"], dep_config["tag"], location, key_file_path)
        
        return demjson.decode_file(os.path.join(location, get_project_name_from_url(dep_config["giturl"]), "deploy", dep_config["config_name"] + ".cfg"))
    
    load_config(os.path.join(location, debug(get_project_name_from_url(giturl), "url_project_nameg"), "deploy", config_name + ".cfg"), load_tag)
