from pathlib import Path
from pylode.profiles.ontpub import OntPub

REPO_DIR = Path(__file__).parent.parent.resolve()

# initialise
od = OntPub(ontology=REPO_DIR / "model.ttl")

# make HTML
html = od.make_html()

# post-process HTML to put in images
# deduplicate id="bore"
before = '''<dl>
          <dt id="bore">bore</dt>'''
after = '''<dl>
          <dt id="b">bore</dt>'''
html = html.replace(before, after)

# remove title
html = html.replace('<h1>Bore Model</h1>\n',  '')

# add overview figure
concepts_img = f'''<div id="content">
      <h1>Geosamples Model</h1>
      <img src="img/overview.svg" style="width:600px;" /> 
'''
html = html.replace('<div id="content">', concepts_img)

from rdflib import Graph
from rdflib.namespace import SDO
from markdown import markdown
g = Graph().parse("model.ttl")
for o in g.objects(None, SDO.abstract):
    abstract = str(o)
abstract_section = f'''<div class="section" id="abstract">
<h2>Introduction</h2>
{markdown(abstract)}
</div>
'''
html = html.replace('<div class="section" id="classes">', abstract_section)

import re
html = re.sub(r'<p>[\s]*<code>', '<pre><code>', html)
html = re.sub(r'</code>[\s]*</p>', '</code></pre>', html)
# write HTML to file
open(REPO_DIR / "model.html", "w").write(html)
