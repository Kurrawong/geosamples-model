from pathlib import Path
import tomllib
from datetime import datetime
from jinja2 import Environment
from rdflib import Graph

REPO_DIR = Path(__file__).parent.parent.resolve()

with open("pyproject.toml", "rb") as f:
    pyproj = tomllib.load(f)

iri = None
q = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT ?iri
    WHERE {
        VALUES ?type {
            owl:Ontology
            skos:ConceptScheme
        }
        ?iri a ?type
    }
    """
g = Graph().parse("model.ttl")
for row in g.query(q):
    iri = row["iri"]

tmp = '''# {{title}}

### v{{version}}

{{description}}

Code Repository at: <{{repository}}>

Published Online at: 

* <{{iri}}>


## Contacts
{% for author in authors|sort() %}
 * {{author}}
{% endfor %}

## License & Rights

{{license}}

&copy; KurrawongAI, {{year}}
'''


environment = Environment()
template = environment.from_string(tmp)
context = {
    "title": pyproj["tool"]["poetry"]["name"],
    "version": pyproj["tool"]["poetry"]["version"],
    "description": pyproj["tool"]["poetry"]["description"],
    "repository": pyproj["tool"]["poetry"]["repository"],
    "iri": iri,
    "authors": pyproj["tool"]["poetry"]["authors"],
    "license": pyproj["tool"]["poetry"]["license"],
    "year": datetime.now().strftime("%Y")
}
mkdn = template.render(context)


open(REPO_DIR / "README.md", "w").write(mkdn)
