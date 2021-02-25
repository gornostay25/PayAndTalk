from clubhouse.clubhouse import Clubhouse
import configparser
from bottle import Bottle,run,auth_basic,request,response,view,static_file
app = Bottle()
USERCONFIG = None
client = None
ME = None

def read_config(filename='setting.ini'):
    """ (str) -> dict of str
    Read Config
    """
    config = configparser.ConfigParser()
    config.read(filename)
    if "Account" in config:
        return dict(config['Account'])
    return dict()

def doAuth(user,password):
    if USERCONFIG["login"] == user and USERCONFIG["password"] == password:
        return True
    else:
        return False


@app.route("/assets/<file:path>")
def staticAssets(file):
    return static_file(file,root="./views/assets/")

@app.get("/")
@auth_basic(doAuth)
@view("index")
def index():
    return {}

@app.get("/settings")
@auth_basic(doAuth)
@view("settings")
def settings():
    return read_config()


def main():
    global client,ME
    client = Clubhouse(
        user_id=USERCONFIG["user_id"],
        user_token=USERCONFIG["user_token"],
        user_device=USERCONFIG["user_device"]
    )
    ME = client.me()
    run(app, host='localhost', port=8080,debug=True)
    doExit()


def doExit():
    pass


if __name__ == "__main__":
    USERCONFIG = read_config()
    main()