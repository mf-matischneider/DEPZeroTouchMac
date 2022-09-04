apple_pref_path = "/Library/Preferences/"
class PlistManager:

    def __init__(self, plist_path):
        self.plist_path = plist_path

    def get_plist_value(self, key):
        return os.popen(f"defaults read {self.plist_path} {key}").read()

    def set_plist_value(self, key, value):
        os.system(f"defaults write {self.plist_path} {key} {value}")

    def show_all_files(self):
        self.set_plist_value('com.apple.Finder', 'AppleShowAllFiles', 'YES')
        os.system("killall Finder")

    def hide_all_files(self):
        self.set_plist_value('com.apple.Finder', 'AppleShowAllFiles', 'NO')
        os.system("killall Finder")

    def set_plist_path(self, plist_path):
        self.plist_path = plist_path

    def get_plist_path(self):
        return self.plist_path

    def create_plist(self, plist_name):
        os.system(f"touch {apple_pref_path}{plist_name}.plist")