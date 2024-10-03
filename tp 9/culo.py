import py5

# Global variables
paddle1_y = paddle2_y = 0
paddle_width = paddle_height = 0
paddle_speed = ball_size = 0
ball_x = ball_y = ball_dx = ball_dy = 0
player1_score = player2_score = 0
background_image = None
game_mode = "menu"  # "menu", "multiplayer", "singleplayer"
ball_speed_increase = 1.1
max_ball_speed = 8
keys = set()

def setup():
    py5.size(561, 262)
    global paddle_width, paddle_height, paddle_speed, ball_size
    global ball_x, ball_y, ball_dx, ball_dy
    global paddle1_y, paddle2_y, player1_score, player2_score, background_image
    background_image = py5.load_image("cojones.jpg")
    paddle_width = 20
    paddle_height = 100
    paddle_speed = 7
    ball_size = 20
    reset_game()

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx = 5
    ball_dy = 3
    paddle1_y = py5.height / 2 - paddle_height / 2
    paddle2_y = py5.height / 2 - paddle_height / 2
    player1_score = 0
    player2_score = 0

def draw():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score, background_image
    
    if background_image is not None:
        py5.image(background_image, 0, 0, py5.width, py5.height)

    if game_mode == "menu":
        display_menu()
    else:
        play_game()

def display_menu():
    py5.background(0)
    py5.fill(255)
    py5.text_size(32)
    py5.text_align(py5.CENTER)
    py5.text("Selecciona un Modo", py5.width / 2, 80)
    py5.text_size(24)
    py5.text("1. Multijugador", py5.width / 2, 120)
    py5.text("2. Contra Computadora", py5.width / 2, 160)
    py5.text("Presiona 1 o 2 para jugar", py5.width / 2, 220)

def play_game():
    global paddle1_y, paddle2_y, player1_score, player2_score
    global ball_x, ball_y, ball_dx, ball_dy
    # Draw paddles
    py5.rect(30, paddle1_y, paddle_width, paddle_height)  # Left paddle
    py5.rect(py5.width - 30 - paddle_width, paddle2_y, paddle_width, paddle_height)  # Right paddle
    
    # Draw the ball
    py5.ellipse(ball_x, ball_y, ball_size, ball_size)
    
    # Draw the score
    py5.text_size(32)
    py5.text_align(py5.CENTER)
    py5.fill(255)
    py5.text(f"{player1_score} - {player2_score}", py5.width / 2, 40)
    
    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy
    
    # Ball bounces off top and bottom
    if ball_y <= ball_size / 2 or ball_y >= py5.height - ball_size / 2:
        ball_dy *= -1
    
    # Check collisions with paddles
    if ball_x - ball_size / 2 <= 30 + paddle_width:
        if paddle1_y < ball_y < paddle1_y + paddle_height:
            ball_dx *= -1
            ball_x = 30 + paddle_width + ball_size / 2
            increase_ball_speed()  # Aumentar la velocidad de la pelota en la colisión
    
    if ball_x + ball_size / 2 >= py5.width - 30 - paddle_width:
        if paddle2_y < ball_y < paddle2_y + paddle_height:
            ball_dx *= -1
            ball_x = py5.width - 30 - paddle_width - ball_size / 2
            increase_ball_speed()  # Aumentar la velocidad de la pelota en la colisión
    
    # Ball out of bounds
    if ball_x < 0:
        player2_score += 1
        reset_ball()
    
    if ball_x > py5.width:
        player1_score += 1
        reset_ball()

    # Paddle movement control
    if 'w' in keys and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if 's' in keys and paddle1_y < py5.height - paddle_height:
        paddle1_y += paddle_speed
    
    # AI control for single-player mode
    if game_mode == "singleplayer":
        ai_control()

    # Control for player 2 in multiplayer
    if 'o' in keys and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if 'l' in keys and paddle2_y < py5.height - paddle_height:
        paddle2_y += paddle_speed

def ai_control():
    global paddle1_y, paddle2_y
    # Basic AI that follows the ball
    if ball_y < paddle2_y + paddle_height / 2 and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if ball_y > paddle2_y + paddle_height / 2 and paddle2_y < py5.height - paddle_height:
        paddle2_y += paddle_speed

def increase_ball_speed():
    global ball_dx, ball_dy
    ball_dx *= ball_speed_increase
    ball_dy *= ball_speed_increase

    if abs(ball_dx) > max_ball_speed:
        ball_dx = max_ball_speed * (1 if ball_dx > 0 else -1)
    if abs(ball_dy) > max_ball_speed:
        ball_dy = max_ball_speed * (1 if ball_dy > 0 else -1)

def key_pressed():
    global keys, game_mode
    if game_mode == "menu":
        if py5.key == '1':
            game_mode = "multiplayer"
            reset_game()
        elif py5.key == '2':
            game_mode = "singleplayer"
            reset_game()
    else:
        keys.add(py5.key)

def key_released():
    global keys
    keys.discard(py5.key)

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx *= -1
    ball_dy = py5.random(-3, 3)

if __name__ == "__main__":
    py5.run_sketch()
