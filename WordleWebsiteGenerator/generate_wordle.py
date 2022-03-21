import os, shutil

from matplotlib.pyplot import get


new_line = "\n"
new_line_as_text = "\\n"
tab = "    "

def app_python(has_answers, get_todays_wordle_func_code, answers_file, valid_guesses_file):
    return f'''
from flask import Flask, render_template, request
import random, datetime, threading, time

HAS_ANSWERS = {has_answers}

def seconds_until_midnight():
    dt = datetime.datetime.now()
    return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)

def load_possible_answers():
    answers = {{}}
    with open("databases/{answers_file}", "r") as file:
        lines = [_.strip().lower() for _ in file.read().split("{new_line_as_text}") if _.strip()]
        for line in lines:
            spl = line.split()
            name = spl[0]
            {(f'meaning = " ".join(spl[1:]).strip(){new_line}{tab}{tab}{tab}answers[name] = meaning' if has_answers else 'answers[name] = ""')}
    return answers

def load_valid_guesses(possible_answers):
    answers = []
    with open("databases/{valid_guesses_file}", "r") as file:
        answers += [_.strip().lower() for _ in file.read().split("{new_line_as_text}") if _.strip()]
    answers += [_.strip().lower() for _ in list(possible_answers.keys()) if (_.strip() and _ not in answers)]
    return answers

{get_todays_wordle_func_code}

app = Flask(__name__)

possible_answers = load_possible_answers()
valid_guesses = load_valid_guesses(possible_answers)
wordle = None

def new_wordle():
    global wordle
    wordle = get_todays_wordle(possible_answers)

def word_thread_func():
    time.sleep(seconds_until_midnight())
    while True:
        new_wordle()
        time.sleep(60 * 60 * 24)

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/is_word", methods=['POST'])
def is_word():
    word_to_check = request.get_json().get("word").strip().lower()
    is_valid = word_to_check in valid_guesses
    return {{"status": "success", "is_valid": is_valid}}

@app.route("/word_today", methods=['POST'])
def word_today():
    return {{"status": "success", "word": wordle, "meaning": possible_answers[wordle]}}

if __name__ == "__main__":
    new_wordle()
    word_thread = threading.Thread(target=word_thread_func, args=())
    word_thread.start()
    app.run(host="0.0.0.0", port=80)
'''

def app_js(has_answers, num_letters, num_guesses):
    return f'''
let numLetters = {num_letters};
let numGuesses = {num_guesses};
let titleDisplay;
let keyboard;
let messageDisplay;
let wordle;
let wordleMeaning;
let currentRow = 0;
let currentTile = 0;
let isGameOver = false;

document.addEventListener("keydown", e => {{
    handleClick(e.key);
}});

document.addEventListener("DOMContentLoaded", () => {{
    for (let i = 0; i < numGuesses; i++) {{
        let r = [];
        for (let j = 0; j < numLetters; j++) {{
            r.push('');
        }}
        guessRows.push(r);
    }}

    tileDisplay = document.querySelector('.tile-container');
    keyboard = document.querySelector('.key-container');
    messageDisplay = document.querySelector('.message-container');
    getWordle();

    guessRows.forEach((guessRow, guessRowIndex) => {{
        const rowElement = document.createElement('div');
        rowElement.setAttribute('id', 'guessRow-' + guessRowIndex);
        guessRow.forEach((_guess, guessIndex) => {{
            const tileElement = document.createElement('div');
            tileElement.setAttribute('id', 'guessRow-' + guessRowIndex + '-tile-' + guessIndex);
            tileElement.classList.add('tile');
            rowElement.append(tileElement);
        }});
        tileDisplay.append(rowElement);
    }});

    let i = 0;
    keys.forEach(row => {{
        i += 1;
        const rowElement = document.createElement("div");
        rowElement.classList.add(`keyboard-row-${{i}}`);
        row.forEach(key => {{
            const buttonElement = document.createElement('button');
            buttonElement.textContent = key;
            buttonElement.setAttribute('id', key);
            buttonElement.addEventListener('click', () => handleClick(key));
            buttonElement.classList.add(`key-row-${{i}}`);
            if (key === "<<" || key === "ENT") {{
                buttonElement.classList.add("longer-key");
            }} else {{
                buttonElement.classList.add("normal-sized-key")
            }}
            rowElement.append(buttonElement)
        }});
        keyboard.append(rowElement)
    }})
}});


const getWordle = () => {{
    fetch(`/word_today`, 
            {{
                method: "POST", 
                headers: {{'Content-Type': 'application/json'}}, 
                body: JSON.stringify({{}})
            }}
        )
        .then(response => response.json())
        .then(json => {{
            wordle = json.word.toUpperCase();
            wordleMeaning = json.meaning;
        }}).catch(err => console.log(err));
}}

const keys = [
    ['Q',
    'W',
    'E',
    'R',
    'T',
    'Y',
    'U',
    'I',
    'O',
    'P'],
    ['A',
    'S',
    'D',
    'F',
    'G',
    'H',
    'J',
    'K',
    'L'],
    ['ENT',
    'Z',
    'X',
    'C',
    'V',
    'B',
    'N',
    'M',
    '<<']
];

const allKeyLetters = [
    'Q',
    'W',
    'E',
    'R',
    'T',
    'Y',
    'U',
    'I',
    'O',
    'P',
    'A',
    'S',
    'D',
    'F',
    'G',
    'H',
    'J',
    'K',
    'L',
    'ENT',
    'Z',
    'X',
    'C',
    'V',
    'B',
    'N',
    'M',
    '<<'
];

let guessRows = [];


const handleClick = (letter) => {{
    if (!isGameOver && (allKeyLetters.includes(letter.toUpperCase()) || letter === "Backspace" || letter === "Enter")) {{
        if (letter === '<<' || letter === "Backspace") {{
            deleteLetter()
            return
        }}
        if (letter === 'Enter' || letter === "ENT") {{
            checkRow()
            return
        }}
        addLetter(letter.toUpperCase())
    }}
}}

const addLetter = (letter) => {{
    if (currentTile < numLetters && currentRow < numGuesses) {{
        const tile = document.getElementById('guessRow-' + currentRow + '-tile-' + currentTile);
        tile.textContent = letter;
        guessRows[currentRow][currentTile] = letter;
        tile.setAttribute('data', letter);
        currentTile++;
    }}
}}

const deleteLetter = () => {{
    if (currentTile > 0) {{
        currentTile--;
        const tile = document.getElementById('guessRow-' + currentRow + '-tile-' + currentTile);
        tile.textContent = '';
        guessRows[currentRow][currentTile] = '';
        tile.setAttribute('data', '');
    }}
}}

const checkRow = () => {{
    const guess = guessRows[currentRow].join('')
    if (currentTile == numLetters) {{
        fetch(`/is_word`, 
            {{
                method: "POST", 
                headers: {{'Content-Type': 'application/json'}}, 
                body: JSON.stringify({{word: guess}})
            }}
        )
        .then(response => response.json())
        .then(json => {{
            if (!json.is_valid) {{
                showMessage('Word Not In List');
                return;
            }} else {{
                flipTile();
                if (wordle == guess) {{
                    {(f'(showMessage(`Magnificent! Meaning: "${{wordleMeaning}}"`, displayTime=100000))' if has_answers else "")}
                    isGameOver = true;
                    return;
                }} else {{
                    if (currentRow == numGuesses - 1) {{
                        isGameOver = true;
                        showMessage(`Game Over! The word was: "${{wordle}}"{(f' meaning "${{wordleMeaning}}"`' if has_answers else "`")}, displayTime=100000);
                        return;
                    }}
                    if (currentRow < numGuesses - 1) {{
                        currentRow++;
                        currentTile = 0;
                    }}
                }}
            }}
        }}).catch(err => console.log(err));
    }}
}}

const showMessage = (message, displayTime=2000) => {{
    const messageElement = document.createElement('p')
    messageElement.textContent = message
    messageDisplay.append(messageElement)
    setTimeout(() => messageDisplay.removeChild(messageElement), displayTime)
}}

const addColorToKey = (keyLetter, color) => {{
    const key = document.getElementById(keyLetter)
    key.classList.add(color)
}}

const flipTile = () => {{
    const rowTiles = document.querySelector('#guessRow-' + currentRow).childNodes
    let checkWordle = wordle
    const guess = []

    rowTiles.forEach(tile => {{
        guess.push({{letter: tile.getAttribute('data'), color: 'grey-overlay'}})
    }})

    guess.forEach((guess, index) => {{
        if (guess.letter == wordle[index]) {{
            guess.color = 'green-overlay'
            checkWordle = checkWordle.replace(guess.letter, '')
        }}
    }})

    guess.forEach(guess => {{
        if (checkWordle.includes(guess.letter)) {{
            guess.color = 'yellow-overlay'
            checkWordle = checkWordle.replace(guess.letter, '')
        }}
    }})

    rowTiles.forEach((tile, index) => {{
        setTimeout(() => {{
            tile.classList.add('flip')
            tile.classList.add(guess[index].color)
            addColorToKey(guess[index].letter, guess[index].color)
        }}, 500 * index)
    }})
}}
'''

def app_css(light_mode=True):
    return ('''
* {
    color: #ffffff;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande',
    'Lucida Sans', Arial, sans-serif;
}

body {
    background-color: #121213;
}

.game-container {
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

h1 {
    margin-top: 1%;
    margin-bottom: 3%;
}

h2 {
    margin-bottom: 2%;
}

.title-container {
    text-align: center;
    width: 30%;
    border-bottom: solid 1px #3a3a3c;
}

.tile-container div {
    justify-content: center;
}

.tile-container {
    width: 330px;
    margin-bottom: 10px;
}

.key-container {
    width: 450px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

button:hover {
    cursor: pointer;
}

.key-container button {
    height: 50px;
    border-radius: 4px;
    border: none;
    background-color: #818384;
    margin: 4px;
}

.normal-sized-key {
    width: 36px;
}

.longer-key {
    width: 60px;
}

.key-container button:nth-child(11) {
    margin-left: 30px;
}

.key-container button:nth-child(20),
.key-container button:nth-child(28) {
    width: 68px;
}

.tile-container div {
    display: flex;
}

.tile-container .tile {
    width: 62px;
    height: 62px;
    border: 2px solid#3a3a3c;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 2px;
}

.message-container {
    height: 30px;
    z-index: 1;
    text-align: center;
}

.message-container p {
    background-color: #818384;
    border-radius: 10px;
    padding: 10px;
    margin: 0;
}

.tile.flip {
    animation: 0.5s linear flipping;
}

@keyframes flipping {
    0% {
        transform: rotateX(0deg);
    }
    50% {
        transform: rotateX(90deg);
    }
    100% {
        transform: rotateX(0deg);
    }
}



.grey-overlay {
    background-color: #3a3a3c !important;
    border:none !important;
}
.yellow-overlay {
    background-color: #b59f3a !important;
    border:none !important;
}

.green-overlay {
    background-color: #538d4e !important;
    border:none !important;
}
''' if not light_mode else '''

* {
    color: white;
    font-size: 2rem;
    font-weight: 400;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande',
    'Lucida Sans', Arial, sans-serif;
}

h1 {
    font-size: 1rem;
    font-weight: 900;
    color: blue;
}

h2 {
    font-size: 0.5rem;
    font-weight: 900;
    color: blue;
}

body {
    background-color: #ffffff;
}

.game-container {
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

h1 {
    margin-top: 2%;
    margin-bottom: 2%;
}

h2 {
    margin-top: 0%;
    margin-bottom: 2%;
}

.title-container {
    text-align: center;
    width: 30%;
    border-bottom: solid 1px #3a3a3c;
}

.tile-container div {
    justify-content: center;
}

.tile-container {
    margin-top: 1%;
    width: 330px;
    margin-bottom: 0%;
}

.key-container {
    width: 450px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 0;
}

button:hover {
    cursor: pointer;
}

.keyboard-row-1, .keyboard-row-2, .keyboard-row-3 {
    height: 33%;
}

.key-container button {
    height: 85%;
    border-radius: 4px;
    border: none;
    background-color: #a8a8a8;
    margin: 4px;
    font-size: 0.9rem;
}

.normal-sized-key {
    width: 36px;
}

.longer-key {
    width: 60px;
}

.tile-container div {
    display: flex;
}

.tile-container .tile {
    width: 62px;
    height: 62px;
    border: 2px solid#3a3a3c;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 2px;
    color: black;
}

.message-container {
    height: 30px;
    z-index: 1;
    text-align: center;
    position: fixed;
    height: 100%;
    width: 100%;
}

.message-container p {
    background-color: #302e2e;
    border-radius: 10px;
    padding: 10px;
    margin: 0;
    font-size: 0.5rem;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 7%;
}

.tile.flip {
    animation: 0.5s linear flipping forwards;
}

@keyframes flipping {
    0% {
        transform: rotateX(0deg);
    }
    50% {
        transform: rotateX(90deg);
    }
    100% {
        transform: rotateX(0deg);
        color: white;
    }
}



.grey-overlay {
    background-color: #858282 !important;
    border:none !important;
}
.yellow-overlay {
    background-color: #b59f3b !important;
    border:none !important;
}

.green-overlay {
    background-color: #85da7d !important;
    border:none !important;
}
''') 

def app_html(title, subtitle):
    return f'''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{{{url_for('static', filename='css/app.css')}}}}"/>
    <script src="{{{{url_for('static', filename='js/app.js')}}}}"></script>
</head>
    <body>

        <div class="game-container">
            <div class="title-container">
                <h1>{title}</h1>
                <h2>{subtitle}</h2>
            </div>
            <div class="message-container"></div>
            <div class="tile-container"></div>
            <div class="key-container"></div>
        </div>
    </body>
</html>
'''

def generate_wordle(TITLE, SUBTITLE, NUM_LETTERS, NUM_GUESSES, GET_WORDLE_FUNCTION, ANSWERS_FILE, VALID_GUESSES_FILE, HAS_DEFINITIONS, OUTPUT_DIRECTORY, LIGHT_MODE=True):
    os.mkdir(OUTPUT_DIRECTORY)
    os.mkdir(os.path.join(OUTPUT_DIRECTORY, "databases"))
    shutil.copy(ANSWERS_FILE, os.path.join(OUTPUT_DIRECTORY, "databases"))
    shutil.copy(VALID_GUESSES_FILE, os.path.join(OUTPUT_DIRECTORY, "databases"))
    with open(os.path.join(OUTPUT_DIRECTORY, "main.py"), "w") as file:
        file.write(app_python(HAS_DEFINITIONS, GET_WORDLE_FUNCTION, (ANSWERS_FILE.split("/")[-1] if "/" in ANSWERS_FILE else ANSWERS_FILE.split("\\")[-1]), (VALID_GUESSES_FILE.split("/")[-1] if "/" in VALID_GUESSES_FILE else VALID_GUESSES_FILE.split("\\")[-1])))
    os.mkdir(os.path.join(OUTPUT_DIRECTORY, "templates"))
    os.mkdir(os.path.join(OUTPUT_DIRECTORY, "static"))
    os.mkdir(os.path.join(OUTPUT_DIRECTORY, os.path.join("static", "js")))
    os.mkdir(os.path.join(OUTPUT_DIRECTORY, os.path.join("static", "css")))
    with open(os.path.join(OUTPUT_DIRECTORY, os.path.join("templates", "index.html")), "w") as file:
        file.write(app_html(TITLE, SUBTITLE))
    with open(os.path.join(OUTPUT_DIRECTORY, os.path.join("static", os.path.join("js", "app.js"))), "w") as file:
        file.write(app_js(HAS_DEFINITIONS, NUM_LETTERS, NUM_GUESSES))
    with open(os.path.join(OUTPUT_DIRECTORY, os.path.join("static", os.path.join("css", "app.css"))), "w") as file:
        file.write(app_css(light_mode=LIGHT_MODE))