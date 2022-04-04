class SimpleEnvironment:
    def __init__(self, xmin=0, xmax=0, ymin=0, ymax=0, field_of_view=0, coef_deplacement=0):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self.field_of_view = field_of_view
        self.coef_deplacement = coef_deplacement
        super().__init__()

    def get_xmin(self):
        return self.xmin

    def get_xmax(self):
        return self.xmax

    def get_ymin(self):
        return self.ymin

    def get_ymax(self):
        return self.ymax

    def get_field_of_view(self):
        return self.field_of_view

    def get_coef_deplacement(self):
        return self.coef_deplacement
