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
html = html.replace('<h1>Geosamples Model</h1>\n',  '')

# add overview figure
concepts_img = f'''<div id="content">
      <h1>Geosamples Model</h1>
      <a href="img/overview.svg"><img src="img/overview.svg" style="width:800px;" /></a>
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
toc_insert = '''<h3>Table of Contents</h3>
    <ul class="first">
        <li>
          <h4>
            <a href="#introduction">Introduction</a>
          </h4>
          <ul class="second">
            <li>
              <a href="#purpose">Purpose</a>
            </li>
            <li>
              <a href="#supermodel">Use within a Supermodel</a>
            </li>
            <li>
              <a href="#sosa-schema">Use of SOSA & schema.org</a>
            </li>
            <li>
              <a href="#qualified">Qualified Relations Pattern & Equivalencies</a>
            </li>
            <li>
              <a href="#specialised-patterns">Specialised Patterns</a>
            </li>
          </ul>
        </li>
'''
html = re.sub(r'<h3>Table of Contents</h3>([\s]+)<ul class="first">', toc_insert, html)

html = re.sub(r'<p>[\s]*<code>', '<pre><code>', html)
html = re.sub(r'</code>[\s]*</p>', '</code></pre>', html)
# write HTML to file
open(REPO_DIR / "model.html", "w").write(html)
