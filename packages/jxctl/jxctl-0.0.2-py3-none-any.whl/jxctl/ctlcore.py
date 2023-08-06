import os
import yaml

class ctlCore:
    CONTEXT_FILE_PATH = "/.jxctl/config"
    USER_HOME = os.path.expanduser('~')
    CONTEXT_FILE = USER_HOME + CONTEXT_FILE_PATH

    cUser = cToken = cURL = cName = ''

    def __init__(self):
        context = yaml.load(open(self.CONTEXT_FILE))
        self.cUser = str(context["context"]["user"])
        self.cToken = str(context["context"]["token"])
        self.cURL = str(context["context"]["url"])
        self.cName = str(context["context"]["name"])
        #print(self.cName, self.cToken, self.cURL, self.cUser)

    def validate_context(self):
        return True

    def set_context(self, url, user, token, name):
        if user is not None:
            self.cUser = user
        if token is not None:
            self.cToken = token
        if url is not None:
            self.cURL = url

        if name is not None:
            self.cName = name        

        context_file = """
            current-context: %s
            context :
                url: %s
                user: %s
                token: %s
                name: %s
            """ % (self.cName, self.cURL, self.cUser, self.cToken, self.cName)
        print(yaml.dump(yaml.load(context_file), default_flow_style=False))

        with open(self.CONTEXT_FILE, 'w') as cFile:
            yaml.dump(yaml.load(context_file), cFile, default_flow_style=False)

    def show_current_context(self):
        print("Jenkins Running on : " + self.cURL)
        
