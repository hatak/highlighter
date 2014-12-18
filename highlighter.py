# -*- coding:utf-8 -*-

from StringIO import StringIO

from flask import Flask, render_template, Response, request
from pygments import highlight
from pygments.lexers import get_all_lexers, get_lexer_by_name, get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.formatters.img import ImageFormatter
from pygments.util import ClassNotFound

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def top():
    return render_template('top.html', lexers=get_all_lexers())


@app.route('/api/preview', methods=['POST'])
def preview():
    try:
        lexer = get_lexer_by_name(request.form['lexer'])
    except ClassNotFound:
        lexer = TextLexer()

    kwargs = {
        'font_size': request.form['font_size'],
    }
    if not 'is_display_linenum' in request.form:
        kwargs['line_numbers'] = False

    binary = _generate(request.form['text'], lexer, kwargs)
    return Response(binary.encode("base64"), mimetype='text/plain')


# @app.route('/dynamic/generate', methods=['POST'])
#def generate():
#    binary = _generate(request.form['text'], font=request.form['font'], lexer=request.form['lexer'])
#    return Response(binary, mimetype='image/png')


@app.route('/api/detect', methods=['POST'])
def detect_from_name():
    try:
        lexer = get_lexer_for_filename(request.form['name'])
    except ClassNotFound:
        lexer = TextLexer()
    return Response(lexer.aliases[0], mimetype='text/plain')


def _generate(text, lexer, kwargs):
    convert_text = []

    # check multi-byte character and append dummy character(space)
    for line in text.split('\n'):
        count = 0
        for c in line:
            if ord(c) > 255:
                count += 1
        convert_text.append(line + str(" " * count))

    # Font: RictyDiscord-Regular"
    # Style: EclipseStyle, emacs, default,
    f = ImageFormatter(font_name="RictyDiscord-Regular",
                       line_pad=5, line_number_bg="#fff", style="github", **kwargs)
    sio = StringIO(highlight("\n".join(convert_text), lexer, f))
    sio.seek(0)
    return sio.getvalue()


if __name__ == '__main__':
    app.run()
