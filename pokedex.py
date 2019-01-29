import anydbm
import pickle
from Tkinter import *
from ttk import Combobox, Progressbar
import urllib
from PIL import ImageTk, Image
import search_engine
import pokemon


class Ui(Frame):  # Implementation of Ui class which represents the main frame.
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.DATABASE = 'pokemon.db'
        self.engine = search_engine.PokemonSearchEngine()
        self.search_key = StringVar()
        self.pokemons = dict()
        self.pokemon_types = ['All Types']
        self.COLOR_CHART = {'Bug': 'olive drab', 'Dragon': 'tomato', 'Electric': 'gold', 'Fairy': 'HotPink1',
                            'Fighting': 'orange red', 'Fire': 'dark orange', 'Flying': 'deep sky blue',
                            'Ghost': 'dark violet', 'Grass': 'yellow green', 'Ground': 'goldenrod', 'Ice': 'cyan',
                            'Normal': 'gray', 'Poison': 'medium orchid', 'Psychic': 'hot pink',
                            'Rock': 'saddle brown', 'Steel': 'lightgrey', 'Water': 'steel blue'}

        self.init_ui()

    # UI Generator Functions
    def init_ui(self):
        frm_options = Frame(self)
        frm_title = Frame(frm_options, bg='red', highlightbackground="black", highlightthickness=2)
        frm_fetch = Frame(frm_options, bg='red', highlightbackground="black", highlightthickness=2)
        frm_search = Frame(frm_options, bg='red', highlightbackground="black", highlightthickness=2)
        frm_filter = Frame(frm_search,  bg='red')
        frm_filter_label = Frame(frm_filter, bg='red')
        frm_results = Frame(frm_options, bg='red', highlightbackground="black", highlightthickness=2)
        frm_pokemon = Frame(frm_results, bg='red')
        Label(frm_title, text='POKEDEX', bg='red', fg='white', font='Calibri 20 bold')\
            .pack(fill=X)

        Button(frm_fetch, text='Fetch Pokemon\nData', bg='yellow',
               command=self.btn_fetchdata_onclick).pack(side=LEFT, padx=5, pady=20)
        self.progress = Progressbar(frm_fetch, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(fill=X, padx=15, pady=30, expand=True)
        self.lbl_progress = Label(self.progress, text='')
        self.lbl_progress.pack(pady=5)
        Label(frm_search, text='Search&Filtering', bg='red', font='Calibri 15 bold')\
            .pack()
        Entry(frm_search, textvariable=self.search_key, width=40)\
            .pack(fill=X, padx=15, pady=15)
        Label(frm_filter_label, text='Filter By Type', bg='red', font='Calibri 12')\
            .pack(side=LEFT, padx=5)
        frm_filter_label.pack(side=TOP, fill=X)
        self.cb_filter_type = Combobox(frm_filter)
        self.cb_filter_type.pack(side=LEFT, fill=X, padx=5, pady=5, expand=True)
        Button(frm_filter, text='SEARCH', bg='yellow',
               command=self.btn_search_onclick).pack(side=RIGHT, fill=X, padx=10)

        self.lbl_result = Label(frm_results, text='Total Number Of Results', bg='red', font='Calibri 13 bold')
        self.lbl_result.pack()
        self.lb_pokemons = Listbox(frm_pokemon)
        self.lb_pokemons.pack(side=LEFT, padx=20, pady=10)
        Button(frm_pokemon, text='Get Pokemon\nData', bg='yellow',
               command=self.btn_getpokemon_onclick).pack(side=RIGHT, padx=10)

        frm_options.pack(side=LEFT, fill=BOTH, expand=True)
        frm_title.pack(fill=X)
        frm_fetch.pack(fill=X)
        frm_search.pack(fill=X)
        frm_filter.pack(fill=X)
        frm_results.pack(fill=X)
        frm_pokemon.pack(fill=X)
        self.pack(fill=BOTH, expand=True)

    def pack_pokemon_detail(self, pokemon):
        self.frm_detail = Frame(self, bg='red', highlightbackground="black", highlightthickness=2)

        Label(self.frm_detail, text=pokemon.name, bg='red', font='Calibri 18 bold').pack()
        Label(self.frm_detail, text=pokemon.id, bg='red', font='Calibri 13 bold').pack()
        cnvs_img = Canvas(self.frm_detail, bg='red')
        urllib.urlretrieve(pokemon.img, '1.png')
        cnvs_img.pack(fill=Y)
        Img = Image.open('1.png')
        Img = Img.resize((400, 250))
        self.c = ImageTk.PhotoImage(Img)
        cnvs_img.create_image(0, 0, anchor=NW, image=self.c)
        for type in pokemon.type:
            Label(self.frm_detail, text=type, bg=self.COLOR_CHART[type], width=20, font='Calibri 10 bold').pack()
        Label(self.frm_detail, text='Height: '+pokemon.height, bg='red', font='Calibri 10 bold').pack()
        Label(self.frm_detail, text='Weight: '+pokemon.weight, bg='red', font='Calibri 10 bold').pack()
        Label(self.frm_detail, text='Category: '+pokemon.category, bg='red', font='Calibri 10 bold').pack()
        Label(self.frm_detail, text='Ability: '+pokemon.ability, bg='red', font='Calibri 10 bold').pack()
        Label(self.frm_detail, text='Weakness: '+', '.join(pokemon.weakness), bg='red', font='Calibri 10 bold').pack()
        self.frm_detail.pack(side=RIGHT, fill=BOTH)

    # GUI Element's Events
    def btn_fetchdata_onclick(self):
        try:
            self.read_from_db(self.DATABASE, self.pokemons)
        except anydbm.error:
            for pokemon in self.load_data('all_pokemon.txt'):
                self.pokemons[pokemon] = self.engine.search(pokemon)
                self.progress['value'] += 0.70
                self.progress.update()
            self.create_database(self.DATABASE, self.pokemons)
        finally:
            self.lbl_progress['text'] = 'FINISHED'
            self.get_pokemon_types()

    def btn_search_onclick(self):
        if self.cb_filter_type.get() == 'All Types':
            source = self.filter_pokemon(self.search_key.get())
        else:
            source = self.filter_pokemon_by_type(self.search_key.get().lower(), self.cb_filter_type.get())

        self.lbl_result['text'] = 'Total: '+str(len(source))+' Result'
        self.clear_and_insert_to_listbox(self.lb_pokemons, source)

    def btn_getpokemon_onclick(self):
        try:
            self.frm_detail.pack_forget()
        except:
            print 'All Calculated, No Problem'
        finally:
            self.pack_pokemon_detail(
                 self.pokemons[self.lb_pokemons.get(ACTIVE)]
            )

    # Utilities
    def filter_pokemon_by_type(self, query_string, type):
        results = []
        for pokemon_name, pokemon_object in self.pokemons.items():
            if query_string in pokemon_name.lower() and type in pokemon_object.type:
                results.append(pokemon_name)

        return sorted(results)

    def filter_pokemon(self, query_string):
        results = []
        for pokemon_name, pokemon_object in self.pokemons.items():
            if query_string in pokemon_name:
                results.append(pokemon_name)

        return sorted(results)

    def get_pokemon_types(self):
        for pokemon, pokemon_object in self.pokemons.items():
            for type in pokemon_object.type:
                if type not in self.pokemon_types:
                    self.pokemon_types.append(type)
        self.cb_filter_type['values'] = sorted(self.pokemon_types)
        self.cb_filter_type.current(0)

    @staticmethod
    def clear_and_insert_to_listbox(listbox, source):
        listbox.delete(0, END)
        for item in source:
            listbox.insert(END, item)

    @staticmethod
    def load_data(filename):
        data = []
        with open(filename, 'r') as file:
            for line in file:
                data.append(line.replace('\n', ''))

        return data

    @staticmethod
    def create_database(filename, datas):
        db = anydbm.open(filename, 'c')
        for key, value in datas.items():
            db[key] = pickle.dumps(value)

    @staticmethod
    def read_from_db(filename, source):
        db = anydbm.open(filename, 'r')
        for pokemon in db:
            source[pokemon] = pickle.loads(db[pokemon])


if __name__ == '__main__':  # Settings about root.
    root = Tk()
    root.title('Selamun Aleykum')
    app = Ui(root)
    root.mainloop()