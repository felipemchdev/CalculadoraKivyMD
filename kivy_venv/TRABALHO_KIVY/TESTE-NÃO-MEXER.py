from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.screenmanager import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import OneLineListItem

KV = '''
ScreenManager:
    HomeScreen:
    ProductListScreen:
    ProductDetailScreen:
    CartScreen:
    ProfileScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10

        MDTopAppBar:
            title: "Mercado do Verde"
            left_action_items: [["menu", lambda x: app.toggle_menu()]]
            md_bg_color: 0, 0, 0, 1  # Fundo escuro
            specific_text_color: 0, 1, 0, 1  # Verde para o texto
            right_action_items: [["magnify", lambda x: app.on_search_click()]]

        MDTextField:
            id: search_field
            hint_text: "Pesquisar produtos"
            size_hint: 1, None
            height: "40dp"
            pos_hint: {"center_x": 0.5}
            on_text_validate: app.search_products()
        
        ScrollView:
            MDGridLayout:
                cols: 2
                padding: "10dp"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height
                MDCard:
                    size_hint: None, None
                    size: "280dp", "380dp"
                    pos_hint: {"center_x": 0.5}
                    elevation: 10
                    on_release: app.show_product_list("Categoria 1")
                    BoxLayout:
                        orientation: "vertical"
                        MDLabel:
                            text: "Categoria 1"
                            theme_text_color: "Secondary"
                            size_hint_y: None
                            height: "48dp"
                        MDRaisedButton:
                            text: "Ver Produtos"
                            size_hint: None, None
                            size: "200dp", "50dp"
                            pos_hint: {"center_x": 0.5}

<ProductListScreen>:
    name: "product_list"
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Lista de Produtos"
            left_action_items: [["arrow-left", lambda x: app.change_screen("home")]]
            md_bg_color: 0, 0, 0, 1  # Fundo escuro
            specific_text_color: 0, 1, 0, 1  # Verde para o texto
        
        ScrollView:
            MDGridLayout:
                cols: 2
                padding: "10dp"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height
                id: product_grid
                # Os produtos serão adicionados aqui com base no filtro

<ProductDetailScreen>:
    name: "product_detail"
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Detalhes do Produto"
            left_action_items: [["arrow-left", lambda x: app.change_screen("product_list")]]
            md_bg_color: 0, 0, 0, 1  # Fundo escuro
            specific_text_color: 0, 1, 0, 1  # Verde para o texto
        
        MDLabel:
            text: "Detalhes do Produto"
            halign: "center"
            theme_text_color: "Secondary"
        
        MDLabel:
            text: "Descrição do Produto"
            halign: "center"
            theme_text_color: "Primary"
        
        MDRaisedButton:
            text: "Adicionar ao Carrinho"
            size_hint: None, None
            size: "250dp", "50dp"
            pos_hint: {"center_x": 0.5}
            on_release: app.add_to_cart()

<CartScreen>:
    name: "cart"
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Carrinho de Compras"
            left_action_items: [["arrow-left", lambda x: app.change_screen("home")]]
            md_bg_color: 0, 0, 0, 1  # Fundo escuro
            specific_text_color: 0, 1, 0, 1  # Verde para o texto
        
        MDLabel:
            text: "Itens no Carrinho"
            halign: "center"
            theme_text_color: "Secondary"
        
        MDLabel:
            text: "Produto 1 - R$ 99,99"
            theme_text_color: "Primary"
            halign: "center"
        
        MDRaisedButton:
            text: "Finalizar Compra"
            size_hint: None, None
            size: "250dp", "50dp"
            pos_hint: {"center_x": 0.5}

<ProfileScreen>:
    name: "profile"
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Perfil"
            left_action_items: [["arrow-left", lambda x: app.change_screen("home")]]
            md_bg_color: 0, 0, 0, 1  # Fundo escuro
            specific_text_color: 0, 1, 0, 1  # Verde para o texto
        
        MDLabel:
            text: "Cadastro de Usuário"
            halign: "center"
            theme_text_color: "Secondary"
        
        MDTextField:
            hint_text: "Nome"
            size_hint: 1, None
            height: "40dp"
        
        MDTextField:
            hint_text: "Email"
            size_hint: 1, None
            height: "40dp"
        
        MDTextField:
            hint_text: "Senha"
            size_hint: 1, None
            height: "40dp"
        
        MDRaisedButton:
            text: "Cadastrar"
            size_hint: None, None
            size: "250dp", "50dp"
            pos_hint: {"center_x": 0.5}
'''

class HomeScreen(Screen):
    pass

class ProductListScreen(Screen):
    def update_product_list(self, products):
        product_grid = self.ids.product_grid
        product_grid.clear_widgets()

        for product in products:
            product_card = MDCard(
                size_hint=(None, None),
                size=("280dp", "380dp"),
                pos_hint={"center_x": 0.5},
                elevation=10,
                on_release=lambda product_name=product["name"]: MDApp.get_running_app().show_product_details(product_name)  # Correção
            )
            box_layout = BoxLayout(orientation="vertical")
            box_layout.add_widget(MDLabel(text=product["name"], theme_text_color="Secondary", size_hint_y=None, height="48dp"))
            box_layout.add_widget(MDRaisedButton(text=f"R$ {product['price']}", size_hint=(None, None), size=("200dp", "50dp"), pos_hint={"center_x": 0.5}))

            product_card.add_widget(box_layout)
            product_grid.add_widget(product_card)

class ProductDetailScreen(Screen):
    pass

class CartScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class MyApp(MDApp):
    cart = []
    search_query = ""
    all_products = [
        {"name": "Produto 1", "category": "Categoria 1", "price": "99,99"},
        {"name": "Produto 2", "category": "Categoria 1", "price": "89,99"},
        {"name": "Produto 3", "category": "Categoria 2", "price": "79,99"},
        {"name": "Produto 4", "category": "Categoria 2", "price": "69,99"},
    ]
    filtered_products = all_products

    def build(self):
        self.theme_cls.primary_palette = "Green"  # Cor verde para o tema
        self.theme_cls.theme_style = "Dark"  # Tema escuro

        # Menu de navegação
        self.nav_drawer = MDNavigationDrawer()
        self.nav_drawer.add_widget(BoxLayout())  # Apenas um espaço por enquanto, pode ser substituído por conteúdo

        # Inicializando a tela principal
        screen = Builder.load_string(KV)
        return screen

    def on_search_click(self):
        self.search_query = self.root.get_screen("home").ids.search_field.text
        print(f"Searching for: {self.search_query}")
        self.filter_products()
        self.change_screen("product_list")

    def search_products(self):
        print(f"Search query: {self.search_query}")
        self.filter_products()
        self.change_screen("product_list")

    def filter_products(self):
        if self.search_query:
            self.filtered_products = [product for product in self.all_products if self.search_query.lower() in product["name"].lower()]
        else:
            self.filtered_products = self.all_products
        self.root.get_screen("product_list").update_product_list(self.filtered_products)

    def show_product_list(self, category):
        self.filtered_products = [product for product in self.all_products if product["category"] == category]
        self.change_screen("product_list")

    def show_product_details(self, product_name):
        # Mostra os detalhes do produto
        self.change_screen("product_detail")

    def add_to_cart(self):
        # Adiciona um produto ao carrinho
        self.cart.append("Produto 1")  # Apenas um exemplo
        self.change_screen("cart")

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def toggle_menu(self):
        # Toggle do menu
        if self.nav_drawer.state == "open":
            self.nav_drawer.set_state("close")
        else:
            self.nav_drawer.set_state("open")

if __name__ == "__main__":
    MyApp().run()
