import os
import matplotlib.pyplot as plt
import numpy as np
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout

Window.size = (450, 800)

KV = '''
MDBoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: "Calculadora"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
        md_bg_color: 0, 0, 0, 1  # Barra superior preta
        elevation: 4
        size_hint_y: None  # Impede o comportamento automático de altura
        height: "40dp"  # Barra superior mais fina
        title_font_size: "16sp"  # Tamanho do texto reduzido
        title_align: "left"  # Alinhamento à esquerda
        padding: "10dp"  # Ajustando o padding para deixar mais compacto

    MDNavigationDrawer:
        id: nav_drawer
        scrim_color: 0, 0, 0, 0.6
        width: "220dp"
        size_hint_y: None
        height: self.minimum_height

        BoxLayout:
            orientation: 'vertical'
            height: dp(0)
            spacing: dp(0)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "Menu"
                font_style: "H5"
                size_hint_y: None
                height: dp(10)
                height: self.texture_size[1]
                theme_text_color: "Primary"
                padding: dp(0)

            OneLineListItem:
                text: "Gráficos de Funções"
                on_release: 
                    nav_drawer.set_state("close")
                    app.animate_graph_up()
                    screen_manager.current = "graph_calculator"
                theme_text_color: "Primary"

            OneLineListItem:
                text: "Calculadora"
                on_release: 
                    nav_drawer.set_state("close")
                    app.animate_graph_up()
                    screen_manager.current = "basic_calculator"
                theme_text_color: "Primary"

            OneLineListItem:
                text: "Tema"
                on_release: 
                    app.toggle_theme()  
                    nav_drawer.set_state("close")
                    app.animate_graph_up()
                theme_text_color: "Primary"

            OneLineListItem:
                text: "Sobre"
                on_release: 
                    nav_drawer.set_state("close")
                    app.animate_graph_up()
                    screen_manager.current = "about"
                theme_text_color: "Primary"

    ScreenManager:
        id: screen_manager

        Screen:
            name: "graph_calculator"
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10), dp(20), dp(10), dp(10)
                spacing: dp(10)

                MDTextField:
                    id: function_input
                    hint_text: "Digite a função ex: f(x) = 3x^2 + 2x + 5"
                    mode: "rectangle"
                    multiline: False
                    size_hint_y: None
                    height: dp(50)  # Altura fixa para o campo de entrada
                    padding_y: dp(10)  # Espaçamento do texto dentro da caixa de texto

                MDRaisedButton:
                    text: "Gerar Gráfico"
                    on_release: app.plot_function()
                    size_hint_y: None
                    height: self.parent.height * 0.06
                    size_hint_x: 1

                MDLabel:
                    id: error_label
                    text: ""
                    theme_text_color: "Error"
                    size_hint_y: None
                    height: self.parent.height * 0.1

                Image:
                    id: graph_image
                    size_hint_y: None
                    height: self.parent.height * 0.5
                    size_hint_x: 1
                    opacity: 0

                MDLabel:
                    text: "Versão 1.88"
                    color: 0.5, 0.5, 0.5, 1
                    size_hint_y: None
                    height: self.parent.height * 0.05
                    halign: "center"
                    font_size: '10sp'

        Screen:
            name: "basic_calculator"
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(20)

                MDTextField:
                    id: calculator_display
                    hint_text: ""
                    font_size: '24sp'
                    halign: "right"
                    size_hint_y: None
                    height: dp(50)

                GridLayout:
                    cols: 4
                    spacing: dp(10)
                    padding: dp(10)
                    size_hint_x: None
                    width: self.parent.width * 0.82 
                    pos_hint: {"right": 1} 

                    MDFlatButton:
                        text: "C"
                        on_release: app.update_display("C")
                        theme_text_color: "Error"
                    MDFlatButton:
                        text: "()"
                        on_release: app.update_display("()")
                    MDFlatButton:
                        text: "%"
                        on_release: app.update_display("%")
                    MDFlatButton:
                        text: "/"
                        on_release: app.update_display("/")

                    MDFlatButton:
                        text: "7"
                        on_release: app.update_display("7")
                    MDFlatButton:
                        text: "8"
                        on_release: app.update_display("8")
                    MDFlatButton:
                        text: "9"
                        on_release: app.update_display("9")
                    MDFlatButton:
                        text: "x"
                        on_release: app.update_display("*")

                    MDFlatButton:
                        text: "4"
                        on_release: app.update_display("4")
                    MDFlatButton:
                        text: "5"
                        on_release: app.update_display("5")
                    MDFlatButton:
                        text: "6"
                        on_release: app.update_display("6")
                    MDFlatButton:
                        text: "-"
                        on_release: app.update_display("-")

                    MDFlatButton:
                        text: "1"
                        on_release: app.update_display("1")
                    MDFlatButton:
                        text: "2"
                        on_release: app.update_display("2")
                    MDFlatButton:
                        text: "3"
                        on_release: app.update_display("3")
                    MDFlatButton:
                        text: "+"
                        on_release: app.update_display("+")

                    MDFlatButton:
                        text: "+/-"
                        on_release: app.update_display("+/-")
                    MDFlatButton:
                        text: "0"
                        on_release: app.update_display("0")
                    MDFlatButton:
                        text: ","
                        on_release: app.update_display(",")
                    MDFlatButton:
                        text: "="
                        on_release: app.calculate_result()

        Screen:
            name: "about"
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(20)

                MDLabel:
                    text: "Sobre"
                    halign: "center"
                    font_style: "H5"
                    size_hint_y: None
                    height: self.parent.height * 0.1

                MDLabel:
                    text: "Calculadora com Kivy - Feito por Felipe Machado"
                    halign: "center"
                    size_hint_y: None
                    height: self.parent.height * 0.1
'''

class MainApp(MDApp):
    temp_image_path = "temp_graph.png"

    def build(self):
        self.title = "Calculadora"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"
        Window.bind(on_request_close=self.on_app_close)
        app_interface = Builder.load_string(KV)
        
        app_interface.ids.screen_manager.current = "basic_calculator"
        
        app_interface.ids.nav_drawer.set_state("close")
        
        return app_interface

    def plot_function(self):
        import matplotlib.pyplot as plt
        import numpy as np

        func_input = self.root.ids.function_input.text.strip()

        if not func_input:
            self.root.ids.error_label.text = "Por favor, insira uma função!"
            self.root.ids.graph_image.opacity = 0
            return

        self.root.ids.error_label.text = ""

        try:
            x = np.linspace(-10, 10, 400)
            y = x**2  # Exemplo de uma função quadrática f(x) = x^2

            plt.plot(x, y)
            plt.title("Gráfico da Função")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.grid(True)

            # Salvar a imagem do gráfico
            plt.savefig(self.temp_image_path)
            plt.close()

            # Carregar a imagem no Kivy
            self.root.ids.graph_image.source = self.temp_image_path
            self.root.ids.graph_image.opacity = 1

        except Exception as e:
            self.root.ids.error_label.text = f"Erro: {e}"
            self.root.ids.graph_image.opacity = 0

    def update_display(self, value):
        display = self.root.ids.calculator_display
        current_text = display.text

        if value == "C":
            display.text = ""
        elif value == "+/-":
            display.text = "-" + current_text if current_text[0] != '-' else current_text[1:]
        elif value == "()":
            display.text += "()"
        else:
            display.text += value

    def calculate_result(self):
        display = self.root.ids.calculator_display
        try:
            result = eval(display.text)
            display.text = str(result)
        except Exception:
            display.text = "Erro!"

    def on_app_close(self, *args):
        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def animate_graph_up(self):
        animation = Animation(pos_hint={"top": 1}, duration=0.3)
        animation.start(self.root.ids.graph_image)

    def toggle_theme(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

MainApp().run()
