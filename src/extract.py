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

if __name__ == "__main__":
    pokemon = fetch_pokemon_list()
    print(f"Fetched {len(pokemon)} Pokémon:")
    print(pokemon[:2])