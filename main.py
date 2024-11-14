from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

# Ігнорування сертифікатів SSL
ssl._create_default_https_context = ssl._create_unverified_context

sparql = SPARQLWrapper('https://dbpedia.org/sparql')

query = '''
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>

    SELECT ?country ?population
    WHERE {
      ?country dct:subject dbc:Eastern_Europe ;
               a dbo:Country ;
               dbo:populationTotal ?population .
    }
    ORDER BY DESC(?population)
'''

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
query_res = sparql.query().convert()

print("Населення країн Східної Європи:")
for value in query_res['results']['bindings']:
    country = value['country']['value']
    population = value['population']['value']
    print(f"{country} - чисельність населення: {population}")
