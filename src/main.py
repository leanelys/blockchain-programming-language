from flask import Flask, render_template, request, send_file
from lexer import my_lexer
from parser import my_parser
import json
import io
import sys
import globals

def run_program(code):
    lexer = my_lexer
    parser = my_parser

    buffer = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer

    try:
        parser.parse(code, lexer=lexer)
    except Exception as e:
        print("[Runtime Error]", e)
    
    sys.stdout = sys_stdout
    return buffer.getvalue()

# Start flask app
app = Flask(__name__)

# Main and only page
@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    code = ""

    if request.method == 'POST':
        code = request.form['code']
        output = run_program(code)

    chain = json.dumps([blk.get_as_dict() for blk in globals.blockchain.chain], indent=4)
    return render_template('home.html', output=output, code=code, chain=chain)

# Allows user to download the blockchain as a json file
@app.route('/download')
def download():
    globals.blockchain.export()
    return send_file('blockchain.json', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
