import random
import pygame
from tkinter import *
from tkinter import messagebox

# Variables:
snake_x = 0 # Snake x position. 
snake_y = 0 # Snake y position.
movement_speed = 15  # Speed of snake movement.
current_direction = "none" # Direction of the snake currently.
rect_size = 20 # Size of the snake's head and food rectangle.
snake_segments = []  # List to store the segments of the snake
food_x = 0 # Food x position.
food_y = 0 # Food y position.
score = 0 # The score of the game.
is_up = False  # Boolean for up
is_down = False  # Boolean for down
is_left = False  # Boolean for left
is_right = False  # Boolean for right

#pygame.mixer.init()
#eat_sound = pygame.mixer.Sound("eat_sound.wav")  

# This makes the window/declares thew window.
def window():
    global score, score_label

    window = Tk()
    window.title("Snake Game")
    window.configure(bg = 'lightgray')
    window.resizable(False, False)
    
    canvas = Canvas(window, width = 400, height = 400)
    canvas.pack()

    set_initial_position()  # Set the initial position of the snake
    set_initial_position_food()  # Set the initial position of the food
    increase_snake_size()  # Increase the size of the snake (initialize the first segment)

    draw_snake(canvas)  
    draw_food(canvas)
    move_snake(canvas)  # Start the continuous movement
    
    # Create a label for the score display
    score_label = Label(window, text="Score: " + str(score), font=("Arial", 24))
    score_label.pack()

    # Bind arrow key events to the handle_key function
    window.bind("<KeyPress>", lambda event: handle_key(event, canvas))

    window.mainloop()

# Function to handle arrow key events
def handle_key(event, canvas):
    global current_direction, is_up, is_down, is_left, is_right

    key = event.keysym

    if key == "Up":
        current_direction = "up"
        is_up = True  
        is_down = False 
        is_left = False  
        is_right = False 
    elif key == "Down":
        current_direction = "down"
        is_up = False  
        is_down = True 
        is_left = False  
        is_right = False
    elif key == "Left":
        current_direction = "left"
        is_up = False  
        is_down = False 
        is_left = True  
        is_right = False
    elif key == "Right":
        is_up = False  
        is_down = False 
        is_left = False  
        is_right = True
        current_direction = "right"



# Function to continuously move the snake & among other things
def move_snake(canvas):
    global snake_x, snake_y, food_x, food_y, score

    if is_up:
        snake_y = snake_segments[0][1] - movement_speed
        snake_x = snake_segments[0][0]
    elif is_down:
        snake_y = snake_segments[0][1] + movement_speed
        snake_x = snake_segments[0][0]
    elif is_left:
        snake_x = snake_segments[0][0] - movement_speed
        snake_y = snake_segments[0][1]
    elif is_right:
        snake_x = snake_segments[0][0] + movement_speed
        snake_y = snake_segments[0][1]
        
    # Update the segments of the snake
    update_snake_segments()

    # Redraw the snake at its new position
    canvas.delete("snake")  # Remove the previous snake
    draw_snake(canvas)  # Draw the snake at the updated position

    # Check for game over
    if snake_x >= 400 or snake_y >= 400 or snake_x < 0 or snake_y < 0:
        # Show game over popup
        messagebox.showinfo("Game Over", "You lost the game!")
        quit()
    
    # Check for game over if snake collides with its own body
    if check_self_collision():
        # Show game over popup
        messagebox.showinfo("Game Over", "You lost the game!")
        quit()

    # Checks for the collision of the snake and the food.
    if (
        snake_x < food_x + rect_size
        and snake_x + rect_size > food_x
        and snake_y < food_y + rect_size
        and snake_y + rect_size > food_y
    ):
        # Snake ate the food, respawn it in a new location
        respawn_food(canvas)
        random_score_number = random.randint(1, 10)
        score += random_score_number
        update_score_label()  # Call the function to update the score label
        increase_snake_size()  # Increase the size of the snake

    # Schedule the next movement
    canvas.after(150, lambda: move_snake(canvas))

# Function to set the initial position of the snake randomly
def set_initial_position():
    global snake_x, snake_y
    snake_x = random.randint(0, 380)  # Generate a random x-coordinate between 0 and 380
    snake_y = random.randint(0, 380)  # Generate a random y-coordinate between 0 and 380

# Function to draw the snake
def draw_snake(canvas):
    for segment in snake_segments:
        x, y = segment
        canvas.create_rectangle(x, y, x + rect_size, y + rect_size, fill="red", tags="snake")


# Function to draw the food for our snake.
def draw_food(canvas):
    global food_x, food_y
    
    canvas.create_rectangle(food_x, food_y, food_x + rect_size, food_y +rect_size, fill = "blue", tags = "food")

# Function to set the initial position of the food randomly
def set_initial_position_food():
    global food_x, food_y
    food_x = random.randint(0, 380)  # Generate a random x-coordinate between 0 and 380
    food_y = random.randint(0, 380)  # Generate a random y-coordinate between 0 and 380

# Function to respawn the food at a new position
def respawn_food(canvas):
    global food_x, food_y
    canvas.delete("food")  # Remove the previous food

    food_x = random.randint(0, 380)  # Generate a random x-coordinate between 0 and 380
    food_y = random.randint(0, 380)  # Generate a random y-coordinate between 0 and 380

    draw_food(canvas)  # Draw the food at the new position

# Function to update the score label
def update_score_label():
    global score, score_label
    score += random.randint(1, 10)
    score_label.config(text="Score: " + str(score))

# Function to increase the size of the snake
def increase_snake_size():
    global snake_x, snake_y, snake_segments

    new_segment = (snake_x, snake_y)
    snake_segments.insert(0, new_segment)

# Function to update the snake segments based on the current direction
def update_snake_segments():
    global snake_x, snake_y, snake_segments

    # Create a new segment for the head of the snake
    new_segment = (snake_x, snake_y)

    # Update the snake_segments list with the new segment
    snake_segments.insert(0, new_segment)

    # Remove the last segment if the snake has grown
    if len(snake_segments) > score:
        snake_segments.pop()

# It says in the name.
def check_self_collision():
    global snake_x, snake_y, snake_segments

    # Check if the head of the snake collides with any of its segments
    for segment in snake_segments[1:]:
        if snake_x == segment[0] and snake_y == segment[1]:
            return True

    return False

# Think of this as our main method. 
window()
