from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import subprocess
import re

class RadarApp(App):
    def build(self):
        self.title = "Radar Wi-Fi Móvil"
        
        # Diseño principal
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Título superior
        self.titulo = Label(
            text="[b]Radar Wi-Fi Familiar[/b]",
            markup=True,
            font_size='22sp',
            size_hint_y=None,
            height=50,
            color=(0.22, 0.74, 0.96, 1)
        )
        layout.add_widget(self.titulo)
        
        # Botón de escaneo manual
        btn_escanear = Button(
            text="Escanear Red Ahora",
            size_hint_y=None,
            height=55,
            background_color=(0.16, 0.65, 0.36, 1)
        )
        btn_escanear.bind(on_press=self.ejecutar_escaneo)
        layout.add_widget(btn_escanear)
        
        # Contenedor con desplazamiento para la lista de dispositivos
        self.scroll = ScrollView(size_hint=(1, 1))
        self.lista_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.lista_layout.bind(minimum_height=self.lista_layout.setter('height'))
        
        self.scroll.add_widget(self.lista_layout)
        layout.add_widget(self.scroll)
        
        # Estado inferior
        self.status_label = Label(
            text="Presiona el botón para buscar dispositivos...",
            size_hint_y=None,
            height=30,
            font_size='12sp',
            color=(0.6, 0.65, 0.7, 1)
        )
        layout.add_widget(self.status_label)
        
        # Escanear automáticamente al iniciar
        Clock.schedule_once(self.ejecutar_escaneo, 1)
        
        return layout

    def ejecutar_escaneo(self, instance):
        self.status_label.text = "Escaneando red local..."
        self.lista_layout.clear_widgets()
        
        dispositivos = []
        try:
            # Lee la tabla ARP del sistema Android
            resultado = subprocess.check_output(["ip", "neigh"], universal_newlines=True)
            for linea in resultado.splitlines():
                partes = linea.split()
                if len(partes) >= 5:
                    ip = partes[0]
                    mac = partes[4]
                    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                        dispositivos.append({"ip": ip, "mac": mac})
        except Exception as e:
            # Plan B: intentar con arp -a si ip neigh no está disponible en alguna versión
            try:
                resultado = subprocess.check_output(["arp", "-a"], universal_newlines=True)
                for linea in resultado.splitlines():
                    match_ip = re.search(r'\(?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]?', linea)
                    match_mac = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', linea)
                    if match_ip:
                        dispositivos.append({"ip": match_ip.group(1), "mac": match_mac.group(0) if match_mac else "Desconocida"})
            except Exception as err:
                print(f"Error general de escaneo: {err}")

        if not dispositivos:
            lbl = Label(text="No se encontraron dispositivos activos.", size_hint_y=None, height=40, color=(0.8, 0.3, 0.3, 1))
            self.lista_layout.add_widget(lbl)
            self.status_label.text = "Escaneo finalizado: 0 dispositivos."
        else:
            for dev in dispositivos:
                card_text = f"IP: {dev['ip']}\nMAC: {dev['mac']}"
                lbl = Label(
                    text=card_text,
                    size_hint_y=None,
                    height=65,
                    halign='left',
                    valign='middle',
                    color=(0.9, 0.9, 0.9, 1)
                )
                lbl.bind(size=lbl.setter('text_size'))
                self.lista_layout.add_widget(lbl)
            self.status_label.text = f"Escaneo completado: {len(dispositivos)} dispositivos encontrados."

if __name__ == '__main__':
    RadarApp().run()