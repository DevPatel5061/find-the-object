import pygame, random, time

# Defining Colours
DARK_GRAY = (109, 109, 109)
LIGHT_GRAY = (240, 240, 240)
GRAY = (201, 201, 201)
BLACK = (0, 0, 0)
RED = (246, 38, 38)

# Initializing Pygame
pygame.init()
pygame.mixer.init()

# Setting the screen size
screen_size = (900, 700)
screen = pygame.display.set_mode(screen_size)

# Setting game caption
pygame.display.set_caption("Find The Objects")

# Importing background
level_one_background_image = pygame.image.load("Background/Level_1.png")
level_one_background = level_one_background_image.get_rect()

level_two_background_image = pygame.image.load("Background/Level_2.png")
level_two_background = level_two_background_image.get_rect()

level_three_background_image = pygame.image.load("Background/Level_3.png")
level_three_background = level_three_background_image.get_rect()

# Importing level selectors
level_one_selector = pygame.image.load("Icons/Level_1_Selector.png")
level_one_selector_hover = pygame.image.load("Icons/Level_1_Selector_Hover.png")

level_two_selector = pygame.image.load("Icons/Level_2_Selector.png")
level_two_selector_hover = pygame.image.load("Icons/Level_2_Selector_Hover.png")

level_three_selector = pygame.image.load("Icons/Level_3_Selector.png")
level_three_selector_hover = pygame.image.load("Icons/Level_3_Selector_Hover.png")

# Hit box for levels
level_hit_box = pygame.Rect((260, 170, 380, 378))

# Importing sprite for red circle
red_circle = pygame.image.load("Objects/Red_Circle.png")

# Level 1 Objects and Positions
parking_sign = pygame.image.load("Objects/Level 1/Parking_Sign.png")
roof_panel = pygame.image.load("Objects/Level 1/Roof_Panel.png")
sun_chair = pygame.image.load("Objects/Level 1/Sun_Chair.png")

l1_object_positions = [[725, 347], [1840, 725], [800, 660], [1750, 500], [730, 700], [1535, 185]]

# Level 2 Objects and Positions
keyboard = pygame.image.load("Objects/Level 2/Keyboard.png")
equation = pygame.image.load("Objects/Level 2/Equation.png")
toolbox = pygame.image.load("Objects/Level 2/Toolbox.png")

l2_object_positions = [[460, 430], [300, 125], [1890, 770], [1545, 415], [350, 225], [375, 835], [300, 975], [685, 360], [955, 845]]

# Level 3 Objects and Positions
person = pygame.image.load("Objects/Level 3/Person.png")
rock = pygame.image.load("Objects/Level 3/Rock.png")
stump = pygame.image.load("Objects/Level 3/Stump.png")

l3_object_positions = [[430, 430], [765, 545], [1255, 575], [400, 275], [405, 130], [700, 500], [510, 610], [425, 320], [1210, 355]]

# Level page button
right_button = pygame.image.load("Buttons/Right_Button.png")
right_button_hover = pygame.image.load("Buttons/Right_Button_Hover.png")
left_button = pygame.image.load("Buttons/Left_Button.png")
left_button_hover = pygame.image.load("Buttons/Left_Button_Hover.png")

# Importing title sprite
title = pygame.image.load("Icons/Title.png")

# Importing font
title_font = pygame.font.Font("Font/Ballega.ttf", 70)
play_font = pygame.font.Font("Font/Ballega.ttf", 50)
instruction_font = pygame.font.Font("Font/Ballega.ttf", 25)
level_font = pygame.font.Font("Font/Ballega.ttf", 65)
timer_font = pygame.font.Font("Font/Ballega.ttf", 35)
end_screen_font = pygame.font.Font("Font/Ballega.ttf", 80)
end_screen_information = pygame.font.Font("Font/Ballega.ttf", 45)

# Loading the background musics
menu_song = pygame.mixer.Sound('Sounds/Background Music/Woody_Path.wav')
game_song = pygame.mixer.Sound('Sounds/Background Music/Dark_Knight.wav')

# Setting a channel for each background music
menu_channel = pygame.mixer.Channel(1)
game_channel = pygame.mixer.Channel(2)

# Playing the background music
menu_channel.play(menu_song, loops=-1)
game_channel.play(game_song, loops=-1)

# Setting the volume of the background music
menu_channel.set_volume(0.25)
game_channel.set_volume(0)

# Loading sound effects
start = pygame.mixer.Sound("Sounds/Sound Effects/Start_Click.wav")
click = pygame.mixer.Sound("Sounds/Sound Effects/UI_Click.wav")
success = pygame.mixer.Sound("Sounds/Sound Effects/Success.wav")

# Setting the volume of sound effects
start.set_volume(0.15)
success.set_volume(0.35)

# Settings and defining screen status
in_start_screen = True
in_level = False
in_game = False
in_legend = False
in_end_screen = False

# Keeps track of levels
level = 1
level_displayed = True

# Checks if user won or timer finished
timer_finished = False
level_completed = False

# Animation variables for effect
play_offset = 0
direction = 1

# Camera position and speed
cameraX, cameraY = 0, 0
camera_speed = 7

# Computes if an object was clicked
object_clicked = [False] * 9
objects_found = [0] * 9

# Left click handling
left_click_up = False
left_click_down = False

# Pygame setting for clock
clock = pygame.time.Clock()

# Loop until the user clicks the close button
done = False

# A 2D list containing all the positions of each object of each level (Row represents level)
object_positions = [l1_object_positions[random.randint(0, 1)], l1_object_positions[random.randint(2, 3)], l1_object_positions[random.randint(4, 5)],
                    l2_object_positions[random.randint(0, 2)], l2_object_positions[random.randint(3, 5)], l2_object_positions[random.randint(6, 8)],
                    l3_object_positions[random.randint(0, 2)], l3_object_positions[random.randint(3, 5)], l3_object_positions[random.randint(6, 8)]]

# Organizes objects into a list
objects = [parking_sign, roof_panel, sun_chair, keyboard, equation, toolbox, person, rock, stump]


# Function for the bouncing animation
def bouncing_animation(play_offset, direction):

    # Calculates offset
    play_offset += direction * 0.5

    # Switches direction once the limit is reached
    if play_offset > 5 or play_offset < -5:
        direction *= -1

    return play_offset, direction


# Function for the camera movement
def camera_movement(width, height, cameraX, cameraY):

    keys = pygame.key.get_pressed()

     # Changes camera position when WASD is pressed
    if keys[pygame.K_w]:
        cameraY -= camera_speed
    if keys[pygame.K_s]:
        cameraY += camera_speed
    if keys[pygame.K_a]:
        cameraX -= camera_speed
    if keys[pygame.K_d]:
        cameraX += camera_speed

    # Makes sure camera position is within frame
    if cameraX < 0:
        cameraX = 0
    elif cameraX > width - screen_size[0]:
        cameraX = width - screen_size[0]

    if cameraY < 0:
        cameraY = 0
    elif cameraY > height - screen_size[1]:
        cameraY = height - screen_size[1]

    return cameraX, cameraY


# A function to display the background image and objects for the levels
def objects_spawning(level_chosen, background_image, list_shift):

    if level == level_chosen:
        screen.blit(background_image, (-cameraX, -cameraY))
        for i in range(3):
            screen.blit(objects[i + list_shift], (object_positions[i + list_shift][0] - cameraX, object_positions[i + list_shift][1] - cameraY))


# A function to display the red circle on objects that were found
def objects_clicking(object_clicked, objects_found):
    
    # Checks if an object has been clicked
    # If so, object_clicked[object value] is turned true
    if event.type == pygame.MOUSEBUTTONDOWN:
        for i, object in enumerate(objects):
            if object.get_rect(topleft=(object_positions[i][0] - cameraX, object_positions[i][1] - cameraY)).collidepoint(event.pos):
                success.play()
                object_clicked[i] = True
                objects_found[i] = 1
                break

    # Offsets for the circles as each object requires a different offset
    red_circle_offsets = [(-15, -5), (-3, -5), (6, -5), (-4, -11), (-2, -5), (-8, -11), (-16, -2), (-13, -17), (-7, -12)]

    # If an object has been clicked, offset values are retrieved and the circle is displayed
    for i, clicked in enumerate(object_clicked):
        if clicked:
            x_offset, y_offset = red_circle_offsets[i]
            screen.blit(red_circle, (object_positions[i][0] - cameraX + x_offset, object_positions[i][1] - cameraY + y_offset))

    return object_clicked, objects_found


# A function to make the level selector to hover
def level_selectors(selector, hover):
    
    screen.blit(selector, (0, 0))
    if level_hit_box.collidepoint(pygame.mouse.get_pos()):
        screen.blit(hover, (-5, -5))

# A function to make the level page buttons to hover
def level_button_hover(hover, direction, x, y):
    
    if direction.collidepoint(pygame.mouse.get_pos()):
        screen.blit(hover, (x, y))


# A function to change the page when the buttons are pressed
def level_change_buttons(direction, change, level, left_click):

    # If the cursor hovers over a button and is pressed, level changes 
    if left_button_rect.collidepoint(pygame.mouse.get_pos()) or right_button_rect.collidepoint(pygame.mouse.get_pos()):
        if direction.collidepoint(event.pos) and left_click:
            click.play()
            level += change
            left_click = False

    return level, left_click

def timer(time_limit, in_end_screen, in_game, timer_finished):

    # Computes the elapsed time and remaining time in seconds
    current_time = time.time()
    elapsed = current_time - start_time
    remaining = time_limit * 61.25 - elapsed

    # Changes timer color to red once 30 seconds or less remains
    timer_color = BLACK
    if remaining < 30:
        timer_color = RED
    
    # Changes to end screen once timer hits 0
    if remaining < 0:
        in_game = False
        in_end_screen = True
        timer_finished = True

    # Calculates the time remaining in minutes and seconds
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)

    # Renders the timer using the minutes and seconds
    countdown_display = timer_font.render(f"{minutes:02}:{seconds:02}", True, timer_color)

    # Creates a transparent rectangle for timer 
    timer_surface = pygame.Surface((150, 40), pygame.SRCALPHA)
    pygame.draw.rect(timer_surface, (50, 50, 50, 110), (0, 0, 125, 40))

    # Displays timer
    screen.blit(timer_surface, (15, 13))
    screen.blit(countdown_display, (20, 20))

    return in_end_screen, in_game, timer_finished
    

# A function to create the title screen for each level
def level_title_screen(text, x, y):

    # Creates, renders, and displays a title slide for each level
    title = level_font.render(text, True, GRAY)
    screen.blit(title, (x, y))
    pygame.display.flip()
    pygame.time.delay(1000)


# Main program loop
while not done:

    left_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            left_click_up = True

            # Left click handling for the game
            if left_click_down == True and left_click_up == True:
                left_click = True
                left_click_down = False
                left_click_up = False

            # Changes to level screen
            if in_start_screen:
                left_click = False
                start.play()
                in_start_screen = False
                in_level = True

            # Changes to the game screen
            if in_level and level_hit_box.collidepoint(event.pos) and left_click == True:
                click.play()
                in_level = False
                in_game = True
                start_time = time.time()
                
        # Allows the user to press Q for the legend
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and in_game:
                in_legend = not in_legend

    screen.fill(LIGHT_GRAY)

    # Runs the start screen
    if in_start_screen: 

        # Creates the play and instruction text
        play = play_font.render("Click To Play!", True, GRAY)
        instruction = instruction_font.render("WASD To Move | Left Click For Action | Q For Legend", True, GRAY)
        
        # Runs bouncing animation for the play text
        play_offset, direction = bouncing_animation(play_offset, direction)

        # Displays the starting screen
        screen.blit(title, (10, -100))
        screen.blit(play, (270, 320 + play_offset))
        screen.blit(instruction, (90, 650))


    # Runs the level screen
    elif in_level:
        
        screen.fill(LIGHT_GRAY)

        # Creates a hitbox for right and left button
        right_button_rect = right_button.get_rect(topleft=(800, 325))
        left_button_rect = left_button.get_rect(topleft=(50, 325))

        # Displays the correct page and level button for level 1
        if level == 1:
            screen.blit(right_button, (800, 325))
            level, left_click = level_change_buttons(right_button_rect, 1, level, left_click)
            level_selectors(level_one_selector, level_one_selector_hover)
            level_button_hover(right_button_hover, right_button_rect, 798, 323)

         # Displays the correct page and level button for level 2
        elif level == 2:
            screen.blit(right_button, (800, 325))
            screen.blit(left_button, (50, 325))
            level, left_click = level_change_buttons(right_button_rect, 1, level, left_click)
            level, left_click = level_change_buttons(left_button_rect, -1, level, left_click)
            level_selectors(level_two_selector, level_two_selector_hover)
            level_button_hover(right_button_hover, right_button_rect, 798, 323)
            level_button_hover(left_button_hover, left_button_rect, 48, 323)

         # Displays the correct page and level button for level 3
        else:
            screen.blit(left_button, (50, 325))
            level, left_click = level_change_buttons(left_button_rect, -1, level, left_click)
            level_selectors(level_three_selector, level_three_selector_hover)
            level_button_hover(left_button_hover, left_button_rect, 48, 323)


    # Runs the game
    if in_game: 

        # Changes the music
        menu_channel.set_volume(0)
        game_channel.set_volume(0.25)

        # Displays the title screen for each level
        if level_displayed:
            if level == 1:
                level_title_screen("The Busy City", 200, 300)
            elif level == 2:
                level_title_screen("Financial Center", 165, 300)
            elif level == 3: 
                level_title_screen("Crowded Forest", 165, 300)
            level_displayed = False

        # Spawns the objects, starts the timer and initiates the camera movement for level 1
        if level == 1:
            cameraX, cameraY = camera_movement(level_one_background.width, level_one_background.height, cameraX, cameraY)
            objects_spawning(1, level_one_background_image, 0)
            in_end_screen, in_game, timer_finished = timer(0.75, in_end_screen, in_game, timer_finished)

        # Spawns the objects, starts the timer and initiates the camera movement for level 2
        elif level == 2:
            cameraX, cameraY = camera_movement(level_two_background.width, level_two_background.height, cameraX, cameraY)
            objects_spawning(2, level_two_background_image, 3)
            in_end_screen, in_game, timer_finished = timer(1, in_end_screen, in_game, timer_finished)

        # Spawns the objects, starts the timer and initiates the camera movement for level 3
        elif level == 3: 
            cameraX, cameraY = camera_movement(level_three_background.width, level_three_background.height, cameraX, cameraY)
            objects_spawning(3, level_three_background_image, 6)
            in_end_screen, in_game, timer_finished = timer(1.5, in_end_screen, in_game, timer_finished)
        
        object_clicked, objects_found = objects_clicking(object_clicked, objects_found)

        # Switches to the end screen once all 3 objects are found
        if objects_found.count(1) >= 3:
            in_game = False
            in_end_screen = True
            level_completed = True


    # Runs the end screen
    elif in_end_screen:
        screen.fill(LIGHT_GRAY)

        if timer_finished:
            # Renders and displays the text
            times_up = end_screen_font.render("Time's Up!", True, GRAY)
            replay = end_screen_information.render("Replaying level in 5 seconds.", True, GRAY)
            screen.blit(times_up, (225, 250))
            screen.blit(replay, (100, 350))

            # Allows the screen to update 
            pygame.display.flip()
            pygame.time.delay(5000)

        elif level_completed:
            # Renders and displays the text
            completed = end_screen_font.render("Level Completed!", True, GRAY)
            next_level = end_screen_information.render("Next level in 5 seconds.", True, GRAY)
            screen.blit(completed, (85, 250))
            screen.blit(next_level, (165, 340))

            # Allows the screen to update 
            pygame.display.flip()
            pygame.time.delay(5000)

            # Moves to the next level
            # If the level is 3 then it goes back to level 1
            if level == 3:
                level = 1
                level_displayed = True
            else:
                level += 1
                level_displayed = True

        # Resets all neccessary variables
        timer_finished = False
        level_completed = False
        in_end_screen = False
        in_game = True
        ticks = pygame.time.get_ticks()
        object_clicked = [False] * 9
        objects_found = [0] * 9
        start_time = time.time()


    # Runs the legend screen
    if in_legend:

        # Creates the transparent rectangle for the legend
        legend_surface = pygame.Surface((225, 40), pygame.SRCALPHA)
        pygame.draw.rect(legend_surface, (10, 10, 10, 150), (0, 0, 225, 40))

        # Displays legend
        screen.blit(legend_surface, (15, 650))

        # Displays the objects for each level within the legend rectangle
        if level == 1:
            screen.blit(parking_sign, (35, 652))
            screen.blit(roof_panel, (87, 654))
            screen.blit(sun_chair, (160, 651))

        if level == 2:
            screen.blit(keyboard, (35, 659))
            screen.blit(equation, (105, 656))
            screen.blit(toolbox, (175, 660))

        if level == 3:
            screen.blit(person, (55, 653))
            screen.blit(rock, (115, 666))
            screen.blit(stump, (175, 659))


    # Pygame essentials 
    pygame.display.flip()
    clock.tick(60)

# Close the window and quit.
pygame.quit()