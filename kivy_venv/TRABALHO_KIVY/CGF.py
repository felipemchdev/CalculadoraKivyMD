import numpy as np
import matplotlib.pyplot as plt
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
import re

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    canvas:
        Color:
            rgba: 1, 1, 1, 1  # Cor branca
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Calculadora de Gráficos da Função"
        color: 0, 0, 0, 1  # Texto em preto
        size_hint_y: None
        height: self.parent.height * 0.1  # 10% da altura do pai

    MDTextField:
        id: function_input
        hint_text: "Digite a função (ex: f(x) = 3*x**3 + 3*x + 3)"
        mode: "outlined"
        line_color_normal: 0, 0, 1, 1  # Borda azul
        line_color_focus: 0, 0, 1, 1  # Borda azul quando focado
        multiline: False
        size_hint_y: None
        height: self.parent.height * 0.1  # 10% da altura do pai

    Button:
        text: "Gerar Gráfico"
        on_release: app.plot_function()
        size_hint_y: None
        height: self.parent.height * 0.06  # 8% da altura do pai para deixar mais fino
        size_hint_x: 1  # Ocupa toda a largura disponível
        background_color: 0.4, 0.8, 1, 1  # Azul claro
        color: 1, 1, 1, 1  # Texto em branco
        pos_hint: {"center_x": 0.5}  # Centraliza horizontalmente

    Label:
        id: error_label
        text: ""  # Inicialmente vazio
        color: 1, 0, 0, 1  # Texto em vermelho
        size_hint_y: None
        height: self.parent.height * 0.1  # 10% da altura do pai

    Image:
        id: graph_image
        size_hint_y: None
        height: self.parent.height * 0.5  # 50% da altura do pai
        
    Label:
        text: "Feito por Felipe Machado - Versão 1.45"
        color: 0.5, 0.5, 0.5, 1  # Texto em cinza
        size_hint_y: None
        height: self.parent.height * 0.05  # 5% da altura do pai
        halign: "center"
        valign: "middle"
        font_size: '10sp'  # Tamanho de fonte pequeno
'''

class MainApp(MDApp):
    dialog = None

    def build(self):
        self.title = "Calculadora de Gráficos da Função"  # Definindo o título do aplicativo
        root = Builder.load_string(KV)
        Window.bind(size=self.on_size)  # Conectar o redimensionamento da janela
        return root

    def on_size(self, *args):
        # Atualiza o tamanho do fundo sempre que a janela é redimensionada
        pass  # Não precisa de ajustes para este exemplo

    def plot_function(self):
        function_str = self.root.ids.function_input.text

        # Verificar se a entrada está vazia
        if not function_str.strip():
            self.root.ids.error_label.text = "Digite no campo acima!"
            return

        # Verificar se a entrada contém apenas caracteres válidos
        if not re.match(r'^[0-9x\+\-\*\/\.\(\) ]+$', function_str):
            self.root.ids.error_label.text = "Isso não é uma função, apenas letra(s)!"
            return

        self.root.ids.error_label.text = ""  # Limpar mensagem de erro

        # Verificar se a entrada começa com 'f(x) = '
        if function_str.startswith('f(x) = '):
            function_str = function_str[7:]  # Remover 'f(x) = '

        # Substituir potenciação '^' por '**'
        function_str = function_str.replace('^', '**')

        # Substituir multiplicação implícita entre números e 'x'
        function_str = re.sub(r'(?<=[0-9])(?=[x])', '*', function_str)  # Ex: 3x -> 3*x
        function_str = re.sub(r'(?<=[)])(?=[x])', '*', function_str)  # Ex: (x-1)x -> (x-1)*x

        # Remover espaços em branco
        function_str = function_str.replace(' ', '')

        x = np.linspace(-10, 10, 400)
        try:
            # Avaliar a função como uma expressão numérica
            y = eval(function_str)

            # Verificar se y é um valor numérico
            if not isinstance(y, (np.ndarray, list)):
                raise ValueError("A função não retornou um valor válido.")

            # Gerar o gráfico
            plt.figure(figsize=(8, 4))
            plt.plot(x, y)
            plt.title(f'Gráfico de {function_str}')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid()
            plt.axhline(0, color='black', lw=0.5, ls='--')
            plt.axvline(0, color='black', lw=0.5, ls='--')

            # Salvar o gráfico em um buffer de imagem
            plt.savefig('graph.png', bbox_inches='tight', pad_inches=0)  # Ajustando para não deixar espaço
            plt.close()

            # Atualizar a imagem no aplicativo
            self.root.ids.graph_image.source = 'graph.png'
            self.root.ids.graph_image.reload()

        except (SyntaxError, ValueError):
            self.root.ids.error_label.text = "Isso não é uma função válida!"  # Mensagem personalizada para erro
        except Exception as e:
            self.show_error(f"Erro: {str(e)}")

    def show_error(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Erro",
                text=message,
                size_hint=(0.8, 1),
                buttons=[
                    Button(text="Fechar", on_release=self.close_dialog)
                ]
            )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

if __name__ == '__main__':
    MainApp().run()
