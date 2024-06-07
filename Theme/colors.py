class Colors:
    def __init__(self):
        self.background_color = "#090810"
        self.navbar_color = "#232228"
        self.sidebar_color = "#232228"
        self.sidebar_button_color = "#090810"
        self.sidebar_button_selected_color = "#7657ff"
        self.button_colors = [
            "#323234", "#323234", "#323234", "#323234", "#323234",
            "#323234", "#323234", "#323234", "#323234", "#323234", "#323234"
        ]
        self.title_bar_color = "#090810"

        self.navbar_button_style = f"background-color: {self.button_colors[0]}; border: none; border-radius: 10px;"
        self.navbar_button_hover_style = f"background-color: {self.sidebar_button_selected_color};"

    def set_background_color(self, color):
        self.background_color = color

    def set_navbar_color(self, color):
        self.navbar_color = color

    def set_navbar_button_style(self, style):
        self.navbar_button_style = style

    def set_navbar_button_hover_style(self, style):
        self.navbar_button_hover_style = style

    def set_sidebar_color(self, color):
        self.sidebar_color = color

    def set_sidebar_button_color(self, color):
        self.sidebar_button_color = color

    def set_sidebar_button_selected_color(self, color):
        self.sidebar_button_selected_color = color

    def set_button_colors(self, colors):
        self.button_colors = colors

    def set_title_bar_color(self, color):
        self.title_bar_color = color
