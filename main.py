from asyncore import loop
from ursina import *
from ursina import Audio
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random

noise = PerlinNoise(octaves=3,seed=random.randint(1,1000))

app = Ursina()
audio = Audio()

grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
sand_texture = load_texture('assets/sand_block.png')

placing_sound = Audio('assets/block_place.wav')
breaking_sound = Audio('assets/bone_break.wav')


block_pick = grass_texture

window.fps_counter.enabled = False
window.exit_button.visible = False
window.fullscreen = True

initial_player_position = (10, 1, 10)  # Adjust the position as needed

player = FirstPersonController(position=initial_player_position)

def update_block_pick():
    global block_pick
    if held_keys['1']:
        block_pick = grass_texture
    if held_keys['2']:
        block_pick = stone_texture
    if held_keys['3']:
        block_pick = brick_texture
    if held_keys['4']:
        block_pick = dirt_texture
    if held_keys['5']:
        block_pick = sand_texture
    
def update():
    if player.y < -35:
        player.position = (0, 1, 0)  # Teleport the player back to the center

    if held_keys['right mouse'] or held_keys['left mouse']:
        hand.active()
    else:
        hand.passive()

    update_block_pick()

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block.obj',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                placing_sound.play()
                if block_pick == grass_texture:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=grass_texture)
                if block_pick == stone_texture:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=stone_texture)
                if block_pick == brick_texture:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=brick_texture)
                if block_pick == dirt_texture:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=dirt_texture)
                if block_pick == sand_texture:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=sand_texture)

            if key == 'left mouse down':
                    destroy(self)
                    breaking_sound.play()


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True,
        )


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm.obj',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)



for z in range(-10, 10):
    for x in range(-10, 10):
        y = noise([x * 0.02, z * 0.02])
        y = math.floor(y * 7.5)

        voxel = Voxel(position=(x, y, z))

# Define a function to close the window
def close_window():
    window.close()

# Bind the function to a key press (e.g., press 'Esc' to close the window)
def input(key):
    if key == 'escape':
        close_window()


player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
