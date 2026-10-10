from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from urllib.parse import quote
import webbrowser
from kivy.utils import platform

def open_url(url):
    if platform == "android":
        from jnius import autoclass
        Intent = autoclass("android.content.Intent")
        Uri = autoclass("android.net.Uri")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
        PythonActivity.mActivity.startActivity(intent)
    else:
        webbrowser.open(url)

APP_NAME = "BELKURI CRUNCH"
WHATSAPP_NUMBER = "917477888445"

ORANGE = get_color_from_hex("#F57C00")
GREEN = get_color_from_hex("#198754")
RED = get_color_from_hex("#E53935")
DARK = get_color_from_hex("#202020")
WHITE = get_color_from_hex("#FFFFFF")
LIGHT = get_color_from_hex("#F6F6F6")
GREY = get_color_from_hex("#777777")

Window.clearcolor = LIGHT

PRODUCTS =[
    {"id": 1, "name": "Classic Potato Chips","price": 5, "image": "products/classic.png"},
    {"id": 2, "name": "Masala Chips","price": 5, "image": "products/masala.png"},
    {"id": 3, "name": "Chili Spicy Chips","price": 10, "image": "products/chili.png"},
    {"id": 4, "name": "Special Crunch","price": 20, "image": "products/special.png"},
]

cart = {}

def add_to_cart(product):
    pid = product["id"]
    if pid in cart:
        cart[pid]["quantity"] += 1
    else:
        cart[pid] = {"product": product, "quantity": 1}

def increase_quantity(pid):
    if pid in cart:
        cart[pid]["quantity"] += 1

def decrease_quantity(pid):
    if pid in cart:
        cart[pid]["quantity"] -= 1
        if cart[pid]["quantity"] <= 0:
            del cart[pid]

def remove_from_cart(pid):
    cart.pop(pid, None)

def cart_total():
    return sum(item["product"]["price"] * item["quantity"] for item in cart.values())

def create_button(text, background=ORANGE, height=dp(50), font_size=dp(15)):
    return Button(text=text, size_hint_y=None, height=height, font_size=font_size,
                  bold=True, color=WHITE, background_normal="", background_color=background)

class BottomNavigation(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(65)
        self.padding = dp(5)
        self.spacing = dp(5)
        for text, screen_name in [
            ("🏠\nHome", "home"),
            ("🥔\nProducts", "products"),
            ("🛒\nCart", "cart"),
            ("📦\nOrder", "order"),
        ]:
            btn = Button(text=text, font_size=dp(12), bold=True, color=DARK,
                         background_normal="", background_color=WHITE)
            btn.bind(on_release=lambda instance, name=screen_name: self.go_to(name))
            self.add_widget(btn)

    def go_to(self, screen_name):
        App.get_running_app().root.current = screen_name

class Header(BoxLayout):
    def __init__(self, title=APP_NAME, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(65)
        self.padding = [dp(15), dp(5)]
        self.add_widget(Label(text=title, font_size=dp(20), bold=True, color=DARK))

class HomeScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", spacing=dp(8))

        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(70), padding=dp(10))
        header.add_widget(Label(text="🥔", font_size=dp(40), size_hint_x=None, width=dp(60)))
        header.add_widget(Label(text="BELKURI CRUNCH", font_size=dp(23), bold=True, color=ORANGE))
        root.add_widget(header)

        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", spacing=dp(15), padding=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(Label(text="🥔 BELKURI CRUNCH", font_size=dp(28), bold=True, color=ORANGE,
                                 size_hint_y=None, height=dp(60)))
        content.add_widget(Label(text="Crunchy Taste • Desi Feel", font_size=dp(19), bold=True, color=DARK,
                                 size_hint_y=None, height=dp(45)))
        content.add_widget(Label(text="Fresh • Crispy • Delicious", font_size=dp(16), color=GREY,
                                 size_hint_y=None, height=dp(40)))

        shop = create_button("🛍️  SHOP NOW", ORANGE, dp(55), dp(17))
        shop.bind(on_release=lambda x: setattr(self.manager, "current", "products"))
        content.add_widget(shop)

        content.add_widget(Label(text="Why BELKURI CRUNCH?", font_size=dp(21), bold=True, color=DARK,
                                 size_hint_y=None, height=dp(45)))
        FEATURES = [
            ("potato.png", "Fresh Potato"),
            ("crunchy.png", "Extra Crunchy"),
            ("spicy.png", "Desi Masala"),
            ("heart.png", "Made With Care"),
        ]
        for icon, feature in FEATURES:
            content.add_widget(Label(text=feature, font_size=dp(17), color=DARK,
                                     size_hint_y=None, height=dp(42)))

        view = create_button("🥔  VIEW PRODUCTS", GREEN, dp(55))
        view.bind(on_release=lambda x: setattr(self.manager, "current", "products"))
        content.add_widget(view)

        scroll.add_widget(content)
        root.add_widget(scroll)
        root.add_widget(BottomNavigation())
        self.add_widget(root)

class ProductsScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", spacing=dp(5))
        root.add_widget(Header("🥔 Our Products"))

        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=dp(12), padding=dp(12), size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))

        for product in PRODUCTS:
            card = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(120),
                             spacing=dp(10), padding=dp(10))
            card.add_widget(Label(text=product["emoji"], font_size=dp(45),
                                  size_hint_x=None, width=dp(70)))

            info = BoxLayout(orientation="vertical", spacing=dp(3))
            info.add_widget(Label(text=product["name"], font_size=dp(17), bold=True, color=DARK))
            info.add_widget(Label(text=product["bengali"], font_size=dp(13), color=GREY))
            info.add_widget(Label(text=f"₹{product['price']}", font_size=dp(17), bold=True, color=GREEN))
            card.add_widget(info)

            btn = create_button("+ ADD", ORANGE, dp(48), dp(13))
            btn.size_hint_x = None
            btn.width = dp(80)
            btn.bind(on_release=lambda x, p=product: self.add_product(p))
            card.add_widget(btn)
            layout.add_widget(card)

        scroll.add_widget(layout)
        root.add_widget(scroll)
        root.add_widget(BottomNavigation())
        self.add_widget(root)

    def add_product(self, product):
        add_to_cart(product)
        Popup(title="Added to Cart",
              content=Label(text=f"{product['name']} added to cart!"),
              size_hint=(0.8, 0.3)).open()

class CartScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", spacing=dp(5))
        root.add_widget(Header("🛒 Your Cart"))

        if not cart:
            box = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(15))
            box.add_widget(Label(text="🛒\n\nYour cart is empty", font_size=dp(22), color=GREY))
            btn = create_button("🥔 SHOP NOW", ORANGE, dp(55))
            btn.bind(on_release=lambda x: setattr(self.manager, "current", "products"))
            box.add_widget(btn)
            root.add_widget(box)
        else:
            scroll = ScrollView()
            layout = GridLayout(cols=1, spacing=dp(10), padding=dp(10), size_hint_y=None)
            layout.bind(minimum_height=layout.setter("height"))

            for pid, item in cart.items():
                product = item["product"]
                quantity = item["quantity"]

                card = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(125),
                                 padding=dp(10), spacing=dp(5))
                top = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(45))
                top.add_widget(Label(text=product["name"], font_size=dp(16), bold=True, color=DARK))
                top.add_widget(Label(text=f"₹{product['price']} each", font_size=dp(14), color=GREEN))
                card.add_widget(top)

                bottom = BoxLayout(orientation="horizontal", spacing=dp(5))
                minus = Button(text="−", font_size=dp(20), bold=True, color=WHITE,
                               background_normal="", background_color=RED)
                minus.bind(on_release=lambda x, p=pid: self.change_quantity(p, -1))
                qty = Label(text=str(quantity), font_size=dp(18), bold=True, color=DARK)
                plus = Button(text="+", font_size=dp(20), bold=True, color=WHITE,
                              background_normal="", background_color=GREEN)
                plus.bind(on_release=lambda x, p=pid: self.change_quantity(p, 1))
                remove = Button(text="🗑 Remove", font_size=dp(13), color=WHITE,
                                background_normal="", background_color=GREY)
                remove.bind(on_release=lambda x, p=pid: self.remove_product(p))

                bottom.add_widget(minus)
                bottom.add_widget(qty)
                bottom.add_widget(plus)
                bottom.add_widget(remove)
                card.add_widget(bottom)
                layout.add_widget(card)

            scroll.add_widget(layout)
            root.add_widget(scroll)

            root.add_widget(Label(text=f"TOTAL: ₹{cart_total()}", font_size=dp(21), bold=True,
                                  color=DARK, size_hint_y=None, height=dp(60)))

            order = create_button("📦  PLACE ORDER", GREEN, dp(55), dp(17))
            order.bind(on_release=lambda x: setattr(self.manager, "current", "order"))
            root.add_widget(order)

        root.add_widget(BottomNavigation())
        self.add_widget(root)

    def change_quantity(self, pid, amount):
        if amount > 0:
            increase_quantity(pid)
        else:
            decrease_quantity(pid)
        self.on_pre_enter()

    def remove_product(self, pid):
        remove_from_cart(pid)
        self.on_pre_enter()

class OrderScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", spacing=dp(5))
        root.add_widget(Header("📦 Place Your Order"))

        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", spacing=dp(12), padding=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(Label(text="Customer Name", font_size=dp(15), bold=True, color=DARK,
                                 size_hint_y=None, height=dp(30)))
        name_input = TextInput(hint_text="Enter your name", multiline=False,
                               size_hint_y=None, height=dp(50))
        content.add_widget(name_input)

        content.add_widget(Label(text="Phone Number", font_size=dp(15), bold=True, color=DARK,
                                 size_hint_y=None, height=dp(30)))
        phone_input = TextInput(hint_text="Enter phone number", multiline=False, input_type="number",
                                size_hint_y=None, height=dp(50))
        content.add_widget(phone_input)

        content.add_widget(Label(text="Delivery Address", font_size=dp(15), bold=True, color=DARK,
                                 size_hint_y=None, height=dp(30)))
        address_input = TextInput(hint_text="Enter full delivery address", multiline=True,
                                  size_hint_y=None, height=dp(100))
        content.add_widget(address_input)

        content.add_widget(Label(text="ORDER SUMMARY", font_size=dp(19), bold=True, color=ORANGE,
                                 size_hint_y=None, height=dp(45)))

        summary = ""
        for item in cart.values():
            product = item["product"]
            quantity = item["quantity"]
            summary += f"{product['name']} × {quantity} = ₹{product['price'] * quantity}\n"

        if not summary:
            summary = "Cart is empty."

        content.add_widget(Label(text=summary, font_size=dp(15), color=DARK,
                                 size_hint_y=None, height=dp(100)))
        content.add_widget(Label(text=f"TOTAL: ₹{cart_total()}", font_size=dp(22), bold=True,
                                 color=GREEN, size_hint_y=None, height=dp(50)))

        wa = create_button("📲 ORDER ON WHATSAPP", GREEN, dp(60), dp(17))
        wa.bind(on_release=lambda x: self.send_whatsapp(name_input.text, phone_input.text, address_input.text))
        content.add_widget(wa)

        scroll.add_widget(content)
        root.add_widget(scroll)
        root.add_widget(BottomNavigation())
        self.add_widget(root)

    def send_whatsapp(self, name, phone, address):
        if not cart:
            Popup(title="Cart Empty",
                  content=Label(text="Please add products to your cart first."),
                  size_hint=(0.85, 0.3)).open()
            return

        if not name.strip() or not phone.strip() or not address.strip():
            Popup(title="Missing Information",
                  content=Label(text="Please enter name, phone and delivery address."),
                  size_hint=(0.85, 0.3)).open()
            return

        message = "🥔 BELKURI CRUNCH ORDER\n========================\n\n"
        message += f"👤 Name: {name}\n📞 Phone: {phone}\n📍 Address: {address}\n\n"
        message += "🛒 ORDER DETAILS\n------------------------\n"

        for item in cart.values():
            product = item["product"]
            quantity = item["quantity"]
            message += f"{product['name']} × {quantity} = ₹{product['price'] * quantity}\n"

        message += f"\n💰 TOTAL: ₹{cart_total()}\n\nThank you for ordering from BELKURI CRUNCH! ❤️"

        url = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"
        try:
            open_url(url)
        except Exception as exc:
            Popup(title="WhatsApp Error",
                  content=Label(text=f"Could not open WhatsApp.\n{exc}"),
                  size_hint=(0.9, 0.4)).open()

class BelkuriCrunchApp(App):
    def build(self):
        self.title = APP_NAME
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ProductsScreen(name="products"))
        sm.add_widget(CartScreen(name="cart"))
        sm.add_widget(OrderScreen(name="order"))
        return sm

if __name__ == "__main__":
    BelkuriCrunchApp().run()
