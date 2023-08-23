import random
import arcade

from kick_the_mole.mole import Mole

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
total_seconds = 0
time_start = 61


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Topo Animation")
        self.background = None
        self.mole_list = []
        self.animating = False
        self.score = 0
        self.time_to_play = time_start
        self.level = "Tutorial"

    def setup(self):
        self.mole_list = [
            Mole(200, 400, 0.7, self),
            Mole(1500, 400, 0.7, self),
            Mole(400, 900, 0.5, self),
            Mole(1000, 900, 0.5, self),
            Mole(1700, 900, 0.5, self),
            # Agrega más instancias aquí con diferentes posiciones y escalas
        ]
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("img/fondo.png")

    def on_mouse_press(self, x, y, button, modifiers):
        global total_seconds
        if self.time_to_play <= 0:
            # Reiniciar los valores y configurar el juego nuevamente
            self.time_to_play = time_start
            total_seconds = 0
            self.score = 0
            self.level = "Tutorial"
            for mole in self.mole_list:
                mole.reset()  # Implementa el método reset en la clase Mole si es necesario
            self.setup()  # Vuelve a configurar el juego
        else:
            # Lógica de detección de clics durante el juego
            for mole in self.mole_list:
                if mole.collides_with_point((x, y)):
                    mole.be_clicked()

    def on_draw(self):
        arcade.start_render()

        if self.time_to_play <= 0:
            # Dibuja la pantalla azul
            arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                         SCREEN_WIDTH, SCREEN_HEIGHT,
                                         arcade.color.LIGHT_BLUE)

            # Muestra el texto "Final Score: [score registrado]"
            final_score_text = f"Final Score: {self.score} puntos"
            arcade.draw_text(final_score_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.BLACK, font_size=30, anchor_x="center")
        else:
            # Dibuja la pantalla de juego normal
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
            for mole in self.mole_list:
                mole.draw()

            # Dibujar el contador de segundos
            arcade.draw_text(f"Time: {self.time_to_play} seconds", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 16)
            arcade.draw_text(f"Score: {self.score} points", 960, SCREEN_HEIGHT - 30, arcade.color.BLACK, 16)
            arcade.draw_text(f"Level: {self.level}", 1600, SCREEN_HEIGHT - 30, arcade.color.BLACK, 16)

    def on_update(self, delta_time):
        time_to_wait = 5
        if self.time_to_play > 0:
            global total_seconds
            total_seconds += delta_time
            self.time_to_play = int(time_start - total_seconds)

            if self.time_to_play < 11:
                time_to_wait = 2
                self.level = "Not even God"
                for mole in self.mole_list:
                    mole.increase_speed(30)
                    mole.increase_score_to_increase(160)
            elif self.time_to_play < 21:
                time_to_wait = 2
                self.level = "Hard"
                for mole in self.mole_list:
                    mole.increase_speed(25)
                    mole.increase_score_to_increase(80)
            elif self.time_to_play < 31:
                time_to_wait = 2
                for mole in self.mole_list:
                    mole.increase_speed(20)
                    mole.increase_score_to_increase(40)
            elif self.time_to_play < 41:
                time_to_wait = 3
                self.level = "Intermediate"
                for mole in self.mole_list:
                    mole.increase_speed(16)
                    mole.increase_score_to_increase(20)
            elif self.time_to_play < 51:
                time_to_wait = 4
                self.level = "Easy"
                for mole in self.mole_list:
                    mole.increase_speed(8)
                    mole.increase_score_to_increase(10)

            if int(total_seconds) % time_to_wait == 0 and int(total_seconds) != 0 and not self.animating:
                for mole in self._get_up_moles():
                    mole.get_up()
            elif int(total_seconds) % time_to_wait == 1:
                self.animating = False

            for mole in self.mole_list:
                mole.update(delta_time, int(total_seconds))


    def _get_up_moles(self):
        if not self.animating:
            self.animating = True
            num_moles = random.randint(1, len(self.mole_list))
            available_indices = list(range(len(self.mole_list)))
            moles = []
            for i in range(num_moles):
                mole_index = random.choice(available_indices)
                available_indices.remove(mole_index)
                moles.append(self.mole_list[mole_index])
            return moles
        else:
            return []

    def increase_score(self, score):
        self.score += score


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
