# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]

paddle1_pos = HALF_PAD_HEIGHT + 160
paddle2_pos = HALF_PAD_HEIGHT + 160
paddle1_vel = 0
paddle2_vel = 0
vel = 4
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists	
    ball_pos = [WIDTH/2, HEIGHT/2]

    f = random.randrange(120,240) / 100
    g = (random.randrange(60,180) / 100) + 0.5
    
    if direction == RIGHT:
        ball_vel = [f,-g]
    elif direction == LEFT:
        ball_vel = [-f,-g]
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_pos = HALF_PAD_HEIGHT + 160
    paddle2_pos = HALF_PAD_HEIGHT + 160
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
    spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]               
                
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]            
    
    #Draw ball
    canvas.draw_circle(ball_pos, 20, 1, 'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + 40 + paddle1_vel) <= HEIGHT and paddle1_vel > 0:
        paddle1_pos += paddle1_vel
    elif (paddle1_pos - 40) + paddle1_vel >= 0 and paddle1_vel < 0:
        paddle1_pos += paddle1_vel
    elif paddle2_pos + 40  + paddle2_vel <= HEIGHT and paddle2_vel > 0:
        paddle2_pos += paddle2_vel  
    elif paddle2_pos - 40 + paddle2_vel >= 0 and paddle2_vel < 0:
        paddle2_pos += paddle2_vel  
        
    # draw paddles
    canvas.draw_polygon([[0, (paddle1_pos - 40)], [PAD_WIDTH, (paddle1_pos - 40)],[PAD_WIDTH, (paddle1_pos + 40)],[0, (paddle1_pos + 40)]], 1, "White", "white") 
    canvas.draw_polygon([[600, (paddle2_pos - 40)], [(600 - PAD_WIDTH), (paddle2_pos - 40)],[600 - PAD_WIDTH, (paddle2_pos + 40)],[600, (paddle2_pos + 40)]], 1, "White", "white") 
    
    # determine whether paddle and ball collide    
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) or ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if (ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH)) and (ball_pos[1] >= (paddle1_pos - 40) and ball_pos[1] <= (paddle1_pos + 40)):
            ball_vel[0] = - (ball_vel[0] - .25) 
        elif (ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH)) and (ball_pos[1] >= (paddle2_pos - 40) and ball_pos[1] <= (paddle2_pos + 40)):
            ball_vel[0] = - (ball_vel[0] + .25)        
        else:
            if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
                score2 += 1
                spawn_ball(RIGHT)
            elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
                score1 += 1
                spawn_ball(LEFT)
    # draw scores
    canvas.draw_text(str(score1), [225,50], 36 ,"White")
    canvas.draw_text(str(score2), [350,50], 36 ,"White")    
        
        
def keydown(key):
    global paddle1_vel, paddle2_vel, vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
