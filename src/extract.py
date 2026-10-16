import requests
import csv
import gzip
from io import StringIO
import boto3
import duckdb
from botocore import UNSIGNED
from botocore.client import Config

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

def fetch_pokemon_list(limit: int = 151) -> list[dict]:
    """
    Fetches a list of Pokémon from the PokeAPI.

    Args:
        limit (int): The number of Pokémon to fetch. Default is 150."""
        
    response = requests.get(POKEAPI_URL, params={"limit": limit}, timeout=30)
    response.raise_for_status()
    return response.json()["results"]
POKEAPI_GRAPHQL_URL = "https://graphql.pokeapi.co/v1beta2"
POKEMON_DETAILS_QUERY = """
    query PokemonDetails($limit: Int!) {
    pokemon(limit: $limit, order_by: {id: asc}) {
    id
    name
    base_experience
    height
    weight
  }
}
"""
def fetch_pokemon_details(limit: int = 151) -> list[dict]:
    """
    Return id, name, base_experience, height and weight for the first `limit` Pokemon.

    Args:
        limit (int): The number of Pokémon to fetch. Default is 150.
    """
    response = requests.post(
        POKEAPI_GRAPHQL_URL,
        json={"query": POKEMON_DETAILS_QUERY, "variables": {"limit": limit}},
        timeout=30
    )
    response.raise_for_status()
    return response.json()["data"]["pokemon"]

NOAA_BUCKET = "noaa-ghcn-pds"
WEATHER_COLUMNS = [
    "id", "date", "element", "value",
    "mflag", "qflag", "sflag", "obs_time"
]

def fetch_weather(station_id: str="ASN00002022") -> list[dict]:
    """
    Fetches weather data for a given station from NOAA's GHCN dataset.

    Args:
        station_id (str): The station ID to fetch data for. Default is "ASN00002022".
    """
    file_key = f"csv.gz/by_station/{station_id}.csv.gz"
    s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    response = s3_client.get_object(Bucket=NOAA_BUCKET, Key=file_key)
    compressed_data = response['Body'].read()

    csv_text = gzip.decompress(compressed_data).decode('utf-8')
    reader = csv.DictReader(StringIO(csv_text), fieldnames=WEATHER_COLUMNS)
    return list(reader)

def read_local_csv(path: str) -> duckdb.DuckDBPyRelation:
    """
Read a CSV file with DuckDB. Column types are inferred automatically.

    Args:
        path (str): The path to the local CSV file.
    """
    return duckdb.read_csv(path)

if __name__ == "__main__":
    pokemon = fetch_pokemon_list()
    print(f"Fetched {len(pokemon)} Pokémon:")
    print(pokemon[:2])
    
    details = fetch_pokemon_details()
    print(f"Fetched details for {len(details)} Pokémon:")
    print(details[:2])
    
    weather = fetch_weather()
    print(f"Fetched {len(weather)} weather records:")
    print(weather[:2])
    
    orders = read_local_csv("data/orders.csv")
    print(orders.columns)
    print(orders.types)
    orders.limit(5).show()
    
    # DuckDb can also query a file directly with plain SQL
    
    duckdb.sql("SELECT COUNT(*) AS total_orders FROM 'data/orders.csv'").show()