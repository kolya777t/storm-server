from flask import Flask, request, jsonify
import random

app = Flask(__name__)
CHECKED_FILE = "checked.txt"
FOUND_FILE = "found.txt"
WORDS_FILE = "bip39_words.txt"

# Загрузка словаря
with open(WORDS_FILE) as f:
    WORDS = [w.strip() for w in f.readlines()]

# Проверка тестовой фразы при запуске
TEST_PHRASE = "allow claim sustain comfort tuition coral quote topple scorpion nation merry kiss"
with open(FOUND_FILE, "a") as f:
    f.write(f"[TEST] {TEST_PHRASE} | TEST_ADDRESS | 500 USDT\n")

@app.route("/get_task", methods=["GET"])
def get_task():
    with open(CHECKED_FILE, "r") as f:
        already_checked = set(line.strip() for line in f)
    for _ in range(100):
        phrase = " ".join(random.sample(WORDS, 12))
        if phrase not in already_checked:
            return jsonify({"phrase": phrase})
    return jsonify({"phrase": ""})

@app.route("/submit_checked", methods=["POST"])
def submit_checked():
    data = request.json
    phrase = data.get("phrase", "")
    if phrase:
        with open(CHECKED_FILE, "a") as f:
            f.write(phrase + "\n")
    return jsonify({"status": "ok"})

@app.route("/submit_found", methods=["POST"])
def submit_found():
    data = request.json
    with open(FOUND_FILE, "a") as f:
        f.write(f"{data['phrase']} | {data['address']} | {data['balance']} USDT\n")
    return jsonify({"status": "saved"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)