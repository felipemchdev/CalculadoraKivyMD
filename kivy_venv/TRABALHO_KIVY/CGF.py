import os
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem

Window.size = (450, 800)

KV = '''
MDBoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: "Calculadora"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
        title_align: "left"
        md_bg_color: 0, 0, 0, 1  # Fundo preto
        elevation: 4
        padding: "0dp"

    MDNavigationDrawer:
        id: nav_drawer
        scrim_color: 0, 0, 0, 0.6

        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            MDLabel:
                text: "Menu"
                font_style: "H5"
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Primary"

            OneLineListItem:
                text: "Gráficos de Funções"
                on_release: 
                    nav_drawer.set_state("close")
                    screen_manager.current = "graph_calculator"
                theme_text_color: "Primary"

            OneLineListItem:
                text: "Calculadora"
                on_release: 
                    nav_drawer.set_state("close")
                    screen_manager.current = "basic_calculator"
                theme_text_color: "Primary"

            OneLineListItem:
                text: "Tema"
                on_release: 
                    app.toggle_theme()  
                    nav_drawer.set_state("close")
                theme_text_color: "Primary"

            OneLineListItem:
                text: "Sobre"
                on_release: 
                    nav_drawer.set_state("close")
                    screen_manager.current = "about"
                theme_text_color: "Primary"

    ScreenManager:
        id: screen_manager

        Screen:
            name: "graph_calculator"
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10), dp(20), dp(10), dp(10)
                spacing: dp(20)

                MDTextField:
                    id: function_input
                    hint_text: "Digite a função ex: f(x) = 3x^2 + 2x + 5"
                    mode: "rectangle"
                    multiline: False
                    size_hint_y: None
                    height: self.parent.height * 0.1

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
                    size_hint_y: 0.6
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
                    cols: 4  # Com 4 colunas
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
        pass

    def toggle_theme(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

    def update_display(self, value):
        current_text = self.root.ids.calculator_display.text
        if value == "C":
            self.root.ids.calculator_display.text = ""
        else:
            self.root.ids.calculator_display.text = current_text + value

    def calculate_result(self):
        try:
            expression = self.root.ids.calculator_display.text
            result = str(eval(expression))
            self.root.ids.calculator_display.text = result
        except Exception as e:
            self.root.ids.calculator_display.text = "Erro"

    def on_app_close(self, *args):
        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)
        return False

if __name__ == "__main__":
    MainApp().run()
