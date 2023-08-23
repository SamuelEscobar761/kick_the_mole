import arcade
import time

SPRITE_WIDTH = 454
SPRITE_HEIGHT = 454

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

ANIMATION_SPEED = 24
ANIMATION_INTERVAL = 5  # Intervalo de tiempo en segundos para la animación

total_seconds = 0  # Variable para llevar el contador de segundos


class Topo(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.textures = []
        for row in range(4):
            for column in range(6):
                texture = arcade.load_texture("img/mole_sprite_sheet.png", column * SPRITE_WIDTH, row * SPRITE_HEIGHT,
                                              SPRITE_WIDTH, SPRITE_HEIGHT)
                self.textures.append(texture)

        self.set_texture(0)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.frame = 0
        self.animation_time = 0
        self.last_animation_time = 0
        self.animate = False


    def update(self, delta_time, total_seconds):
        self.animation_time += delta_time
        # Verificamos si es hora de animar nuevamente
        if total_seconds % ANIMATION_INTERVAL == 0:
            self.animate = True
            self.last_animation_time = delta_time

        if self.animate:
            # Calculamos el nuevo frame basado en la velocidad de la animación
            frame = int(self.animation_time - self.last_animation_time - delta_time / ANIMATION_SPEED) % len(self.textures)

            # Cambiamos el frame solo si ha pasado suficiente tiempo
            if frame != self.frame:
                self.frame = frame
                self.set_texture(self.frame)

            if self.frame == 23:
                self.frame = 0
                self.animate = False

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Topo Animation")
        self.topo = None

    def setup(self):
        self.topo = Topo()
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("img/fondo.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.topo.draw()

        # Dibujar el contador de segundos
        arcade.draw_text(f"Tiempo: {int(total_seconds)} segundos", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 16)

    def on_update(self, delta_time):
        global total_seconds
        total_seconds += delta_time
        self.topo.update(delta_time, int(total_seconds))


def main():

    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
