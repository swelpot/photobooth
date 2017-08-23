import argparse
import warnings
import json
import pprint
import logging
import kivy
from kivy.uix.button import Button

kivy.require('1.10.0')

from kivy.app import App

class MainApp(App):

    def build(self):
        button = Button(text='Hello world', font_size=14)
        button.bind(on_press=self.callback)


        return button

    def callback(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        exit(0)


if __name__ == '__main__':
    mainApp = MainApp()
    mainApp.run()
