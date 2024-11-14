from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

# Ігнорування сертифікатів SSL
ssl._create_default_https_context = ssl._create_unverified_context

sparql = SPARQLWrapper('https://dbpedia.org/sparql')

# Запит для отримання назв країн та пов'язаних мов
query = '''
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>

    SELECT ?countryName (GROUP_CONCAT(UCASE(?languageName); separator="|") AS ?languages)
    WHERE {
      ?country dct:subject ?category ;
               rdfs:label ?countryName .
      FILTER (
        LANG(?countryName) = "en" &&
        STRSTARTS(?countryName, "A") &&
        (STRSTARTS(STR(?category), "http://dbpedia.org/resource/Category:European_") ||
         STRSTARTS(STR(?category), "http://dbpedia.org/resource/Category:North_American_"))
      )

      OPTIONAL {
        ?country dbo:language ?language .
        ?language rdfs:label ?languageName .
        FILTER (LANG(?languageName) = "en")
      }
    }
    GROUP BY ?countryName
    ORDER BY ?countryName
'''

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
query_res = sparql.query().convert()

print("Таблиця країн та пов'язаних мов:")
for value in query_res['results']['bindings']:
    country = value['countryName']['value']
    languages = value['languages']['value'] if 'languages' in value else "N/A"
    print(f"{country}: {languages}")
