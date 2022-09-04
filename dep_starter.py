import getpass
import os
import shutil
import subprocess
from datetime import datetime

from plist_manager import PlistManager

temp_folder_path = '/usr/local/depnotify-with-installers/'

prestarter_installer_path = 'usr/local/depnotify-with-installers/DEPNotify-prestarter-installer.sh'
prestarter_uninstaller_path = 'usr/local/depnotify-with-installers/DEPNotify-prestarter-uninstaller.zsh'

# Placeholders
org_identifier = 'com.Markforged'
temp_utilities_path = '/usr/local/depnotify-with-installers'
dep_notify_installer_name = 'DEPNotify.pkg'
dep_notify_log_path = '/var/tmp/depnotify.log'
dep_notify_app_path = '/Applications/Utilities/DEPNotify.app/Contents/MacOS/DEPNotify'
installer_base_string = '{0}.DEPNotify-prestarter'.format(org_identifier)
installer_script_name = '{0}-installer.zsh'.format(installer_base_string)
installer_script_path = '{0}/{1}'.format(temp_utilities_path, installer_script_name)
uninstaller_script_name = '{0}-uninstaller.zsh'.format(installer_base_string)
uninstaller_script_path = '{0}/{1}'.format(temp_utilities_path, uninstaller_script_name)
dep_notify_starter_trigger = '/var/tmp/depnotify-starter-trigger'

# LaunchDaemon name and file path
launch_daemon_name = '{0}.plist'.format(installer_base_string)
launch_daemon_path = '/Library/LaunchDaemons/{0}'.format(launch_daemon_name)


# Install DEPNotify to Applications/Utilities
def install_dep_notify():
    installer_command = '/usr/sbin/installer -pkg {0}/{1} -target /'.format(temp_utilities_path,
                                                                            dep_notify_installer_name)
    if os.path.exists(dep_notify_app_path):
        print('DEP Notify Already installed')
    else:
        os.system(installer_command)


#########################################################################################
# Setup Script creation & General Appearance
#########################################################################################

def create_setup_script():
    print(f'Creating Setup Script {installer_script_path}')


# Banner Image
banner_image_path = '/usr/local/techops/logos/logo.png'
# Placeholder for org name
org_name = 'Markforged'
# Heading displayed under logo
banner_title = 'Welcome to {0}'.format(org_name)
# Subheading support contact info
support_contact_details = 'email helpdesk@markforged.com'

# Welcome Message
main_text = 'hanks for choosing a Mac at {0}!We want you to have a few applications and settings configured before you get started with your new Mac. This process should take 10 to 20 minutes to complete. \n \n If you need additional software or help, please visit the help center at https://help.markforged.com/it.'.format(
    org_name)
# Initial Start Status text that shows as things are firing up
initial_start_status = 'Initial Configuration Starting...'
install_complete_text = 'Configuration Completed!'
# Text that will display inside the alert once policies have finished
complete_main_text = 'Your Mac is now finished initial setup and configuration.'
complete_button_text = 'Restart'
#########################################################################################
# Plist Configuration
#########################################################################################
# Plist save location
dep_notify_user_input_plist = f'/Users/{getpass.getuser()}/Library/Preferences/menu.nomad.DEPNotifyUserInput.plist'
# Status text alignment
status_text_alignment = 'center'

# Help Button Configuration
help_bubble_title = 'Need Help?'
help_bubble_body = f'This tool at {org_name} is designed to help you get started with your new Mac.designed to help ' \
                   f'with new employee onboarding. If you have issues, please contact {support_contact_details}. '

# Error Screen Text
error_banner_title = 'Uh Oh, Something Went Wrong!'
error_banner_body = 'Please contact {0} for assistance.'.format(support_contact_details)

# Error status message that is displayed under the progress bar
error_status = 'Setup Failed, Please contact the helpdesk team.'

#########################################################################################
# Task List
#########################################################################################
# The policy array must be formatted "Progress Bar text,Functionname". These will be
# run in the order as they appear below.

policy_array = [
    'Cleaning Dock,CLEAN_DOCK'
    'Naming Computer,NAME_COMPUTER'
    'Installing 1Password,INSTALL_1PASSWORD'
    'Installing Chrome,INSTALL_CHROME'
    'Installing Google Drive For Desktop,INSTALL_DRIVE'
    'Installing Zoom,INSTALL_ZOOM'
    'Installing Slack,INSTALL_SLACK'
    'Configuring Printers,INSTALL_PRINTERS'
    'Installing DUO Health App,INSTALL_DHA'
    'Installing Sentinel One,INSTALL_S1'
    'Doing some cleanup,CLEANUP'
]


#########################################################################################
# Application Installation
#########################################################################################
# Install 1Password
def install_1password():
    print('Installing 1Password')
    # os.system('sudo /usr/local/bin/brew cask install 1password')
    install_pkg('https://app-updates.agilebits.com/download/OPM7', '1Password.pkg')


def install_chrome():
    print('Installing Chrome')
    # os.system('sudo /usr/local/bin/brew cask install google-chrome')
    install_pkg('https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg', 'Google Chrome.pkg')


def install_drive():
    print('Installing Google Drive')
    # os.system('sudo /usr/local/bin/brew cask install google-drive-file-stream')
    install_dmg('https://dl.google.com/drive-file-stream/GoogleDriveFileStream.dmg', 'GoogleDriveFileStream.pkg')

def install_zoom():
    print('Installing Zoom')
    # os.system('sudo /usr/local/bin/brew cask install zoomus')
    install_pkg('https://zoom.us/client/latest/ZoomInstallerIT.pkg', 'Zoom.pkg')
    # Create custom zoom plist
    zoom_plist = f'/Users/{getpass.getuser()}/Library/Preferences/us.zoom.config.plist'
    plist_manager = PlistManager(zoom_plist)
    plist_manager.set('nogoogle', True)
    plist_manager.set('nofacebook', True)
    plist_manager.set('ZAutoSSOLogin', True)
    plist_manager.set('ZSSOHost', 'markforged.zoom.us')
    plist_manager.set('ZRemoteControlAllApp', True)
    plist_manager.set('PackageRecommend', 'ZAutoJoinVoip')
    plist_manager.set('ZAutoJoinVoip', True)
    plist_manager.set('ZDualMonitorOn', False)



def install_slack():
    print('Installing Slack')
    # os.system('sudo /usr/local/bin/brew cask install slack')


def configure_printers():
    print('Configuring Printers')


def install_dha():
    print('Installing DUO Health App')
    # os.system('sudo /usr/local/bin/brew cask install duo-health')


def install_s1():
    print('Installing Sentinel One')
    # os.system('sudo /usr/local/bin/brew cask install sentinelone')


def cleanup():
    print('Cleaning up')


#########################################################################################
# Base Install Functions
def install_pkg(download_url, pkg_name):
    print(f'Installing {pkg_name}')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp_folder_name = f'Download-{date}'
    os.chdir(temp_utilities_path)
    if os.path.exists(f'{temp_utilities_path}/temp_folder_name'):
        print(f'{temp_folder_name} already exists')
        os.chdir(temp_folder_name)
        subprocess.call(['curl', '-s -O', download_url])
    else:
        os.mkdir(temp_folder_name)
        os.chdir(temp_folder_name)

    download = subprocess.call(['curl', '-s -O', download_url])
    if check_app_installed(pkg_name):
        print(f'{pkg_name} already installed')
    elif download == 0:
        print(f'{pkg_name} downloaded successfully')
        subprocess.call(['installer', '-pkg', pkg_name, '-target', '/'])
        print(f'{pkg_name} installed successfully')
    else:
        print(f'{pkg_name} failed to download')

    # Remove the temp folder
    os.chdir(temp_utilities_path)
    os.rmdir(temp_folder_name)
    print(f'{temp_folder_name} removed')
    return True


# check if app is installed
def check_app_installed(app_name):
    if os.path.exists('/Applications/{0}.app'.format(app_name)):
        print('App {0} is already installed.'.format(app_name))
        return True
    else:
        return False
# Base DMG Install Function
def install_dmg(download_url, dmg_name):
    print(f'Installing {dmg_name}')
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp_folder_name = f'Download-{date}'
    os.chdir(temp_utilities_path)
    if os.path.exists(f'{temp_utilities_path}/temp_folder_name'):
        print(f'{temp_folder_name} already exists')
        os.chdir(temp_folder_name)
        subprocess.call(['curl', '-s -O', download_url])
    else:
        os.mkdir(temp_folder_name)
        os.chdir(temp_folder_name)

    download = subprocess.call(['curl', '-s -O', download_url])
    if check_app_installed(dmg_name):
        print(f'{dmg_name} already installed')
    elif download == 0:
        print(f'{dmg_name} downloaded successfully')
        subprocess.call(['hdiutil', 'attach', dmg_name])
        subprocess.call(['installer', '-pkg', f'/Volumes/{dmg_name}/{dmg_name}.pkg', '-target', '/'])
        print(f'{dmg_name} installed successfully')
    else:
        print(f'{dmg_name} failed to download')

    # Remove the temp folder
    os.chdir(temp_utilities_path)
    os.rmdir(temp_folder_name)
    print(f'{temp_folder_name} removed')
    return True

