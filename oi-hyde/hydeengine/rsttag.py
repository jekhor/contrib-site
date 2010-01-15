from jinja2 import nodes
from jinja2.ext import Extension
from docutils import core, io


# html_parts and html_body are both copy&pasted from docutils examples.py
def html_parts(input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=1, initial_header_level=1):
    """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
    """
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        writer_name='html', settings_overrides=overrides)
    return parts

def html_body(input_string, source_path=None, destination_path=None,
              input_encoding='unicode', output_encoding='unicode',
              doctitle=1, initial_header_level=1):
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see `html_parts()` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """
    parts = html_parts(
        input_string=input_string, source_path=source_path,
        destination_path=destination_path,
        input_encoding=input_encoding, doctitle=doctitle,
        initial_header_level=initial_header_level)
    fragment = parts['html_body']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding)
    return fragment


class RstExtension(Extension):

    tags = set(['rst'])

    def __init__(self, environment):
        super(RstExtension, self).__init__(environment)
        environment.extend(rst_raw_txt = None)

    def parse(self, parser):
        # the first token is the token that started the tag.  In our case
        # we only listen to ``'cache'`` so this will be a name token with
        # `cache` as value.  We get the line number so that we can give
        # that line number to the nodes we create by hand.
        lineno = parser.stream.next().lineno

        args = []
        if parser.stream.skip_if('comma'):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))
        # now we parse the body of the cache block up to `endcache` and
        # drop the needle (which would always be `endcache` in that case)
        body = parser.parse_statements(['name:endrst'], drop_needle=True)

        # now return a `CallBlock` node that calls our _cache_support
        # helper method on this extension.
        return nodes.CallBlock(self.call_method('_render_rst', args), [], [], body).set_lineno(lineno)

    def _render_rst(self, hdr_lvl, caller):
        if hdr_lvl is not None:
            hdr_lvl = int(hdr_lvl)
        else:
            hdr_lvl = 1
        rv = caller()
        return html_body(rv, doctitle='', initial_header_level=hdr_lvl)

if __name__ == '__main__':
    from jinja2 import Environment
    env = Environment(extensions=[RstExtension])
    tplStr = """Hello {{ user_name }}!
Here's some RST markup:
{% rst,3 %}
My Doc Title:
=============

 *bold*
{% endrst %}
{% rst,1 %}
My Doc Title:
=============

 *bold*
{% endrst %}

"""
    tpl = env.from_string(tplStr)
    print tpl.render({'user_name': 'BlaFasel'})
