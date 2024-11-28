from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD

# Ініціалізація графа
g = Graph()

# Створення тверджень
brass = URIRef("http://example.org/Brass")
copper = URIRef("http://example.org/Copper")
zinc = URIRef("http://example.org/Zinc")
spiegel = URIRef("http://example.org/SPIEGEL")
germany = URIRef("http://example.org/Germany")
essay = URIRef("http://example.org/Essay")
introduction = URIRef("http://example.org/Introduction")
main_body = URIRef("http://example.org/MainBody")
conclusion = URIRef("http://example.org/Conclusion")
pavlo = URIRef("http://example.org/Pavlo")
olena = URIRef("http://example.org/Olena")
kyiv = URIRef("http://example.org/Kyiv")
stefan = URIRef("http://example.org/Stefan")
anna = URIRef("http://example.org/Anna")
ivan = URIRef("http://example.org/Ivan")
rome = URIRef("http://example.org/Rome")

# Додавання трійок у граф
g.add((brass, RDF.type, Literal("Alloy of Copper and Zinc")))
g.add((spiegel, RDF.type, Literal("German news magazine based in Hamburg")))
g.add((essay, RDF.type, Literal("Composed of Introduction, Main Body, and Conclusion")))
g.add((pavlo, FOAF.knows, olena))
g.add((olena, RDF.type, Literal("Says her friend lives in Kyiv")))
g.add((stefan, RDF.type, Literal("Thinks Anna knows he knows her father")))
g.add((ivan, RDF.type, Literal("Knows Rome is the capital of Italy")))

# Виведення трійок
for s, p, o in g:
    print(s, p, o)
