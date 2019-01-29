from bs4 import BeautifulSoup
import urllib2
import pokemon

class PokemonSearchEngine:
    def __init__(self):
        self.BASE_URL = 'https://www.pokemon.com/us/pokedex/'

    def search(self, pokemon=''):
        r = urllib2.urlopen(self.BASE_URL+pokemon)
        soup = BeautifulSoup(r.read(), 'html.parser')
        pokemon_details = soup.find('section', attrs={'class': 'section pokedex-pokemon-details'})
        pokemon_titlte = soup.find('div', attrs={'class': 'pokedex-pokemon-pagination-title'})
        pokemon_attrs = pokemon_details.find_all('span', attrs={'class': 'attribute-value'})

        print 'Searchin Now - ' + pokemon

        return Pokemon(self.get_id(pokemon_titlte),
                       pokemon,
                       self.get_img(pokemon_details),
                       self.get_height(pokemon_attrs),
                       self.get_weight(pokemon_attrs),
                       self.get_category(pokemon_attrs),
                       self.get_ability(pokemon_attrs),
                       self.get_type(pokemon_details),
                       self.get_weakness(pokemon_details))

    def get_id(self, soup):
        return soup.find('span', attrs={'class': 'pokemon-number'}).get_text()

    def get_img(self, soup):
        return soup.find('img', attrs={'class': 'active'})['src']

    def get_height(self, soup):
        return soup[0].get_text()

    def get_weight(self, soup):
        return soup[1].get_text()

    def get_category(self, soup):
        return soup[3].get_text()

    def get_ability(self, soup):
        return soup[4].get_text()

    def get_type(self, soup):
        pokemon_type = list()
        for a in soup.find('div', attrs={'class': 'dtm-type'}).ul.find_all('a'):
            pokemon_type.append(a.get_text())
        return pokemon_type

    def get_weakness(self, soup):
        pokemon_weakness = []
        for a in soup.find('div', attrs={'class': 'dtm-weaknesses'}).ul.find_all('span'):
            pokemon_weakness.append(
                a.get_text().replace('\n', '').replace('\t', '').strip(' ')
            )
        return pokemon_weakness