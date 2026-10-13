import requests
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
if __name__ == "__main__":
    pokemon = fetch_pokemon_list()
    print(f"Fetched {len(pokemon)} Pokémon:")
    print(pokemon[:2])
    
    details = fetch_pokemon_details()
    print(f"Fetched details for {len(details)} Pokémon:")
    print(details[:2])