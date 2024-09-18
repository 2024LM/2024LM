from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
import webbrowser
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO





class PasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        password_label = MDLabel(text="Entrez le mot de passe:", halign="center")
        self.password_field = MDTextField(hint_text="Mot de passe", password=True)
        enter_button = MDRaisedButton(text="Valider", on_release=self.check_password)

        layout.add_widget(password_label)
        layout.add_widget(self.password_field)
        layout.add_widget(enter_button)

        self.add_widget(layout)

    def check_password(self, instance):
        if self.password_field.text == "arfoud":
            self.manager.current = "welcome_screen"
        else:
            Snackbar(text="Mot de passe incorrect").show()

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        welcome_label = MDLabel(text=u"Bienvenue dans l'application de téléchargement de manga", halign="center", theme_text_color="Secondary")

        contact_us_button = MDRaisedButton(text=u"Contactez-nous", on_release=self.open_facebook_page)
        video_button = MDRaisedButton(text=u"Vidéo", on_release=self.open_video_link)

        start_button = MDRaisedButton(text=u"Démarrer", on_release=self.start_app)

        layout.add_widget(welcome_label)
        layout.add_widget(contact_us_button)
        layout.add_widget(video_button)
        layout.add_widget(start_button)

        self.add_widget(layout)

        # تشغيل تلقائي للفيديو بعد دخول الشاشة وتكراره كل 30 ثانية
        Clock.schedule_interval(self.auto_open_video, 30)

    def start_app(self, instance):
        self.manager.current = "download_screen"

    def open_facebook_page(self, instance):
        
        webbrowser.open("https://web.facebook.com/profile.php?id=100085445749188")

    def open_video_link(self, instance):
        video_link = "https://youtu.be/RwNwlVO21fo"
        webbrowser.open(video_link)

    def auto_open_video(self, dt):
        self.open_video_link(None)  # None يمثل غياب المعامل instance

class DownloadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        label_num_page = MDLabel(text=u'Numéro de page:')
        self.entry_num_page = MDTextField(hint_text=u"Numéro de page", input_type="number")

        label_num_iterations = MDLabel(text=u'Nombre d\'itérations:')
        self.entry_num_iterations = MDTextField(hint_text=u"Nombre d'itérations", input_type="number")

        label_DOSI = MDLabel(text=u'Chemin du dossier:')
        self.entry_DOSI = MDTextField(hint_text=u"Chemin du dossier", helper_text=u"Exemple: /storage/emulated/0/Download", helper_text_mode="on_focus")

        self.btn_start = MDRaisedButton(text=u"Démarrer le téléchargement", on_release=self.start_download)
        self.btn_stop = MDRaisedButton(text=u"Terminer le processus", on_release=self.stop_download)
        self.download_status = MDLabel(text='', halign="center")

        layout.add_widget(label_num_page)
        layout.add_widget(self.entry_num_page)
        layout.add_widget(label_num_iterations)
        layout.add_widget(self.entry_num_iterations)
        layout.add_widget(label_DOSI)
        layout.add_widget(self.entry_DOSI)
        layout.add_widget(self.btn_start)
        layout.add_widget(self.btn_stop)
        layout.add_widget(self.download_status)

        self.add_widget(layout)

        self.base_save_path = ""  # تعيين المسار الأساسي للحفظ هنا

    def start_download(self, instance):
        try:
            f = int(self.entry_num_page.text)  # استخدم self.entry_num_page بدلاً من self.num_page
            H = 1
            num_iterations = int(self.entry_num_iterations.text)  # استخدم self.entry_num_iterations بدلاً من self.label_num_iterations
            increment_value = 1
            Y = self.entry_DOSI.text  # استخدم self.entry_DOSI بدلاً من self.dir_path
            images_per_group = 5

            self.base_save_path = os.path.join(Y, "Download")  # مسار الحفظ الأساسي

            for iteration in range(num_iterations):
                G = 'https://ww.mangalek.org/comics/return-of-the-broken-constellation/'
                url = G + str(f) + '/'

                response = requests.get(url)
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                img_tags = soup.find_all('img')

                save_path = os.path.join(self.base_save_path, f'page_{f}/')
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                for j, img in enumerate(img_tags):
                    img_url = img.get('src')
                    img_url = urljoin(url, img_url)
                    img_data = requests.get(img_url).content
                    img = Image.open(BytesIO(img_data))
                    img = img.convert("RGB")
                    img_name = f'image_{f}.{H}_{j + 1}.jpg'
                    img_path = os.path.join(save_path, img_name)
                    img.save(img_path)
                    print(f'Saved: {img_path}')

                f += increment_value
                H += 1

            snackbar = Snackbar(text="تم حفظ الصور بنجاح!")
            snackbar.show()
        except Exception as e:
            dialog = MDDialog(title="خطأ", text=str(e), buttons=[MDRaisedButton(text="حسنا")])
            dialog.open()

    def stop_download(self, instance):
        self.download_status.text = u'Processus terminé'

class MangaDownloaderApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        screen_manager = ScreenManager()
        password_screen = PasswordScreen(name="password_screen")
        welcome_screen = WelcomeScreen(name="welcome_screen")
        download_screen = DownloadScreen(name="download_screen")

        screen_manager.add_widget(password_screen)
        screen_manager.add_widget(welcome_screen)
        screen_manager.add_widget(download_screen)

        return screen_manager

if __name__ == '__main__':
    MangaDownloaderApp().run()
