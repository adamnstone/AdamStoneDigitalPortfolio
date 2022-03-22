import flask, threading, time, random, json, os
from flask import request
from cryptography.fernet import Fernet

app = flask.Flask(__name__)
app.config["DEBUG"] = True
#app.config["SERVER_NAME"] = "LaundromatAPI.com"

url = "http://34.67.212.21/"

secret_file_name = "secrets.txt"
data_file_name = "data.txt"
filekey_name = "filekey.txt"
random_secret_characters = ["a", "b", "c", "d", "e", "f", "g", "H", "I", "J", "K", "L", "X", "z", "_", "-"]
secret_length_range = 30, 50
code = 0xfbce434ee3
code_string = "0xfbce434ee3"
master_key = 0x238746AFB
master_key_string = "0x238746AFB"

splitter = "/||-||/"

machine_info = {}

def create_file(path):
    if not os.path.exists(path):
        with open(path, "w") as file:
            pass

def create_files():
    paths = [secret_file_name, data_file_name, filekey_name]
    for path in paths:
        create_file(path)

def erase_data():
    with open(data_file_name, "r+") as file:
        file.truncate(0)

def save_data(data):
    with open(data_file_name, "w") as file:
        file.write(json.dumps(data))

def load_data():
    if os.path.exists(data_file_name):
        with open(data_file_name, "r") as file:
            return json.loads(file.read())
    else:
        return {}


def format_data_for_string_in_json():
    return_string = ""
    machine_info_keys = []
    for k in machine_info:
        machine_info_keys.append(k)
    for i in range(len(machine_info_keys)):
        key = machine_info_keys[i]
        value = machine_info[key]
        return_string += key + ": " + str(value) + (", " if i != len(machine_info) - 1 else "")
    return return_string

def generate_secret():
    secret = ""
    for i in range(random.randint(secret_length_range[0], secret_length_range[1])):
        secret += random_secret_characters[random.randint(0, len(random_secret_characters) - 1)]
    set_secret(secret)
    return secret

def initialize_fernet():
    with open(filekey_name, "rb") as filekey:
        if filekey.read().strip() != "".encode():
            with open(secret_file_name, "r") as f:
                if f.read().strip() != "":
                    decrypt_file(secret_file_name)

    key = Fernet.generate_key()

    # string the key in a file
    with open(filekey_name, 'wb') as filekey:
       filekey.write(key)

    with open(secret_file_name, "r") as f:
        if f.read().strip() != "":
            encrypt_file(secret_file_name)

def get_secrets():
    decrypt_file(secret_file_name)
    contents = ""
    try:
        with open(secret_file_name, "rb") as file:
            contents = file.read().decode()
    except Exception as e:
        pass
    encrypt_file(secret_file_name)
    return contents.split(splitter)

def set_secret(secret):
    decrypt_file(secret_file_name)
    contents = ""
    first = False
    try:
        with open(secret_file_name, "rb") as file:
            contents = file.read().decode()
    except:
        first = True

    with open(secret_file_name, "wb") as file:
        file.write(contents.encode())
        if not first and contents.strip() != "":
            file.write(splitter.encode())
        file.write(secret.encode())
    encrypt_file(secret_file_name)

def encrypt_file(file_name):
    with open(file_name, "r") as f:
        if f.read().strip() == "":
            return
    # opening the key
    with open(filekey_name, 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    encrypted = ""
    with open(file_name, "r") as file:
        encrypted = fernet.encrypt(file.read().encode())
    with open(secret_file_name, "wb") as file:
        file.write(encrypted)

def decrypt_file(file_name):
    with open(file_name, "r") as f:
        if f.read().strip() == "":
            return
    # opening the key
    with open(filekey_name, 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    decrypted = ""
    with open(file_name, "rb") as file:
        decrypted = fernet.decrypt(file.read())
    with open(file_name, "wb") as file:
        file.write(decrypted)

def get_home_page(has_secret=True):
    return_string = "<h1>Home Page for Adam Stone Analytical Services' Laundromat API</h1><br><br>"
    if has_secret:
        info_string = "<ul>"
        for key in machine_info:
            info_string += "<li><h2>" + key + ": " + str(machine_info[key]) + "</h2></li>"
        return_string += info_string + "</ul>"
    else:
        return_string += "<h2>You may register <a href='/register'>here</a>"
    return return_string

def make_response(success, **kwargs):
    rsp = kwargs
    rsp["status"] = "success" if success else "error"
    return rsp, 200 if success else 400


@app.route('/', methods=['GET'])
def home():
    if 'code' in request.args:
        code_attempt = None
        try:
            code_attempt = hex(int(request.args['code']))
        except Exception as e:
            code_attempt = request.args['code']
        print(request.args['code'])
        print(str(code_attempt).lower().strip())
        if str(code_attempt).lower().strip() == code_string:
            return get_home_page()
        else:
            return make_response(False, message="Error: Incorrect code - Please provide the correct code")
    else:
        return get_home_page(has_secret=False)

@app.route('/api/v1', methods=['GET'])
def home_api():
    if 'client_secret' in request.args:
        client_secret = request.args['client_secret']
        if client_secret in get_secrets():
                return make_response(True, message=format_data_for_string_in_json())
        else:
            return make_response(False, message="Error: Invalid client secret - Please provide a valid client secret")
    else:
        return make_response(False, message="Error: No client secret provided - You may register here: " + request.base_url + "/register?code=*the code*")


@app.route("/api/v1/register", methods=['GET'])
def register_api():
    if 'code' in request.args:
        code_attempt = int(request.args['code'], 16)
        if code_attempt == code:
            if not 'string' in request.args:
                return make_response(True, client_secret=generate_secret())
            else:
                use_string = request.args['string'].lower()
                if use_string == 'true':
                    return generate_secret()
                elif use_string == 'false':
                    make_response(True, client_secret=generate_secret())
                else:
                    return make_response(False, message="Error: 'string' not set to 'true' or 'false' - Please provide valid value for parameter 'string'")
        else:
            return make_response(False, message="Error: Incorrect code - Please provide the correct code")
    else:
        return make_response(False, message="Error: Incorrect code - Please provide the correct code")

@app.route("/api/v1/checkcode", methods=['GET'])
def check_code():
    if 'code' in request.args:
        if request.args['code'] == code_string:
            return "success"
        else:
            return "incorrect code"
    else:
        return make_response(False, error="Error: No code provided - Please provide a code")

@app.route("/register", methods=['GET'])
def register():
    return '''<h1>Please enter the code you have been provided with:</h1>
    <br>
    <input id='input'></input>
    <button id='button' onclick='check()'>Submit</button>
    <script>
    function check() {
        if (document.getElementById('input').value.length <= ''' + str(len(code_string)) + ''')
        {
            fetch(window.location.origin + "/api/v1/checkcode?code=" + document.getElementById('input').value)
                .then(function (response) {
                    response.text().then(function (text){
                        if (text == "success")
                        {
                            let url = "''' + url + "?code="+'''"+document.getElementById('input').value;
                            window.open(url);
                            window.close();
                        }
                        else
                        {
                            alert("Incorrect Code")
                        }
                    });
                });
        }
        else if (document.getElementById('input').value.length > ''' + str(len(code_string)) + ''') {
            alert('Code must be less than ''' + str(len(code_string)) + ''' digits');
        }
        else{
            alert('Incorrect Code')
        }
    }
    </script>'''


@app.route('/api/v1/sendmessage', methods=['POST', 'GET'])
def send_message():
    if 'client_secret' in request.args:
        client_secret = request.args['client_secret']
        if client_secret in get_secrets():
            resp = {}
            if 'key' in request.args:
                key = request.args['key']
                if 'fromapp' in request.args:
                    from_app = (True if request.args['fromapp'].lower() == "true" else False)
                    if not from_app:
                        if request.args['fromapp'].lower() != "false":
                            return make_response(False, message="Error: 'fromapp' parameter not a valid value - Please specify 'true' or 'false'")
                    resp['key'] = key + (" - Started From App" if from_app else " - Started By Customer")
                else:
                    return make_response(False, message="Error: No 'fromapp' parameter provided - Please specify 'true' or 'false'")
            else:
                return make_response(False, message="Error: No key field provided - Please specify a key")

            if 'value' in request.args:
                value = request.args['value']
                resp['value'] = value
            else:
                return make_response(False, message="Error: No value field provided - Please specify a value")
            try:
                test = machine_info[resp['key']]
                machine_info[resp['key']] += float(resp['value'])
            except Exception as e:
                try:
                    machine_info[resp['key']] = float(resp['value'])
                except Exception as e2:
                    return make_response(False, message="Error: Key not an number - Please provide a number")

            save_data(machine_info)

            return make_response(True, message="Key '" + key + "' and Value '" + value + "' were received")
        else:
            return make_response(False, message="Error: Invalid client secret - Please provide a valid client secret")
    else:
        return make_response(False, message="Error: No client secret provided - Please provide a client secret")

@app.route('/api/v1/resetinfo', methods=['POST', 'GET'])
def reset_info():
    global machine_info
    if 'master_key' in request.args:
        master_key_attempt = request.args['master_key']
        if master_key_attempt == master_key_string:
            with open(data_file_name, "w") as file:
                machine_info = {}
                erase_data()
                return make_response(True, message="Success - Data Reset")
        else:
            return make_response(False, error="Error: Incorrect master key - Please provide a valid master key")
    else:
        return make_response(False, error="Error: No master key provided - Please provide a master key")

create_files()
initialize_fernet()
with open(data_file_name, "r") as file:
    if file.read().strip() != "":
        machine_info = load_data()

if __name__ == "__main__":
    print("STARTING SERVER...")
    app.run(host="0.0.0.0", port=80)
