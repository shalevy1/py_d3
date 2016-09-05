# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic)  # , line_cell_magic)
from IPython.display import HTML, display
import re
# import requests
# import zipfile
# import io


# The class MUST call this class decorator at creation time
@magics_class
class D3Magics(Magics):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_id = 0  # Used to ensure that the current group selection is unique.
        # self.initialized = True  # Used to ensure that d3.js is only imported once.

    # Unfortunately there isn't an easy way to perform the substitutions necessary to modify a frame-independent
    # block to work within a Jupyter Notebook, so this idea is sandboxed.
    # @line_magic
    # def block(self, line):
    #     user, gist_id = line.split("/")[-2:]
    #     r = requests.get("https://gist.github.com/{0}/{1}/download".format(user, gist_id))
    #     with zipfile.ZipFile(io.BytesIO(r.content)) as ar:
    #         ar.extractall(".blocks/{0}/".format(user, gist_id))
    #         # This creates e.g. ".blocks/mbostock/3885304-master" in the root directory.
    #         # The appended "-master" is due to the format of the zipped file.
    #         # It's a little unideal, but unsure about whether or not removing it would cause any issues I've kept it
    #         # for the time being (you could easily rename the folder).
    #     with open(".blocks/{0}/{1}-master/index.html".format(user, gist_id), "r") as f:
    #         source = f.read()
    #     # We need to perform a few substutions to make the figure work within a Jupyter Notebook file.
    #     # 1. <body> tags are not allowed within a D3 notebook (one has already been defined and HTML documents only
    #     #    allow one <body> and one <head>), but are probably the most common initial selector of all for defining the
    #     #    initial D3 frame. To fix:
    #     #    >>> <body>                 -->     <g>
    #     #    >>> d3.select("body")      -->     d3.select("g")
    #     #    >>> <body id="foo">        -->     ???
    #     #    >>> <body class="foo">     -->     ???
    #     source = source.replace('<body', '<g id="content"')
    #     source = source.replace("select('body", "select(#content")
    #     source = source.replace('select("body', 'select(#content')
    #     display((user, gist_id, source))

    @cell_magic
    def d3(self, line, cell):
        src = line if line else "3.5.17"
        s = """
<script src="//cdnjs.cloudflare.com/ajax/libs/d3/""" + src + """/d3.js"></script>

<script>
_select = d3.select;

d3.select""" + str(self.max_id) + """ = function(selection) {
    return _select("#d3-cell-""" + str(self.max_id) + """").select(selection);
}
d3.selectAll""" + str(self.max_id) + """ = function(selection) {
    return _select("#d3-cell-""" + str(self.max_id) + """").selectAll(selection);
}
</script>
<g id="d3-cell-""" + str(self.max_id) + """">
    """
        cell = re.sub('d3.select\((?!this)', "d3.select" + str(self.max_id) + "(", cell)
        s += cell + "\n</g>"
        print(s)
        h = HTML(s)
        self.max_id += 1
        display(h)

# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(D3Magics)