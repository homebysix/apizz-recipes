#!/usr/bin/python
#

import os
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["MASCLIDownloader"]



class MASCLIDownloader(Processor):
    """Downloads and installs a Mac App Store app given a provided MAS app ID
       """
    description = __doc__

    input_variables = {
        "appstoreextractor_dir": {
        	"required": False,
        	"default": "/Users/Shared/AppStore_Packages",
        	"description":
        		("Path to AppStoreExtractor.sh packaging directory."),
        },
        "appstoreextractor_script": {
        	"required": True,
        	"description":
        		("Full path to AppStoreExtractor.sh script"),
        },
        "force": {
            "required": False,
            "default": False,
            "description":
                ("If set to true, will forcibly reinstall the Mac App Store app if already installed."),
        },
        "mas_app_id": {
            "required": True,
            "description":
                ("Software ID for Mac App Store app."),
        },
    }
    output_variables = {
        "developer": {
            "description": "Developer from Mac App Store listing",
        },
        "minimum_os_version": {
            "description": "Minimum OS version from Mac App Store listing.",
        },
        "name": {
            "description": "Software name from Mac App Store listing.",
        },
        "pathname": {
        	"description": "Path to AppStoreExtractor-created DMG"
        },
        "version": {
            "description": "Software version from Mac App Store listing.",
        },
    }

    def main(self):
        """Set Variables"""
        appstoreextractor_dir = self.env['appstoreextractor_dir']
        appstoreextractor_script = self.env['appstoreextractor_script']
        force = self.env['force']
        mas_app_id = self.env['mas_app_id']
        mas_cli_exec = os.popen('which mas').read()
                
        """Verify mas-cli is installed"""
        if not os.path.exists(mas_cli_exec):
        	raise ProcessorError(
        		"mas-cli does not appear to be installed, or not located in your PATH.")
        		
        """Verify AppStoreExtractor.sh exists"""
        if not os.path.exists(appstoreextractor_script):
        	raise ProcessorError(
        		"AppStoreExtractor.sh does not appear to located at the path provided.")
        
        """Check whether to install with --force to reinstall already installed apps"""		
        if force is False:
        	command = ["mas","install", mas_app_id]
        elif force is True:
        	command = ["mas","install", mas_app_id, "--force"]
        else:
        	raise ProcessorError(
        		"Non-boolean value set for 'force' processor input.")
        
        """Run mas-cli download & install"""
        try:
        	subprocess.check_call(command)
        except subprocess.CalledProcessError:
        	raise ProcessorError(
        		"Error Running mas-cli download/install.")
        
         
        """Get MAS app info from mas-cli and parse"""
        try:
        	mas_app_info = os.popen('mas info mas_app_id').read()
        	mas_app_info = mass_app_info.splitlines()
        	mas_app_basicinfo = mass_app_info[0].split()
        	
        	"""Merge MAS app name if it contains spaces"""
        	basic_info_items = len(mas_app_basicinfo[0])
        	if not basic_info_items = 3:
        		name = mas_app_basicinfo[:-2]
        		name = "".join(name)
        	else:
        		name = mas_app_basicinfo[0]
        		
        	version = mas_app_basicinfo[1]
        	developer = mas_app_info[1][4:]
        	minimum_os_version = mas_app_info[3][12]
        
        	self.env["developer"] = str(developer)
        	self.env["minimum_os_version"] = str(minimum_os_version)
        	self.env["name"] = str(name)
        	self.env["version"] = str(version)
        	

if __name__ == '__main__':
    PROCESSOR = MASCLIDownloader()
    PROCESSOR.execute_shell()