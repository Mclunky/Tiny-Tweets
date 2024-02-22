import pygame
import random
import os
import math
import time
#need to delete the remaining sprite after a finch moves
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
YOUTUBE_WIDTH = (1200)
YOUTUBE_HEIGHT = (700)

# Calculate the position to center the YouTube area
youtube_x = (SCREEN_WIDTH - YOUTUBE_WIDTH) // 2
youtube_y = 0
YOUTUBE_AREA = (youtube_x, youtube_y, YOUTUBE_WIDTH, YOUTUBE_HEIGHT)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tiny Tweet')

def scale_image(image, target_width, target_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height

    if target_width / target_height >= aspect_ratio:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

    return pygame.transform.scale(image, (new_width, new_height))


class Background(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)  # Call Sprite initializer
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "background.png")
        loaded_image = pygame.image.load(image_path)
        self.image = scale_image(loaded_image, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def draw(self, surface):
        surface.blit(self.image, self.rect)



class Youtube_Background(pygame.sprite.Sprite):
    def __init__(self, location, size):  # Add 'size' as a parameter
        pygame.sprite.Sprite.__init__(self)  # Call Sprite initializer
        script_dir = os.path.dirname(os.path.abspath(__file__))
        youtube_area_image_path = os.path.join(script_dir, "background_youtube_place.png")

        # Load the image and convert it for better performance
        loaded_image = pygame.image.load(youtube_area_image_path).convert_alpha()

        # Resize the image
        self.image = pygame.transform.scale(loaded_image, size)

        # Set the rectangle for positioning
        self.rect = self.image.get_rect(topleft=location)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Finch:
    def __init__(self, x, y):
        self.dead = False  # Indicates if the finch is dead
        self.death_time = None  # Tracks when the finch died
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'finch_image.png')
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (120, 120))  # Resize the image
        self.x = x
        self.y = y
        self.speed = random.randint(2, 5)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hungerness = 0 
        self.facing_right = True  # Additional attribute to track sprite direction

    def decrease_hungerness(self):
        self.hungerness = max(0, self.hungerness - 10)     
        
    def increase_hungerness(self):
        self.hungerness = min(100, self.hungerness + 1)   


    def move_towards_target(self, target_x, target_y):
        if self.hungerness < 100:

            # Calculate direction vector towards the target
            direction_x = target_x - self.x
            direction_y = target_y - self.y
            if target_x < self.x:
                self.facing_right = False
            else:
                self.facing_right = True

            # Normalize the direction
            distance = math.sqrt(direction_x**2 + direction_y**2)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance

        
                    # Move towards the target
            self.x += direction_x * self.speed * random.choice([3, 1])
            self.y += direction_y * self.speed * random.choice([2, 1])
            # Limit the finch's y position to the bottom 60 pixels of the screen
            self.y = min(self.y, SCREEN_HEIGHT - self.image.get_height())

            # If you also want to prevent the finch from going off the bottom edge:
            self.y = max(self.y, SCREEN_HEIGHT - (self.image.get_height()+30))
    def move(self):
        if self.hungerness < 100:

            new_x = self.x + self.speed * random.choice([1, -1])
            new_y = self.y + self.speed * random.choice([1, -1])

            self.x = new_x
            self.y = new_y
            
            # Limit the finch's y position to the bottom 60 pixels of the screen
            self.y = min(self.y, SCREEN_HEIGHT - self.image.get_height())

            # If you also want to prevent the finch from going off the bottom edge:
            self.y = max(self.y, SCREEN_HEIGHT - (self.image.get_height()+30))
            
    def death(self):
        current_time = time.time()
        if not self.dead:  # Only run this block if the finch just died
            #10 is the time for it to be dead before it disappears
            if current_time - self.death_time >= 10:
                self.dead = True
                self.death_time = time.time()  # Record the time of death

                # Flip the image upside down and grey it out
                self.image = pygame.transform.flip(self.image, False, True)
                self.image.fill((128, 128, 128, 128), None, pygame.BLEND_RGBA_MULT)

                # Adjust the y position to compensate for the flip
                self.y = self.y-self.image.get_height()  # Adjust as needed    



      

    def draw(self, surface):
        if self.facing_right:
            surface.blit(self.image, (self.x, self.y))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, (self.x, self.y))
            

#class MallardDuck:
#    def __init__(self, x, y):
#        script_dir = os.path.dirname(os.path.abspath(__file__))
#        image_path = os.path.join(script_dir, 'MallardDuck.png')
#        self.image = pygame.image.load(image_path)
#        self.image = pygame.transform.scale(self.image, (297, 198))  # Resize the image
#        self.x = x
#        self.y = y
#        self.speed = random.randint(5, 9)
#        self.width = self.image.get_width()
#        self.height = self.image.get_height()
#        self.hungerness = 0 # Max hungerness
#        self.facing_right = True  # Additional attribute to track sprite direction
#
#    def decrease_hungerness(self):
#        # Decrease hungerness by 10, but not below 0 and not higher than 100
#        self.hungerness = max(0, self.hungerness - 10)     
#        
#    def increase_hungerness(self):
#        # Decrease hungerness by 10, but not below 0 and not higher than 100
#        self.hungerness = min(100, self.hungerness + 5)        
#        
#    def death(self):
#        MallardDuck.remove(MallardDuck)  # die


           



#towards_target(self, target_x, target_y):
#        if self.hungerness < 100:

            # Calculate direction vector towards the target
#            direction_x = target_x - self.x
#            direction_y = target_y - self.y
#            if target_x < self.x:
#                self.facing_right = False
#            else:
#                self.facing_right = True####

            # Normalize the direction
#            distance = math.sqrt(direction_x**2 + direction_y**2)
#            if distance > 0:
#                direction_x /= distance
#                direction_y /= distance

            # Move towards the target
#            self.x += direction_x * self.speed * random.choice([8, 1])
#            self.y += direction_y * self.speed * random.choice([4, 1])
            # Limit the finch's y position to the bottom 60 pixels of the screen#
#            self.y = min(self.y, SCREEN_HEIGHT - self.image.get_height())

            # If you also want to prevent the finch from going off the bottom edge:
#            self.y = max(self.y, SCREEN_HEIGHT - (self.image.get_height()+30))
#    def move(self):
        
#        if self.hungerness < 100:
#            new_x = self.x + self.speed * random.choice([5, -5])
#            new_y = self.y + self.speed * random.choice([3, -1])

#            self.x = new_x
#            self.y = new_y
            
            # Limit the finch's y position to the bottom 60 pixels of the screen
#            self.y = min(self.y, SCREEN_HEIGHT - self.image.get_height())

            # If you also want to prevent the finch from going off the bottom edge:
#            self.y = max(self.y, SCREEN_HEIGHT - (self.image.get_height()+30))
      

#    def draw(self, surface):
#        if self.facing_right:
#            surface.blit(self.image, (self.x, self.y))
#        else:
#            flipped_image = pygame.transform.flip(self.image, True, False)
#            surface.blit(flipped_image, (self.x, self.y))
        
class FoodPellet:
    def __init__(self, x, y, radius=5, color=(255, 255, 0)):  # Yellow color
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.fall_speed = 7  # Speed at which the pellet falls

    def update(self):
        # If the pellet is above the threshold, move it down
        if self.y < SCREEN_HEIGHT - 20 - self.radius:
            self.y += self.fall_speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


pellets = []

def run_game():
    clock = pygame.time.Clock()
    finches = [Finch(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(3)]
    #start_ticks = pygame.time.get_ticks()
    
  #  mallard_ducks = [MallardDuck(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(1)]
    
    #initializing the mallard duck first because the delay is too long
   # for mallard_duck in mallard_ducks:
   #     mallard_duck.move()


    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse click position
                (x, y) = pygame.mouse.get_pos()
                # Create a new pellet at this position
                pellets.append(FoodPellet(x, y))
        
        # Clear the screen or redraw the background
        background = Background((0, 0))
        background.draw(screen)

        # Create the YouTube area in the top center of the screen
        youtube_background = Youtube_Background((youtube_x, youtube_y), (YOUTUBE_WIDTH, YOUTUBE_HEIGHT))
        youtube_background.draw(screen)

        # Draw the food pellets
        for food_pellet in pellets:
            food_pellet.update()
            food_pellet.draw(screen)

        # Update and draw finches
        
        

        # Check if it's time to move the ducks
        #if pygame.time.get_ticks() - start_ticks > 800:
        #    start_ticks = pygame.time.get_ticks()
           
            #for mallard_duck in mallard_ducks:
             #   mallard_duck.increase_hungerness()
             #   if mallard_duck.hungerness >= 100:
             #       mallard_duck.remove(mallard_ducks)  # die
             
#                if len(pellets) > 0:
#                    # Find the closest pellet for each mallard duck
#                    closest_pellet = min(pellets, key=lambda pellet: (pellet.x - mallard_duck.x)**2 + (pellet.y - mallard_duck.y)**2)
#                    mallard_duck.move_towards_target(closest_pellet.x, closest_pellet.y)
#                    mallard_duck_rect = pygame.Rect(mallard_duck.x, mallard_duck.y, mallard_duck.width, mallard_duck.height)
#                    for pellet in pellets[:]:  # Copy the list to avoid modifying it during iteration
#                        pellet_rect = pygame.Rect(pellet.x - pellet.radius, pellet.y - pellet.radius, pellet.radius * 2, pellet.radius * 2)
#                        if mallard_duck_rect.colliderect(pellet_rect):
#                            pellets.remove(pellet)  # Remove the pellet
#                            mallard_duck.decrease_hungerness()  # Decrease the duck's hungerness
#                else:
#                    mallard_duck.move()
        for finch in finches:
            finch.move()
            finch.increase_hungerness()
            if finch.hungerness >= 100:
                finch.death()
                finches.remove(finch)

            hungerness_bar_rect = pygame.Rect(finch.x + 10, finch.y - 10, finch.hungerness, 5)  # Draw above the finch
            pygame.draw.rect(screen, (255, 0, 0), hungerness_bar_rect)  # Red bar
            
            
            if len(pellets) > 0:
                # Find the closest pellet for each finch
                closest_pellet = min(pellets, key=lambda pellet: (pellet.x - finch.x)**2 + (pellet.y - finch.y)**2)
                finch.move_towards_target(closest_pellet.x, closest_pellet.y)
                finch_rect = pygame.Rect(finch.x, finch.y, finch.width, finch.height)
                for pellet in pellets[:]:  # Copy the list to avoid modifying it during iteration
                    pellet_rect = pygame.Rect(pellet.x - pellet.radius, pellet.y - pellet.radius, pellet.radius * 2, pellet.radius * 2)
                    if finch_rect.colliderect(pellet_rect):
                        pellets.remove(pellet)  # Remove the pellet
                        finch.decrease_hungerness()  # Decrease the finch's hungerness
            finch.draw(screen)
                

        # Draw each duck and its hungerness bar
#        for mallard_duck in mallard_ducks:
#            hungerness_bar_rect = pygame.Rect(mallard_duck.x, mallard_duck.y - 10, mallard_duck.hungerness, 5)
#            pygame.draw.rect(screen, (255, 0, 0), hungerness_bar_rect)
#            mallard_duck.draw(screen)

      
        # Update the display      
        pygame.display.flip()

    pygame.quit()
run_game()



#The bird must go kill when reach 100 hunger
#add new finches
#add moving clouds
#add delay to eating the next pellets after one is consumed
#add money system for food idk
#
#
#
#
#
#
#
#
#
#
#