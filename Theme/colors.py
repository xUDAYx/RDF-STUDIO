class Colors:
    def __init__(self):
        self.background_color = "#090810"
        self.navbar_color = "#232228"
        self.sidebar_color = "#232228"
        self.sidebar_button_color = "#090810"
        self.sidebar_button_selected_color = "#7657ff"
        self.button_colors = [
            "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
            "#B4A7D6", "#D5A6BD", "#A9D18E", "#D5E8D4", "#E1D5E7", "#FFF2CC"
        ]
        self.title_bar_color = "#090810"  # Add this line

    def set_background_color(self, color):
        self.background_color = color

    def set_navbar_color(self, color):
        self.navbar_color = color

    def set_sidebar_color(self, color):
        self.sidebar_color = color

    def set_sidebar_button_color(self, color):
        self.sidebar_button_color = color

    def set_sidebar_button_selected_color(self, color):
        self.sidebar_button_selected_color = color

    def set_button_colors(self, colors):
        self.button_colors = colors

    def set_title_bar_color(self, color):  # Add this method
        self.title_bar_color = color
