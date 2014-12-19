# -*- coding:utf-8 -*-

from StringIO import StringIO

from flask import Flask, Response, abort, render_template, request, session
from pygments import highlight
from pygments.lexers import get_all_lexers, get_lexer_by_name, get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.formatters.img import ImageFormatter
from pygments.util import ClassNotFound

app = Flask(__name__)
app.config['DEBUG'] = True

DEFAULT_FONT_SIZE = 14


@app.route('/')
def top():
    return render_template('live_convert.html', lexers=get_all_lexers())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/api/preview', methods=['POST'])
def preview():
    _csrf_protect()

    # Set lexer
    try:
        lexer = get_lexer_by_name(request.form['lexer'])
    except ClassNotFound:
        lexer = TextLexer()

    kwargs = {}

    # Set option values for pygments
    # font_size
    try:
        font_size = int(request.form['font_size'])
        if font_size > 0:
            kwargs['font_size'] = font_size
    except ValueError:
        pass

    if not 'font_size' in kwargs.keys():
        kwargs['font_size'] = DEFAULT_FONT_SIZE

    # line_numbers
    if not 'is_display_linenum' in request.form:
        kwargs['line_numbers'] = False

    binary = _generate(request.form['text'], lexer, kwargs)

    return Response(binary.encode("base64"), mimetype='text/plain')


@app.route('/api/detect', methods=['POST'])
def detect_from_name():
    _csrf_protect()

    # Detect lexer
    try:
        lexer = get_lexer_for_filename(request.form['name'])
    except ClassNotFound:
        lexer = TextLexer()
    return Response(lexer.aliases[0], mimetype='text/plain')


def _generate(text, lexer, kwargs):
    convert_text = []

    # Check multi-byte character and append dummy character(space)
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


def _csrf_protect():
    if request.method == "POST":
        if not request.headers.get('X-requested-with').lower() == 'xmlhttprequest':
            abort(403)


if __name__ == '__main__':
    app.run()
