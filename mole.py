import arcade

SPRITE_WIDTH = 454
SPRITE_HEIGHT = 454


class Mole(arcade.Sprite):
    def __init__(self, x, y, scale, game):
        super().__init__()
        self.textures = []
        for row in range(4):
            for column in range(6):
                texture = arcade.load_texture("img/mole_sprite_sheet.png", column * SPRITE_WIDTH, row * SPRITE_HEIGHT,
                                              SPRITE_WIDTH, SPRITE_HEIGHT)
                self.textures.append(texture)
        self.game = game
        self.scale = scale
        self.set_texture(0)
        self.center_x = x
        self.center_y = y
        self.frame = 0
        self.animation_time = 0
        self.animate = False
        self.update_scale()
        self.speed = 4
        self.clicked = False
        self.score_to_increase = 5
        self.hit_box_width = SPRITE_WIDTH * self.scale
        self.hit_box_height = SPRITE_HEIGHT * self.scale
        self.set_hit_box([(-self.hit_box_width / 2, -self.hit_box_height / 2),
                          (-self.hit_box_width / 2, self.hit_box_height / 2),
                          (self.hit_box_width / 2, self.hit_box_height / 2),
                          (self.hit_box_width / 2, -self.hit_box_height / 2)])

    def update_scale(self):
        self.width = SPRITE_WIDTH * self.scale
        self.height = SPRITE_HEIGHT * self.scale

    def update(self, delta_time, total_seconds):
        self.animation_time += delta_time * self.speed
        if self.animate:
            frame = int(self.animation_time * 5) % len(self.textures)
            if frame != self.frame:
                self.frame = frame
                self.set_texture(self.frame)

            if self.frame == 23:
                self.frame = 0
                self.animate = False
        else:
            self.clicked = False

        self.update_scale()

    def get_up(self):
        if not self.animate:
            self.animation_time = 0
        self.animate = True

    def be_clicked(self):
        if not self.clicked and self.animate:  # Agregar "and self.animate"
            self.game.increase_score(self.score_to_increase)
            self.clicked = True

    def increase_speed(self, speed):
        self.speed = speed

    def increase_score_to_increase(self, score):
        self.score_to_increase = score

    def reset(self):
        self.speed = 5
        self.score_to_increase = 5
