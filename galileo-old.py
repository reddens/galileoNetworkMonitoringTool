import kivy
import main
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

        self.cols = 1  

        #add widget
        self.add_widget(Label(text="Data"))
        self.code = Label(text=main.funct())
        self.add_widget(self.code)
        

        #add button
        self.start = Button(text="Start", font_size=20)
        self.add_widget(self.start)

        #add button
        self.stop = Button(text="Stop", font_size=20)
        self.add_widget(self.stop)
    
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        self.code.text = main.funct()

class MyApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    MyApp().run()
