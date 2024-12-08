import pygame
import random
import time

pygame.init()
pygame.font.init()

display_width = 1200
display_height = 600

black = (0,0,0)
white = (255,255,255)
blue = (9,148,220)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Fence!')
clock = pygame.time.Clock()

leftImg = pygame.image.load('leftImg.png')
rightImg = pygame.image.load('rightImg.png')
stripImg = pygame.image.load('strip.png')
leftImgattack = pygame.image.load('leftImgattack.png')
leftImglunging = pygame.image.load('leftImglunging.png')
rightImgattack = pygame.image.load('rightImgattack.png')
rightImglunging = pygame.image.load('rightImglunging.png')
rightImgparry = pygame.image.load('rightImgparry.png')
leftImgparry = pygame.image.load('leftImgparry.png')
controlsImg = pygame.image.load('controls.png')

hit_time = 0

score_left = 0
score_right = 0

wins_left = 0
wins_right = 0

attack_left = False
parry_left = False

attack_right = False
parry_right = False

tick_count_attack_r = 0
tick_count_attack_l = 0

tick_count_parry_r = 0
tick_count_parry_l = 0

right_ai = False
left_ai = False

font = pygame.font.Font("freesansbold.ttf", 100)
small_font = pygame.font.Font("freesansbold.ttf",(35))
smaller_font = pygame.font.Font("freesansbold.ttf",(22))
def left_character(x,y):
	global tick_count_attack_l

	#decide which left sprite to display
	if attack_left == False and parry_left == False:
		gameDisplay.blit(leftImg,(x,y))
	elif attack_left == True:
		gameDisplay.blit(leftImgattack,(x,y))
	elif parry_left == True:
		gameDisplay.blit(leftImglunging,(x,y))

def strip():
	gameDisplay.blit(stripImg,(0,0))
	gameDisplay.blit(controlsImg,(0,0))

def game_loop():
	global score_right,score_left,attack_right,attack_left,parry_left,\
		parry_right, tick_count_attack_r,tick_count_attack_l,hit_time, \
		tick_count_parry_r,tick_count_parry_l,font,wins_right,wins_left,rightImg, \
		right_ai,left_ai

	attack_cooldown_r = 0
	attack_cooldown_l = 0

	hit_left = False
	hit_right = False

	Game_Exit = False

	xl = display_width * 0.33
	xr = display_width * 0.5

	xl_change = 0
	xr_change = 0

	touch_time = time.time()

	ai_difficulty = ["off","easy","medium","hard"]
	ai_toggle_R = 0
	ai_toggle_L = 0
	easy = []
	medium = []
	hard = []

	while not Game_Exit:
		rand_num = random.randint(0,40)
		rand_attack = random.randint(0,100)
		rand_num_l = random.randint(0,40)
		rand_attack_l = random.randint(0,100)
	
		duration = '%.2f' % (time.time() - touch_time)		

		xl_change = 0
		xr_change = 0

		#scoring for moving off of the strip:
		if xl <= 50:
			score_right += 1
			xl = display_width * 0.33
			xr = display_width * 0.5
		if xr >= 950:
			score_left += 1
			xl = display_width * 0.33
			xr = display_width * 0.5
		#reset in event that players cross each other:
		if xr - xl <= -100:
			xl = display_width * 0.33
			xr = display_width * .5

	#events:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				#controls for the right character
				if event.key == pygame.K_LEFT and attack_cooldown_r == 0:
					xr_change = -25
				elif event.key == pygame.K_LEFT:
					#print("can't move: attack coolown is ", attack_cooldown_r)
					pass
				if event.key == pygame.K_RIGHT and attack_cooldown_r == 0:
					xr_change = 25
				if event.key == pygame.K_UP and attack_cooldown_r == 0:
					attack_right = True
					tick_count_attack_r += 1
					attack_cooldown_r += 1
					xr -= 75
				if event.key == pygame.K_DOWN and tick_count_parry_r == 0:
					parry_right = True
					xr += 20

				#controls for the left character
				if event.key == pygame.K_a and attack_cooldown_l == 0:
					xl_change = -25
				if event.key == pygame.K_d and attack_cooldown_l == 0:
					xl_change = 25
				if event.key == pygame.K_w and attack_cooldown_l == 0:
					attack_left = True
					tick_count_attack_l += 1
					attack_cooldown_l += 1
					xl += 25
				if event.key == pygame.K_s:
					parry_left = True
					xl -= 20

				#reset the score
				if event.key == pygame.K_o:
					score_right = 0
					score_left = 0	
					wins_right = 0
					wins_left = 0
				#leave the game
				if event.key == pygame.K_ESCAPE:
					Game_Exit = True

				if event.key == pygame.K_i:
					right_ai = not right_ai
					if ai_toggle_R < 3:
						ai_toggle_R += 1
						print("right difficulty is: ", ai_difficulty[ai_toggle_R])
					else:
						ai_toggle_R = 0
						print("right difficulty is: ", ai_difficulty[ai_toggle_R])

				if event.key == pygame.K_u:
					left_ai = not left_ai
					if ai_toggle_L < 3:
						ai_toggle_L += 1
						print("left difficulty is: ", ai_difficulty[ai_toggle_L])
					else:
						ai_toggle_L = 0
						print("left difficulty is: ", ai_difficulty[ai_toggle_L])


		xr += xr_change
		xl += xl_change
		

	#ai difficulty variables
		easy = [3,2,5,0]
		medium = [4,3,6,1]
		hard = [6,6,10,4]

		left = [0,0,0,0]
		right = [0,0,0,0]

	#set difficulty values
		if ai_toggle_R == 1:
			right = easy
		elif ai_toggle_R == 2:
			right = medium
		elif ai_toggle_R == 3:
			right = hard

		if ai_toggle_L == 1:
			left = easy
		elif ai_toggle_L == 2:
			left = medium
		elif ai_toggle_L == 3:
			left = hard

#render the frame:
		gameDisplay.fill(blue)
		strip()

		#AI
		if ai_toggle_R > 0:
			
			if xr-xl > 90 and right[0] > rand_num and tick_count_attack_r == 0:
				xr -= 25
			elif xr-xl < 190 and right[1] > rand_num and tick_count_attack_r == 0:
				xr += 25
			elif (xr-xl < 130 and tick_count_attack_l > 0) and (right[2] > rand_num and tick_count_parry_r == 0) and (tick_count_attack_r == 0):
				#print("______parry right")
				parry_right = True
				xr += 20
			elif xr-xl < 110 and tick_count_attack_r == 0 and rand_attack <= right[3]:	
				#print("_____attack right")
				attack_right = True
				tick_count_attack_r += 1
				attack_cooldown_r += 1
				xr -= 75

		if ai_toggle_L > 0:
			if xr-xl > 90 and left[0] > rand_num_l and tick_count_attack_l <= 0:
				xl += 25
			elif xr-xl < 190 and left[1] > rand_num_l and tick_count_attack_l <= 0:
				xl -= 25
			elif (xr-xl < 130 and tick_count_attack_r > 0) and (left[2] > rand_num_l and tick_count_parry_l == 0) and (tick_count_attack_l == 0) :
				#print("parry left______")
				parry_left = True
				xl -= 20
			elif xr-xl < 110 and tick_count_attack_l == 0 and rand_attack_l <= left[3]:
				#print("attack left______")
				attack_left = True
				tick_count_attack_l += 1
				attack_cooldown_l += 1
				xl += 40

	#decide which right sprite to display:
		if attack_right == False and parry_right == False and tick_count_attack_r == 0 and tick_count_parry_r == 0:
			gameDisplay.blit(rightImg,(xr,300))
		elif attack_right == True and tick_count_attack_r == 0:
			tick_count_attack_r += 1
			gameDisplay.blit(rightImgattack,(xr,300))
		elif 0 < tick_count_attack_r < 8:
			attack_right = False
			tick_count_attack_r += 1
			gameDisplay.blit(rightImgattack,(xr,300))
		elif tick_count_attack_r >= 8 and tick_count_attack_r < 20:
			attack_right = False
			tick_count_attack_r += 1
			gameDisplay.blit(rightImglunging,(xr,315))

		elif parry_right == True and 0 <= tick_count_parry_r < 20:
			tick_count_parry_r += 1
			gameDisplay.blit(rightImgparry,(xr,300))
		elif parry_right == True and tick_count_parry_r >= 20:
			tick_count_parry_r = 0
			parry_right = False
			attack_right = False
			gameDisplay.blit(rightImgparry,(xr,300)) 

		#reset the right sprite after an attack:
		if tick_count_attack_r == 20:
			xr += 80
			tick_count_attack_r = 0



	#decide which left sprite to display:
		if attack_left == False and parry_left == False and tick_count_attack_l == 0:
			gameDisplay.blit(leftImg,(xl,300))
		elif attack_left == True and tick_count_attack_l == 0:
			tick_count_attack_l += 1
			gameDisplay.blit(leftImgattack,(xl,300))
		elif 0 < tick_count_attack_l < 8:
			attack_left = False
			tick_count_attack_l += 1
			gameDisplay.blit(leftImgattack,(xl,300))
		elif tick_count_attack_l >= 8 and tick_count_attack_l < 20:
			attack_left = False
			tick_count_attack_l += 1
			gameDisplay.blit(leftImglunging,(xl,315))

		elif parry_left == True and 0 <= tick_count_parry_l < 20:
			tick_count_parry_l += 1
			gameDisplay.blit(leftImgparry,(xl,300))
		elif tick_count_parry_l >= 20:
			tick_count_parry_l = 0
			parry_left = False
			attack_left = False
			gameDisplay.blit(leftImgparry,(xl,300)) 

		#reset the left sprite after an attack:
		if tick_count_attack_l == 20:
			xl -= 30
			tick_count_attack_l = 0
			

	#attack cooldowns:
		if 1 <= attack_cooldown_l < 30:
			attack_cooldown_l += 1
		elif attack_cooldown_l == 30:
			attack_cooldown_l = 0		

		if 1 <= attack_cooldown_r < 30:
			attack_cooldown_r += 1
		elif attack_cooldown_r == 30:
			attack_cooldown_r = 0	


	#hit detection:
		#reset after hit:
		if hit_right == True and hit_time == 30:
			xl = display_width * 0.33
			xr = display_width * 0.5
			hit_time = 0
		if hit_left == True and hit_time == 30:
			xl = display_width * 0.33
			xr = display_width * 0.5
			hit_time = 0

		#detect hit:
		if tick_count_attack_l == 19 and (xr-xl) <= 85 and parry_right == False:
			print("!!_touch left_!!\n")
			score_left += 1
			xl = display_width * 0.35
			xr = display_width * 0.5
			hit_time += 1
			touch_time = time.time()
		if tick_count_attack_r == 19 and (xr-xl) <= 45 and parry_left == False:
			print("!!_touch right_!!\n")
			score_right += 1
			xl = display_width * 0.33
			xr = display_width * 0.43
			hit_right == True
			hit_time += 1
			touch_time = time.time()

	#disable hits after a score:
		if 30 > hit_time >= 1:
			hit_time += 1



	#convert touches to wins:
		if score_left == 5:
			wins_left += 1
			score_left = 0
			score_right = 0
		if score_right == 5:
			wins_right += 1
			score_right = 0
			score_left = 0
		
		clock.tick(35)

		show_score = font.render((str(score_left)+ " : "+ str(score_right)), False, (0,0,0))
		gameDisplay.blit(show_score, (490, 100))

		show_score = small_font.render((str(wins_left)), False, (0,0,0))
		gameDisplay.blit(show_score, (508, 50))

		show_score = small_font.render((str(wins_right)), False, (0,0,0))
		gameDisplay.blit(show_score, (652, 50))

		show_score = small_font.render((str(duration)), False, (0,0,0))
		gameDisplay.blit(show_score, (555, 7))

		show_score = smaller_font.render((str("Right AI difficulty: "+ai_difficulty[ai_toggle_R])), False, (0,0,0))
		gameDisplay.blit(show_score, (900, 65))

		show_score = smaller_font.render((str("Left AI difficulty:   "+ai_difficulty[ai_toggle_L])), False, (0,0,0))
		gameDisplay.blit(show_score, (900, 20))



		pygame.display.update()


game_loop()
pygame.quit()
quit()