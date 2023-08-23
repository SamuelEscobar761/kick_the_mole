import arcade


class Mole(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__()

        self.center_x = w // 2
        self.center_y = h // 2
        self.scale = 0.5

        self.texture = arcade.load_texture("img/mole_sprite_sheet.png")

        self.texture_width = 450
        self.texture_height = 450
        self.columns = 6
        self.rows = 4
        self.frame_count = 24

        self.texture_index = 0
        self.current_frame = 0
        self.animation_time = 0.2  # Time in seconds per frame
        self.current_time = 0

    def update(self, delta_time):
        self.current_time += delta_time

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.texture_index = self.current_frame % (self.columns * self.rows)

            left = (self.texture_width * self.texture_index) % (self.texture_width * self.columns)
            top = self.texture_height * (self.texture_index // self.columns)
            self.set_texture(left, top)
