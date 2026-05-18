import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Math challenges
# ---------------------------------------------------------------------------

def generate_math():
    level = random.choice(["easy", "easy", "medium", "hard"])
    if level == "easy":
        op = random.choice(["+", "-"])
        a, b = random.randint(2, 20), random.randint(2, 20)
        if op == "-" and b > a:
            a, b = b, a
        answer = a + b if op == "+" else a - b
    elif level == "medium":
        op = random.choice(["+", "-", "*"])
        if op == "*":
            a, b = random.randint(2, 12), random.randint(2, 12)
            answer = a * b
        elif op == "+":
            a, b = random.randint(20, 99), random.randint(10, 50)
            answer = a + b
        else:
            a, b = random.randint(30, 99), random.randint(10, 30)
            answer = a - b
    else:
        op = random.choice(["*", "+"])
        if op == "*":
            a, b = random.randint(7, 15), random.randint(7, 15)
            answer = a * b
        else:
            a, b = random.randint(100, 500), random.randint(100, 500)
            answer = a + b

    return {
        "type": "math",
        "question": f"{a} {op} {b}",
        "answer": str(answer),
        "level": level,
    }


# ---------------------------------------------------------------------------
# Word association – odd one out
# ---------------------------------------------------------------------------

ODD_ONE_OUT = [
    {"words": ["Apple", "Banana", "Orange", "Hammer"],     "odd": "Hammer",   "reason": "not a fruit"},
    {"words": ["Dog", "Cat", "Bird", "Table"],              "odd": "Table",    "reason": "not an animal"},
    {"words": ["Red", "Blue", "Happy", "Green"],            "odd": "Happy",    "reason": "not a colour"},
    {"words": ["Paris", "London", "Tokyo", "Mountain"],     "odd": "Mountain", "reason": "not a city"},
    {"words": ["Piano", "Guitar", "Violin", "Pencil"],      "odd": "Pencil",   "reason": "not a musical instrument"},
    {"words": ["Run", "Jump", "Walk", "Sky"],               "odd": "Sky",      "reason": "not an action"},
    {"words": ["Circle", "Square", "Triangle", "Water"],    "odd": "Water",    "reason": "not a shape"},
    {"words": ["Rose", "Tulip", "Daisy", "Stone"],          "odd": "Stone",    "reason": "not a flower"},
    {"words": ["Monday", "Friday", "Sunday", "January"],   "odd": "January",  "reason": "not a day of the week"},
    {"words": ["Mercury", "Venus", "Earth", "Moon"],        "odd": "Moon",     "reason": "not a planet"},
    {"words": ["Whisper", "Shout", "Murmur", "Bright"],    "odd": "Bright",   "reason": "not related to sound"},
    {"words": ["Oak", "Pine", "Maple", "Cobra"],            "odd": "Cobra",    "reason": "not a tree"},
    {"words": ["Salmon", "Tuna", "Shark", "Eagle"],         "odd": "Eagle",    "reason": "not a fish"},
    {"words": ["Copper", "Silver", "Gold", "Sand"],         "odd": "Sand",     "reason": "not a metal"},
    {"words": ["Smile", "Laugh", "Grin", "Cry"],            "odd": "Cry",      "reason": "not a happy expression"},
    {"words": ["Chess", "Checkers", "Go", "Tennis"],        "odd": "Tennis",   "reason": "not a board game"},
    {"words": ["Spring", "Summer", "Autumn", "Morning"],   "odd": "Morning",  "reason": "not a season"},
    {"words": ["Italy", "France", "Spain", "Amazon"],       "odd": "Amazon",   "reason": "not a country"},
    {"words": ["Knee", "Elbow", "Wrist", "Forehead"],       "odd": "Forehead", "reason": "not a joint"},
    {"words": ["Flute", "Drums", "Trumpet", "Canvas"],      "odd": "Canvas",   "reason": "not a musical instrument"},
    {"words": ["Saturn", "Jupiter", "Neptune", "Sun"],      "odd": "Sun",      "reason": "not a planet"},
    {"words": ["Novel", "Poem", "Essay", "Hammer"],         "odd": "Hammer",   "reason": "not a literary form"},
    {"words": ["Tiger", "Lion", "Cheetah", "Penguin"],      "odd": "Penguin",  "reason": "not a big cat"},
    {"words": ["Calm", "Serene", "Peaceful", "Loud"],       "odd": "Loud",     "reason": "not a calm state"},
    {"words": ["Oxygen", "Nitrogen", "Hydrogen", "Iron"],  "odd": "Iron",     "reason": "not a gas"},
    {"words": ["Swim", "Dive", "Float", "Climb"],           "odd": "Climb",    "reason": "not a water activity"},
    {"words": ["Noon", "Dusk", "Dawn", "Winter"],           "odd": "Winter",   "reason": "not a time of day"},
    {"words": ["Sparrow", "Robin", "Falcon", "Salmon"],     "odd": "Salmon",   "reason": "not a bird"},
    {"words": ["Brave", "Fearless", "Bold", "Timid"],       "odd": "Timid",    "reason": "not a bold quality"},
    {"words": ["Carrot", "Broccoli", "Spinach", "Peach"],  "odd": "Peach",    "reason": "not a vegetable"},
]


def generate_word():
    item = random.choice(ODD_ONE_OUT)
    words = item["words"][:]
    random.shuffle(words)
    return {
        "type": "word",
        "question": "Which word does NOT belong?",
        "words": words,
        "answer": item["odd"],
        "reason": item["reason"],
    }


# ---------------------------------------------------------------------------
# Memory sequence
# ---------------------------------------------------------------------------

MEMORY_WORDS = [
    "river", "candle", "mountain", "whisper", "amber",
    "gentle", "forest", "silver", "morning", "crystal",
    "harbor", "meadow", "breeze", "lantern", "pebble",
    "echo", "serene", "drift", "bloom", "quiet",
    "stone", "light", "rain", "shore", "wind",
]


def generate_memory():
    mode = random.choice(["numbers", "words"])
    if mode == "numbers":
        length = random.randint(4, 6)
        seq = [str(random.randint(1, 9)) for _ in range(length)]
        return {
            "type": "memory",
            "mode": "numbers",
            "sequence": seq,
            "answer": "".join(seq),
            "hint": "Type all digits in order, no spaces",
        }
    else:
        length = random.randint(3, 4)
        seq = random.sample(MEMORY_WORDS, length)
        return {
            "type": "memory",
            "mode": "words",
            "sequence": seq,
            "answer": " ".join(seq),
            "hint": "Type the words in order, separated by spaces",
        }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

CHALLENGE_TYPES = ["math", "math", "word", "memory"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/challenge")
def get_challenge():
    ctype = request.args.get("type", "random")
    if ctype == "breathing":
        return jsonify({"type": "breathing"})
    if ctype == "random":
        ctype = random.choice(CHALLENGE_TYPES)
    generators = {"math": generate_math, "word": generate_word, "memory": generate_memory}
    return jsonify(generators.get(ctype, generate_math)())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
