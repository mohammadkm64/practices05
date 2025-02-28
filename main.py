from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.switch import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
import matplotlib.pyplot as plt
import json
import os

def calculate_anion_gap(na, cl, hco3):
    if na is None or hco3 is None:
        return None
    return na - (cl + hco3) if cl is not None else na - hco3

def interpret_abg(pH, pCO2, HCO3):
    if pH < 7.35:
        if pCO2 > 45:
            return "Respiratory Acidosis: Consider COPD, drug overdose, or hypoventilation."
        elif HCO3 < 22:
            return "Metabolic Acidosis: Possible causes include DKA, renal failure, or sepsis."
    elif pH > 7.45:
        if pCO2 < 35:
            return "Respiratory Alkalosis: Common causes are hyperventilation, anxiety, or high altitude."
        elif HCO3 > 26:
            return "Metabolic Alkalosis: Possible due to vomiting, diuretics, or excessive antacid use."
    return "ABG appears within normal ranges."

def determine_abg_vbg(pO2, pCO2):
    if pO2 > 75 and 35 <= pCO2 <= 45:
        return "Arterial Blood Gas (ABG)"
    elif pO2 < 50 and pCO2 > 45:
        return "Venous Blood Gas (VBG)"
    return "Unable to determine blood gas type."

class ABGApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"

        self.box = MDBoxLayout(orientation="vertical", padding=10, spacing=10)

        self.toolbar = MDToolbar(title="ABG Analyzer")
        self.toolbar.pos_hint = {"top": 1}
        self.box.add_widget(self.toolbar)

        self.theme_switch = MDSwitch()
        self.theme_switch.bind(active=self.toggle_theme)
        self.box.add_widget(self.theme_switch)

        self.fields = {}
        field_names = ["pH", "pCO2 (mmHg)", "HCO3 (mEq/L)", "PaO2 (mmHg)", "Na (optional)", "Cl (optional)"]
        for name in field_names:
            field = MDTextField(hint_text=f"Enter {name}", mode="rectangle")
            self.fields[name] = field
            self.box.add_widget(field)

        self.interpret_button = MDRaisedButton(text="Interpret ABG", pos_hint={"center_x": 0.5}, on_release=self.on_interpret)
        self.plot_button = MDRaisedButton(text="Plot ABG Results", pos_hint={"center_x": 0.5}, on_release=self.on_plot)
        self.save_button = MDRaisedButton(text="Save Result", pos_hint={"center_x": 0.5}, on_release=self.save_result)
        self.load_button = MDRaisedButton(text="Load Results", pos_hint={"center_x": 0.5}, on_release=self.load_results)

        self.box.add_widget(self.interpret_button)
        self.box.add_widget(self.plot_button)
        self.box.add_widget(self.save_button)
        self.box.add_widget(self.load_button)

        self.result_label = MDLabel(text="Results will be displayed here.", halign="center", theme_text_color="Secondary")
        self.box.add_widget(self.result_label)

        return self.box

    def toggle_theme(self, instance, value):
        self.theme_cls.theme_style = "Dark" if value else "Light"

    def on_interpret(self, instance):
        try:
            pH = float(self.fields["pH"].text)
            pCO2 = float(self.fields["pCO2 (mmHg)"].text)
            HCO3 = float(self.fields["HCO3 (mEq/L)"].text)
            PaO2 = float(self.fields["PaO2 (mmHg)"].text)
            na = float(self.fields["Na (optional)"].text) if self.fields["Na (optional)"].text else None
            cl = float(self.fields["Cl (optional)"].text) if self.fields["Cl (optional)"].text else None

            blood_gas_type = determine_abg_vbg(PaO2, pCO2)
            anion_gap = calculate_anion_gap(na, cl, HCO3)
            disorder_suggestion = interpret_abg(pH, pCO2, HCO3)
            
            interpretation = f"{blood_gas_type}\n\npH: {pH}\npCO2: {pCO2}\nHCO3: {HCO3}\nPaO2: {PaO2}\nAnion Gap: {anion_gap if anion_gap is not None else 'N/A'}\n\nSuggestion: {disorder_suggestion}"
            self.result_label.text = interpretation
            
            self.show_dialog(interpretation)
        except ValueError:
            self.result_label.text = "Please enter valid numerical values!"

    def show_dialog(self, interpretation):
        self.dialog = MDDialog(title="ABG Interpretation", text=interpretation, size_hint=(0.8, 0.4))
        self.dialog.open()

if __name__ == "__main__":
    ABGApp().run()

# Buildozer configuration
requirements = python3,kivy,kivymd
package.domain = org.example
package.name = ABGAnalyzer
package.version = 1.0
android.api = 31
android.ndk = 23b
