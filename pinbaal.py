from pygame import init, font, display, image, transform, time, event, FINGERDOWN, FINGERMOTION, FINGERUP, gfxdraw, mixer, RESIZABLE
from pymunk import Body, Circle, Poly, Space, pygame_util, constraints, PinJoint
from math import degrees, sin, cos, atan2
from random import randint
import pygame
import random


init()
screen = display.set_mode((800, 600))
collection = pygame.Surface((300,200))
collection.fill((0,0,0))
options = pygame_util.DrawOptions(screen)
space = Space()
space.gravity = 0, 600
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
font1 = font.Font(None, 50)
font2 = font.Font(None, 40)
font3 = font.Font(None, 30)

clock = time.Clock()
lightx, lighty = 540, 1090
total_energy = 0

font = pygame.font.Font(None, 100)  # None uses the default font, 36 is the font size
def add_energy(e):
    global total_energy 
    total_energy += e
    title = font1.render("TITLE", True, (255,255,255))
    score_title = font3.render("COLLISION ENERGY", True, (255,255,255))
    score = font1.render(str(total_energy), True, (255, 255, 255))  # White text color
    screen.blit(score, (600, 250))  # Position (100, 100) on the screen    
    screen.blit(score_title,(500, 200))
    screen.blit(title, (500,80))

def take_image_ca(name):
    return image.load(name).convert_alpha()


def take_image_c(name):
    return image.load(name).convert()


bg = pygame.Surface((800, 600))
bg.fill((0, 0, 0))

def pixelize(surface, pixel_size):
    # Get the original size of the surface
    width, height = surface.get_size()

    # Scale down the surface to a smaller size using pixel_size
    small_surface = pygame.transform.scale(surface, (width // pixel_size, height // pixel_size))

    # Scale it back up to the original size
    pixelized_surface = pygame.transform.scale(small_surface, (width, height))

    return pixelized_surface

def inputs(n):
    inputs =[]
    for i in range(n):
        inputs.append((random.uniform(-6,6), random.uniform(-6,6)))
    return inputs

def col(ds, tags, position, background):
    """Show balls moving based on speeds in ds starting at positions."""
    ball_surfaces = []
    positions = []
    for i in tags:
        # Create surfaces for each ball with a different color
        ball_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        color = (i * 50 % 255, 255 - i * 50 % 255, (i * 100) % 255)  # Varying colors
        pygame.draw.circle(ball_surface, color, (20, 20), 4)
        ball_surfaces.append(ball_surface)
        positions.append(position)

    x, y = position

    def slow(v, drag):
        if v > 0:
            return max(0, v - drag)
        elif v < 0:
            return min(0, v + drag)
        return 0

    

    def update_and_draw(screen):
        nonlocal positions, ds
        for i, (x,y) in enumerate(positions):
            (vx,vy) = ds[i]
            if (vx,vy) != (0,0):
                positions[i] = (x - vx, y - vy)
                ds[i] = (slow(vx, 0.3), slow(vy, 0.3))
                background.blit(ball_surfaces[i],(x-20,y-20))
        screen.blit(pixelize(background, 3), (0, 0))  # Blit the entire background to the screen

    return update_and_draw



base_bat_img = take_image_ca("img\\basebat_blue.png")
left_base_bat_img = transform.flip(
    transform.rotate(base_bat_img, 90), True, False)
right_base_bat_img = transform.rotate(base_bat_img, 90)

base_ball_img = take_image_ca("img\\base_ball.png")

ball_c_t = 1
post_c_t = 2
other_c_t = 3


class Base_bat:
    def __init__(self, x, y, a, vect):
        self.body = Body(1, 1, Body.KINEMATIC)
        self.body.position = x, y
        self.body.angle = a
        shape = Poly(self.body, vect)
        shape.elasticity = 0.5
        shape.friction = 0.5
        shape.collision_type = other_c_t
        space.add(self.body, shape)
        self.body.angular_velocity= 15*3.14/180

    def animation_left(self, img, limit_u, limit_d):
        if left:
            self.body.angular_velocity = -15

        if self.body.angle <= limit_u:
            if left:
                self.body.angular_velocity = 0
            else:
                self.body.angular_velocity = 5
        if self.body.angle >= limit_d:
            self.body.angular_velocity = 0

        if self.body.angle <= limit_u - 0.2:
            self.body.angle = limit_u
        if self.body.angle >= limit_d + 0.2:
            self.body.angle = limit_d
        n = transform.rotate(img, -degrees(self.body.angle))
        screen.blit(n, (self.body.position[0] - n.get_width() //
                    2, self.body.position[1] - n.get_height() // 2))

    
    def animation_right(self, img, limit_u,limit_d):
        if right:
            self.body.angular_velocity = 15

        if self.body.angle >= limit_u:
            if right:
                self.body.angular_velocity = 0
            else:
                self.body.angular_velocity = -5
        if self.body.angle <= limit_d:
            self.body.angular_velocity = 0

        if self.body.angle >= limit_u + 0.2:
            self.body.angle = limit_u
        if self.body.angle <= limit_d - 0.2:
            self.body.angle = limit_d

        n = transform.rotate(img, -degrees(self.body.angle))
        screen.blit(n, (self.body.position[0] - n.get_width() //
                    2, self.body.position[1] - n.get_height() // 2))



class Base_ball:
    def __init__(self, x, y):
        self.body = Body(1, 200)
        self.body.position = x, y
        self.shape = Circle(self.body, 8)
        self.shape.elasticity = 0.75
        self.shape.friction = 0.5
        self.shape.collision_type = ball_c_t
        space.add(self.body, self.shape)

    def animation(self):
        n = transform.rotate(base_ball_img, -degrees(self.body.angle))
        screen.blit(n, (self.body.position[0] - n.get_width() //
                    2, self.body.position[1] - n.get_height() // 2))
        # if self.body.velocity.length > 1000:
        #     self.body.velocity *= 0.99
        # pangle = atan2(self.body.velocity[0] - 0, self.body.velocity[1] - 0) - 3.14159
        # if self.body.velocity.length > 400:
        #     gfxdraw.rectangle(screen, (self.body.position[0] + randint(50, 100) * sin(pangle),
        #                                self.body.position[1] + randint(50, 100) * cos(pangle), 10, 10), (0, randint(0, 255), randint(0, 255)))
        #     gfxdraw.box(screen, (self.body.position[0] + randint(25, 100) * sin(pangle),
        #                          self.body.position[1] + randint(25, 100) * cos(pangle), 10, 10), (0, randint(0, 255), randint(0, 255)))
            
class Post:
    def __init__(self, x, y):
        self.body = Body(body_type=Body.STATIC)
        self.body.position = x, y
        self.shape = Circle(self.body, 7)
        self.shape.elasticity = 0.75
        self.shape.friction = 0.5
        self.shape.color = (255, 105, 205, 50)
        self.shape.collision_type = post_c_t
        space.add(self.body, self.shape)

class Bumper:
    def __init__(self, x, y, vert, e, c_t):
        self.body = Body(body_type=Body.STATIC)
        self.body.position = x, y
        self.shape = Poly(self.body, vert)
        self.shape.elasticity = e
        self.shape.friction = 0.1
        self.shape.collision_type = c_t
        self.shape.color = (255, 165, 0, 100)
        space.add(self.body, self.shape)

def Poly_object(x, y, vect, e, c_t):
    body = Body(1, 1, Body.KINEMATIC)
    body.position = x, y
    shape = Poly(body, vect)
    shape.elasticity = e
    shape.friction = 0.5
    shape.collision_type = c_t
    space.add(body, shape)


def Rectangle_object(x, y, a, size):
    body = Body(1, 1, Body.KINEMATIC)
    body.position = x, y
    body.angle = a
    shape = Poly.create_box(body, size)
    shape.elasticity = 0.75
    shape.friction = 0.5
    shape.collision_type = other_c_t
    space.add(body, shape)


def Circle_object(x, y, radius, e, c_t):
    body = Body(1, 1, Body.KINEMATIC)
    body.position = x, y
    shape = Circle(body, radius)
    shape.elasticity = e
    shape.friction = 0.5
    shape.collision_type = post_c_t
    space.add(body, shape)

def collision_begin(arbiter, space, data):
    shape1, shape2 = arbiter.shapes
    total_ke = arbiter.total_ke
    v1 = shape1.body.velocity
    v2 = shape2.body.velocity
    vx = str(shape1.body.velocity[0])
    vy = str(shape1.body.velocity[1])
    collision_info = vx + ", " + vy
    # f = open("pinball_collision.txt", "w")
    # f.write(collision_info)
    # f.close()
    # with open("pinball_collision.txt", 'r') as file:
    #     while (1):
    #         updated_content = file.read()
    #         if collision_info != updated_content:
    #                 #parse updated_content into variables
    #                 #begin_col()
    #                 break
    tags = [0, 1, 2, 3]
    balls.append(col(inputs(4), tags, shape2.body.position, background))
    space.remove(shape2)
    return True




#Initializing Game Variables
a =2
    #gameframe
gameframe_top = 50
gameframe_bottom = 550
gameframe_left = 50
gameframe_right = 350
left_base_bat = Base_bat(140, 500, 46, ((26*a, 6*a), (26*a, -6*a), (-26*a, 4*a), (-26*a, -4*a), (26*a, 0*a)))
right_base_bat = Base_bat(260, 500, -46, ((26*a, 4*a), (26*a, -4*a), (-25*a, 6*a), (-25*a, -6*a), (-26*a, 0*a)))

base_ball = Base_ball(200, 180)

num_post = 15


vert = [(-15, 0), (15, 0), (0, -20)]
booster = Bumper(200, 150, vert, 2.5, other_c_t)
vert = [(0, -40), (0, 40), (20, 0)]
booster_left = Bumper(51, 250, vert, 2.5, other_c_t)
vert = [(0, -40), (0, 40), (-20, 0)]
booster_right = Bumper(349, 250, vert, 2.5, other_c_t)


for post in range(15):
    post = Post(randint(gameframe_left+20, gameframe_right-20), randint(gameframe_top+20, gameframe_bottom-150))





Rectangle_object(25,300,0,(50,600))#left wall
Rectangle_object(575,300,0,(450,600))#midle wall
Rectangle_object(200,25,0,(299,50))
Rectangle_object(200,25,0,(299,50))
Rectangle_object(90,580,0,(100,180))
Rectangle_object(310,580,0,(100,180))
Rectangle_object(40,457,-45*(3.14/180),(100,200))
Rectangle_object(360,457,45*(3.14/180),(100,200))
Rectangle_object(50,50,45*(3.14/180),(50,50))
Rectangle_object(350,50,-45*(3.14/180),(50,50))






#Rectangle_object((800-350)/2,300,0,(800-350,600))
#Rectangle_object(500,25,0,(50,50))




res = 0
running = True
right = False
left = False
gui = pygame.image.load("img\\gui.png")
gui1 = pygame.image.load("img\\gui1.png")
background = pygame.Surface((800, 600))
background.fill((0, 0, 0))  # Fill with black
balls = []  # To store all `update_and_draw` functions
balls.append(col(inputs(0), [], (0,0), background))

while running:
    screen.fill((0,0,0))
    balltopost_handler = space.add_collision_handler(1, 2)
    balltopost_handler.begin = collision_begin
    


    #screen.blit(bg, (0, 0))

    
    left_base_bat.animation_left(left_base_bat_img, -0.80285, 0.80285)
    right_base_bat.animation_right(right_base_bat_img, 0.80285, -0.80285)
    
    
    
    for ev in event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                left_base_bat.body.angular_velocity = -15
                left = True
            if ev.key == pygame.K_RIGHT:
                #right_base_bat.body.angular_velocity = 15
                #right_base_bat.check_movenment_right()
                right_base_bat.body.angular_velocity = 15
                right = True
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                left = False
            if ev.key == pygame.K_RIGHT:
                #right_base_bat.body.angular_velocity = 5
                    right = False


    if base_ball.body.position[1] > 800:
        res = 1
    if res == 1:
        space.remove(base_ball.body, base_ball.shape)
        base_ball = Base_ball(300, 100)
        res = 0
        total_energy = 0
    
    for update_and_draw in balls:
        update_and_draw(screen)
    '''
    left_base_bat.animation_left(left_base_bat_img, -0.80285, 0.80285)
    right_base_bat.animation_right(right_base_bat_img, 0.80285, -0.80285)
    '''
    
    space.debug_draw(options)
    screen.blit(left_base_bat_img,(100,100))
    screen.blit(gui,(0,0))
    add_energy(1)
    screen.blit(collection, (450,350))
    clock.tick(60)
    space.step(1/60)
    display.update()
    
        

