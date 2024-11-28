import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD


# Функція для виконання SPARQL запиту
def execute_sparql_query(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


# SPARQL запит
query = """
SELECT ?country ?countryName (GROUP_CONCAT(DISTINCT UCASE(?language); separator="|") AS ?languages)
WHERE {
  ?country a dbo:Country .
  ?country dbo:continent ?continent .
  ?country rdfs:label ?countryName FILTER (lang(?countryName) = "en") .
  ?country dbo:language ?languageResource .
  ?languageResource rdfs:label ?language FILTER (lang(?language) = "en") .

  FILTER((?continent = "Europe"@en || ?continent = "North America"@en) && STRSTARTS(?countryName, "A"))
}
GROUP BY ?country ?countryName
ORDER BY ?countryName
"""

# Виконання запиту і обробка результатів
results = execute_sparql_query(query)

# Конвертація результатів у DataFrame
data = []
for result in results["results"]["bindings"]:
    country = result["country"]["value"]
    country_name = result["countryName"]["value"]
    languages = result["languages"]["value"]
    data.append([country, country_name, languages])

df = pd.DataFrame(data, columns=["Country", "CountryName", "Languages"])
print(df)

# Ініціалізація графа
g = Graph()

EX = Namespace("http://example.org/")
g.bind("ex", EX)

# Інформація про Кейда
kade = EX.Kade
g.add((kade, RDF.type, FOAF.Person))
g.add((kade, FOAF.name, Literal("Kade")))
g.add((kade, EX.livesAt, Literal("1516 Henry Street, Berkeley, California 94709, USA")))
g.add((kade, EX.degree, Literal("Bachelor of Biology", datatype=XSD.string)))
g.add((kade, EX.interests, Literal("birds, ecology, environment, photography, travel", datatype=XSD.string)))
g.add((kade, EX.visited, Literal("Canada, France", datatype=XSD.string)))

# Інформація про Емму
emma = EX.Emma
g.add((emma, RDF.type, FOAF.Person))
g.add((emma, FOAF.name, Literal("Emma")))
g.add((emma, EX.livesAt, Literal("Carrer de la Guardia Civil 20, 46020 Valencia, Spain")))
g.add((emma, EX.degree, Literal("Master of Chemistry", datatype=XSD.string)))
g.add((emma, EX.knowledge, Literal("waste management, toxic waste, air pollution", datatype=XSD.string)))
g.add((emma, EX.interests, Literal("cycling, music, travel", datatype=XSD.string)))
g.add((emma, EX.visited, Literal("Portugal, Italy, France, Germany, Denmark, Sweden", datatype=XSD.string)))
g.add((emma, EX.age, Literal(36, datatype=XSD.integer)))

# Зв'язок між Кейдом і Еммою
g.add((kade, FOAF.knows, emma))
g.add((kade, EX.metIn, Literal("Paris, August 2014", datatype=XSD.string)))

# Додавання додаткової інформації
g.add((kade, EX.visited, Literal("Germany", datatype=XSD.string)))  # Кейд відвідав Німеччину

print("Трійці")
# Виведення трійок
for s, p, o in g:
    print(s, p, o)

# Виведення трійок, що стосуються лише Емми
print("Трійці Емми")
for s, p, o in g.triples((emma, None, None)):
    print(s, p, o)

print("Трійці з іменами людей")
# Виведення трійок, що містять імена людей
for s, p, o in g.triples((None, FOAF.name, None)):
    print(s, p, o)

# Збереження графа у файл у форматі TURTLE
g.serialize(destination="graph.ttl", format="turtle")
