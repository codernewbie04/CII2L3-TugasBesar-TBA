from distutils.log import debug
from flask import Flask, render_template, jsonify, request
import string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    content = request.get_json(silent=True)
    output, statusLexical = LexicalAnalyzer(content['kalimat'])
    
    if statusLexical:
        output2, statusParser = Parser(content['kalimat'])
        return jsonify({"msg_lexical": output, "status_lexical":statusLexical, "msg_parser": output2, "status_parser":statusParser})
    else:
        return jsonify({"msg_lexical": output, "status_lexical":statusLexical, "msg_parser": "", "status_parser":False})
        
        
def LexicalAnalyzer(string_input):
    # inputting string
    input_string = string_input.lower() + "#"

    # initialization
    alphabet_list = list(string.ascii_lowercase)
    state_list = [
        "q0",
        "q1",
        "q2",
        "q3",
        "q4",
        "q5",
        "q6",
        "q7",
        "q8",
        "q9",
        "q10",
        "q11",
        "q12",
        "q13",
        "q14",
        "q15",
        "q16",
        "q17",
        "q18",
        "q19",
        "q20",
        "q21",
        "q22",
        "q23"
    ]

    transition_table = {}

    for i in state_list:
        for alphabet in alphabet_list:
            transition_table[(i, alphabet)] = "ERROR"
        transition_table[(i, "#")] = "ERROR"
        transition_table[(i, " ")] = "ERROR"

    # CFG
    # s -> NN VB NN
    # NN -> lon | jih | kah | bu | miie | adek
    # VB -> co' | poh | sipa' | galak | 

    # For starting node (q0)
    transition_table[("q0", " ")] = "q0"

    # Finish state
    transition_table[("q22", "#")] = "ACCEPT"
    transition_table[("q22", " ")] = "q23"

    transition_table[("q23", "#")] = "ACCEPT"
    transition_table[("q23", " ")] = "q23"

    # string "lon"
    transition_table[("q23", "l")] = "q1"
    transition_table[("q0", "l")] = "q1"
    transition_table[("q1", "o")] = "q2"
    transition_table[("q2", "n")] = "q22"

    # string "jih"
    transition_table[("q23", "j")] = "q3"
    transition_table[("q0", "j")] = "q3"
    transition_table[("q3", "i")] = "q4"
    transition_table[("q4", "h")] = "q22"

    # string "kah"
    transition_table[("q23", "k")] = "q5"
    transition_table[("q0", "k")] = "q5"
    transition_table[("q5", "a")] = "q4"

    # string "galak"
    transition_table[("q23", "g")] = "q6"
    transition_table[("q0", "g")] = "q6"
    transition_table[("q6", "a")] = "q7"
    transition_table[("q7", "l")] = "q8"
    transition_table[("q8", "a")] = "q9"
    transition_table[("q9", "k")] = "q22"

    # string co'
    transition_table[("q23", "c")] = "q10"
    transition_table[("q0", "c")] = "q10"
    transition_table[("q10", "o")] = "q11"
    transition_table[("q11", "'")] = "q22"

    # string poh
    transition_table[("q23", "p")] = "q12"
    transition_table[("q0", "p")] = "q12"
    transition_table[("q12", "o")] = "q4"
    
    # string sipa'
    transition_table[("q23", "s")] = "q13"
    transition_table[("q0", "s")] = "q13"
    transition_table[("q13", "i")] = "q14"
    transition_table[("q14", "p")] = "q15"
    transition_table[("q15", "a")] = "q11"

    # string bu
    transition_table[("q23", "b")] = "q16"
    transition_table[("q0", "b")] = "q16"
    transition_table[("q16", "u")] = "q22"

    # string miie
    transition_table[("q23", "m")] = "q17"
    transition_table[("q0", "m")] = "q17"
    transition_table[("q17", "i")] = "q18"
    transition_table[("q18", "i")] = "q19"
    transition_table[("q19", "e")] = "q22"

    # string adek
    transition_table[("q23", "a")] = "q20"
    transition_table[("q0", "a")] = "q20"
    transition_table[("q20", "d")] = "q21"
    transition_table[("q21", "e")] = "q9"


    # lexical Analysis
    is_success = False
    return_string = ""
    idx_char = 0
    state = "q0"
    current_token = ""
    while state != "ACCEPT":
        current_char = input_string[idx_char]
        current_token += current_char
        tmp_state = "{space}" if current_char.isspace() else current_char
        tmp_state = state + " "+ tmp_state
        return_string += tmp_state + "<br/>"
        state = transition_table[(state, current_char)]
        if state == "q22":
            return_string += "<br/><div class='alert alert-success' role='alert'>current token: {} is valid".format(current_token) + "</div>"
            current_token = ""
        if state == "ERROR":
            return_string += "<br/><div class='alert alert-danger' role='alert'>ERROR dalam Lexical Analyzer, {} tidak valid</div>".format(current_token)
            break
        idx_char += 1
    # Conclusion
    if state == "ACCEPT":
        is_success = True
        return_string += "<br/><div class='alert alert-success' role='alert'>semua token yang di input: {} valid</div>".format(input_string)
    return return_string, is_success

def Parser(string_input):
    tokens = string_input.lower().split()
    tokens.append("EOS")
    # s -> S NN VB
    # NN -> lon | jih | kah | bu | miie | adek
    # VB -> co' | poh | sipa' | galak |
    # symbols definiton
    non_terminals = ["S", "NN", "VB"]
    terminals = [
        "lon",
        "jih",
        "kah",
        "bu",
        "miie",
        "adek",
        "co'",
        "poh",
        "sipa'",
        "galak",
    ]

    # parse table definition
    parse_table = {}

    parse_table[("S", "lon")] = ["NN", "VB", "NN"]
    parse_table[("S", "jih")] = ["NN", "VB", "NN"]
    parse_table[("S", "kah")] = ["NN", "VB", "NN"]
    parse_table[("S", "bu")] = ["NN", "VB", "NN"]
    parse_table[("S", "miie")] = ["NN", "VB", "NN"]
    parse_table[("S", "adek")] = ["NN", "VB", "NN"]
    parse_table[("S", "co'")] = ["error"]
    parse_table[("S", "poh")] = ["error"]
    parse_table[("S", "sipa'")] = ["error"]
    parse_table[("S", "galak")] = ["error"]
    parse_table[("S", "EOS")] = ["error"]

    parse_table[("NN", "lon")] = ["lon"]
    parse_table[("NN", "jih")] = ["jih"]
    parse_table[("NN", "kah")] = ["kah"]
    parse_table[("NN", "bu")] = ["bu"]
    parse_table[("NN", "miie")] = ["miie"]
    parse_table[("NN", "adek")] = ["adek"]
    parse_table[("NN", "co'")] = ["error"]
    parse_table[("NN", "poh")] = ["error"]
    parse_table[("NN", "sipa'")] = ["error"]
    parse_table[("NN", "galak")] = ["error"]
    parse_table[("NN", "EOS")] = ["error"]

    parse_table[("VB", "lon")] = ["error"]
    parse_table[("VB", "jih")] = ["error"]
    parse_table[("VB", "kah")] = ["error"]
    parse_table[("VB", "bu")] = ["error"]
    parse_table[("VB", "miie")] = ["error"]
    parse_table[("VB", "adek")] = ["error"]
    parse_table[("VB", "co'")] = ["co'"]
    parse_table[("VB", "poh")] = ["poh"]
    parse_table[("VB", "sipa'")] = ["sipa'"]
    parse_table[("VB", "galak")] = ["galak"]
    parse_table[("VB", "EOS")] = ["error"]

    # stack initialization
    stack = []
    stack.append("#")
    stack.append("S")

    # input reading initialization
    idx_token = 0
    symbol = tokens[idx_token]

    return_string = ""
    # parsing process
    while len(stack) > 0:
        top = stack[len(stack) - 1]
        return_string += "top = "+top+"<br/>"
        return_string += "symbol = " + symbol+"<br/>"
        if top in terminals:
            return_string += "top adalah simbol terminal <br/>"
            if top == symbol:
                stack.pop()
                idx_token = idx_token + 1
                symbol = tokens[idx_token]
                if symbol == "EOS":
                    stack.pop()
            else:
                return_string += "<br/><div class='alert alert-danger' role='alert'>ERROR dalam Parsing kalimat {}".format(string_input) + "</div>"
                break
                
        elif top in non_terminals:
            return_string += "top adalah simbol non-terminal <br/>"
            if parse_table[(top, symbol)][0] != "error":
                stack.pop()
                symbols_to_be_pushed = parse_table[(top, symbol)]
                for i in range(len(symbols_to_be_pushed) - 1, -1, -1):
                    stack.append(symbols_to_be_pushed[i])
            else:
                return_string += "<br/><div class='alert alert-danger' role='alert'>ERROR dalam Parsing kalimat {}".format(string_input) + "</div>"
                break
        else:
            return_string += "<br/><div class='alert alert-danger' role='alert'>ERROR dalam Parsing kalimat {}".format(string_input) + "</div>"
            break
        return_string += "isi stack:" + "".join(str(item)+" " for item in stack) + "<br/>"
        return_string += "<br/>"
    # conclusion
    return_string += "<br/>"
    if symbol == "EOS" and len(stack) == 0:
        return_string += "<div class='alert alert-success' role='alert'>input string " + string_input + " diterima, sesuai Grammar</div>"
    return return_string, symbol == "EOS" and len(stack) == 0 


if __name__ == "__main__":
    app.run(debug=True)