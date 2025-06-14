import pygame, sys, random

def draw_floor():
	screen.blit(floor_surface, (floor_x_pos,900))
	screen.blit(floor_surface, (floor_x_pos+576,900))
	
def create_tree():
	random_tree_pos = random.choice(tree_height)
	bottom_tree = tree_surface.get_rect(midtop = (700,random_tree_pos))
	top_tree = tree_surface.get_rect(midbottom = (700,random_tree_pos-300))
	return bottom_tree, top_tree

def move_trees(trees):
	for tree in trees:
		tree.centerx -= 5
	return trees
	
def draw_trees(trees):
	for tree in trees:
		if tree.bottom >= 1024:
			screen.blit(tree_surface, tree)
		else:
			flip_tree = pygame.transform.flip(tree_surface,False,True)
			screen.blit(flip_tree, tree)

def check_collision(trees):
	for tree in trees:
		if dzik_rect.colliderect(tree):
			death_sound.play()
			return False
			
	if dzik_rect.top <= -100 or dzik_rect.bottom >=900:
		death_sound.play()
		return False
	
	return True
			
def rotate_dzik(dzik):
	new_dzik = pygame.transform.rotozoom(dzik, -dzik_movement*3, 1)
	return new_dzik
	
def dzik_animation():
	new_dzik = dzik_frames[dzik_index]
	new_dzik_rect = new_dzik.get_rect(center = (100,dzik_rect.centery))
	return new_dzik,dzik_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface, score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface, score_rect)
		
		high_score_surface = game_font.render(f'Highscore: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/flappy-font.ttf',40)

# zmienne gry
gravity = 0.25
dzik_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/lane.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (576,150))
floor_x_pos = 0

dzik_down = pygame.transform.scale(pygame.image.load('assets/dzik-down.png').convert_alpha(), (75,50))
dzik_mid = pygame.transform.scale(pygame.image.load('assets/dzik-mid.png').convert_alpha(), (75,50))
dzik_up = pygame.transform.scale(pygame.image.load('assets/dzik-up.png').convert_alpha(), (75,50))
dzik_frames = [dzik_down, dzik_mid, dzik_up]
dzik_index = 0
dzik_surface = dzik_frames[dzik_index]
dzik_rect = dzik_surface.get_rect(center = (100,512))

DZIKFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(DZIKFLAP,200)

tree_surface = pygame.image.load('assets/tree.png').convert_alpha()
tree_surface = pygame.transform.scale(tree_surface, (100,670))
tree_list = []
SPAWNTREE = pygame.USEREVENT
pygame.time.set_timer(SPAWNTREE, 1200)
tree_height = [400, 500, 600, 700, 800]

game_over_surface = game_font.render(f'Flappy Dzik',True,(255,255,255))
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sounds/sfx_point.wav')
score_sound_countdown = 100

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active == True:
				dzik_movement = 0
				dzik_movement -= 9
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				tree_list.clear()
				dzik_rect.center = (100,512)
				dzik_movement = 0
				score = 0
				
		if event.type == SPAWNTREE:
			tree_list.extend(create_tree())
		if event.type == DZIKFLAP:
			if dzik_index < 2:
				dzik_index += 1
			else:
				dzik_index = 0
			dzik_surface,dzik_rect = dzik_animation()
	screen.blit(bg_surface,(0,0))

	if game_active:
		# dzik
		dzik_movement += gravity
		rotated_dzik = rotate_dzik(dzik_surface)
		dzik_rect.centery += dzik_movement
		screen.blit(rotated_dzik, dzik_rect)
		game_active = check_collision(tree_list)
		
		# drzew
		tree_list = move_trees(tree_list)
		draw_trees(tree_list)
		score += 0.01
		score_display('main_game')
		score_sound_countdown -= 1
		if score_sound_countdown <= 0:
			score_sound.play()
			score_sound_countdown = 100
	else:
		screen.blit(game_over_surface, game_over_rect)
		high_score = update_score(score, high_score)
		score_display('game_over')
		
	
	# podlog
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0
	
	pygame.display.update()
	clock.tick(60)
