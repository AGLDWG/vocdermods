from textwrap import dedent
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, SKOS
REG = Namespace("http://purl.org/linked-data/registry#")

g = Graph().parse("../rdf/_vocabulary.ttl")


def make_jekyll_header(file_name):
    return f"""---
permalink: /{file_name}.ttl
---
"""


def make_concept_markdown(pref_label, permalink, iri, definition):
    return dedent(
        f"""        ---
        layout: page
        title: {pref_label}
        permalink: /{permalink}
        ---
        # Concept
        
        ## {pref_label}
        
        `{iri}`
        
        {definition}
        
        **Property** | **Value**
        --- | ---
        _Status_ | [Original](https://linked.data.gov.au/def/reg-statuses/original)
        _In Scheme_ | [Vocab Derivation Modes]({{ site.baseurl }}/)
        """)


# make individual Concept RDF files
for s in g.subjects(RDF.type, SKOS.Concept):
    fn = str(s).split("/")[-1]
    cbd = g.cbd(s)

    with open(f"../rdf/{fn}.ttl", "w") as f:
        f.write(make_jekyll_header(fn))
        cbd.bind("reg", REG)
        f.write(cbd.serialize(format="longturtle"))

    with open(f"../md/{fn}.md", "w") as f:
        f.write(make_concept_markdown(
            cbd.value(s, SKOS.prefLabel),
            fn,
            str(s),
            cbd.value(s, SKOS.definition)
        ))



# make Jekyll-ready vocab
txt = make_jekyll_header("vocabulary")
txt += g.serialize(format="longturtle")
with open(f"../rdf/vocabulary.ttl", "w") as f:
    f.write(txt)

# make