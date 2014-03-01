# -*- coding:utf-8 -*-

from StringIO import StringIO

from flask import Flask, render_template, Response, request
from pygments import highlight
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.lexers.special import TextLexer
from pygments.formatters.img import ImageFormatter
from pygments.util import ClassNotFound

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def top():
    return render_template('top.html', lexers=get_all_lexers())

@app.route('/dynamic/preview', methods=['POST'])
def preview():
    binary = _gen(request.form['text'], font=request.form['font'], lexer=request.form['lexer'])
    return Response(binary.encode("base64"), mimetype='text/plain')

@app.route('/dynamic/generate', methods=['POST'])
def generate():
    binary = _gen(request.form['text'], font=request.form['font'], lexer=request.form['lexer'])
    return Response(binary, mimetype='text/png')

def _gen(text, **kwargs):
    try:
        lexer = get_lexer_by_name(kwargs['lexer'])
    except ClassNotFound:
        lexer = TextLexer()

    f = ImageFormatter(font_name=kwargs['font'])
    sio = StringIO(highlight(text, lexer, f))
    sio.seek(0)
    return sio.getvalue()

if __name__ == '__main__':
    app.run()
