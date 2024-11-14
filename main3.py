from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

# Ігнорування сертифікатів SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Ініціалізація об'єкта SPARQLWrapper для DBpedia
sparql = SPARQLWrapper('https://dbpedia.org/sparql')

# 1. Список усіх лауреатів Нобелівської премії з фізики в порядку від найстаршого до наймолодшого
query_oldest_to_youngest = '''
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT ?laureate ?birthDate
    WHERE {
      ?laureate dbo:award dbr:Nobel_Prize_in_Physics ;
                dbo:birthDate ?birthDate .
    }
    ORDER BY ASC(?birthDate)
'''

sparql.setQuery(query_oldest_to_youngest)
sparql.setReturnFormat(JSON)
result_oldest_to_youngest = sparql.query().convert()

print("Лауреати Нобелівської премії з фізики від найстаршого до наймолодшого:")
for result in result_oldest_to_youngest['results']['bindings']:
    laureate = result['laureate']['value']
    birth_date = result['birthDate']['value']
    print(f"{laureate}: {birth_date}")

# 2. Топ 10 університетів з найбільшою кількістю лауреатів Нобелівської премії з фізики
query_top_10_universities = '''
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT ?university (COUNT(?laureate) AS ?numLaureates)
    WHERE {
      ?laureate dbo:award dbr:Nobel_Prize_in_Physics ;
                dbo:almaMater ?university .
    }
    GROUP BY ?university
    ORDER BY DESC(?numLaureates)
    LIMIT 10
'''

sparql.setQuery(query_top_10_universities)
sparql.setReturnFormat(JSON)
result_top_10_universities = sparql.query().convert()

print("\nТоп 10 університетів з найбільшою кількістю лауреатів Нобелівської премії з фізики:")
for result in result_top_10_universities['results']['bindings']:
    university = result['university']['value']
    num_laureates = result['numLaureates']['value']
    print(f"{university}: {num_laureates}")

# 3. Кількість лауреатів Нобелівської премії з фізики, які є іммігрантами
query_immigrant_laureates = '''
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT (COUNT(?laureate) AS ?immigrantCount)
    WHERE {
      ?laureate dbo:award dbr:Nobel_Prize_in_Physics ;
                dbo:birthPlace ?birthCountry ;
                dbo:almaMater ?university .
      ?university dbo:country ?universityCountry .
      FILTER (?birthCountry != ?universityCountry)
    }
'''

sparql.setQuery(query_immigrant_laureates)
sparql.setReturnFormat(JSON)
result_immigrant_laureates = sparql.query().convert()

immigrant_count = result_immigrant_laureates['results']['bindings'][0]['immigrantCount']['value']
print(f"\nКількість лауреатів Нобелівської премії з фізики, які є іммігрантами: {immigrant_count}")
