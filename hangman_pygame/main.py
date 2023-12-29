import pygame
from button import Button
from wordList import word_list
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 1200, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images
images = []
for i in range(7):
    image = pygame.image.load("stages/stage" + str(i) + ".png")
    images.append(image)

# import music
select_sfx = pygame.mixer.Sound("music/select_sound.mp3")
winning_sfx = pygame.mixer.Sound("music/winning_sound.wav")
losing_sfx = pygame.mixer.Sound("music/losing_sound.wav")
hint_open_sfx = pygame.mixer.Sound("music/hint_open.wav")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (202, 228, 241)

def draw_word(word, guessed):

  display_word = ""
  for letter in word:
    if letter in guessed:
      display_word += letter + " "
    else:
      display_word += "_ "
  text = WORD_FONT.render(display_word, 1, BLACK)
  win.blit(text, (400, 200))

def draw_letters_button(letters, radius, status):

  for letter in letters:
    x, y, ltr, visible = letter
    if visible:
      pygame.draw.circle(win, BLACK, (x, y), radius, 3)
      text = LETTER_FONT.render(ltr, 1, BLACK)
      win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

  win.blit(images[status], (150, 100))

def draw_hint (text):
  win.blit(LETTER_FONT.render(text, 1, BLACK), (400, 120))

def final(message, answer):
  pygame.time.delay(500)
  win.fill(BG)
  text1 = WORD_FONT.render(message, 1, BLACK)
  win.blit(text1, (WIDTH / 2 - text1.get_width() / 2, HEIGHT / 2 - text1.get_height() / 2 - 100))
  text2 = WORD_FONT.render(answer, 1, BLACK)
  win.blit(text2, (WIDTH / 2 - text2.get_width() / 2, HEIGHT / 2 - text2.get_height() / 2 - 200))

  end_game = True

  while end_game:
    PLAY_AGAIN_BUTTON = Button(image=pygame.image.load("Rect.png"), pos=(600, 270), text_input="PLAY AGAIN", font=LETTER_FONT, base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("Rect.png"), pos=(600, 400), text_input="QUIT", font=LETTER_FONT, base_color="#d7fcd4", hovering_color="White")

    for button in [PLAY_AGAIN_BUTTON, QUIT_BUTTON]:
      button.changeColor(pygame.mouse.get_pos())
      button.update(win)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_AGAIN_BUTTON.checkForInput(pygame.mouse.get_pos()):
          select_sfx.play()
          end_game = False
          main()
        elif QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
          pygame.quit()

    pygame.display.update()    

def play():

  # game variables
  hangman_status = 0
  random_pair = random.choice(word_list)
  word = random_pair["word"].upper()
  hint = random_pair["hint"]
  guessed = []
  hint_flag = False

  # button variables
  RADIUS = 22
  GAP = 15
  letters = []
  startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
  starty = 400
  A = 65
  for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

  FPS = 60
  clock = pygame.time.Clock()
  run = True
  HINT_BUTTON = Button(image=pygame.image.load("smaller_Rect.png"), pos=(950, 80), text_input="HINT", font=LETTER_FONT, base_color="#d7fcd4", hovering_color="White")


  while run:
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        m_x, m_y = pygame.mouse.get_pos()
        for letter in letters:
          x, y, ltr, visible = letter
          if visible:
            dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
            if dis < RADIUS:
              letter[3] = False
              guessed.append(ltr)
              if ltr not in word:
                hangman_status += 1
        if HINT_BUTTON.checkForInput(pygame.mouse.get_pos()):
          if hint_flag == False:
            hint_open_sfx.play()

          hint_flag = not hint_flag

    win.fill(BG)

    HINT_BUTTON.changeColor(pygame.mouse.get_pos())
    HINT_BUTTON.update(win)
          
    draw_word(word, guessed)
    draw_letters_button(letters, RADIUS, hangman_status)

    if hint_flag:
      draw_hint(hint)

    pygame.display.flip()

    won = True
    for letter in word:
      if letter not in guessed:
        won = False
        break

    if won:
      winning_sfx.play()
      final("You WON!", "The word is " + word)
      break

    if hangman_status == 6:
      losing_sfx.play()
      final("You LOST!", "The word is " + word)
      break

def main():
  win.fill(BG)

  MENU_MOUSE_POS = pygame.mouse.get_pos()

  MENU_TEXT = TITLE_FONT.render("HANGMAN", True, "#b68f40")
  MENU_RECT = MENU_TEXT.get_rect(center=(600, 100))

  PLAY_BUTTON = Button(image=pygame.image.load("Rect.png"), pos=(600, 240), 
                      text_input="PLAY", font=WORD_FONT, base_color="#d7fcd4", hovering_color="White")
  QUIT_BUTTON = Button(image=pygame.image.load("Rect.png"), pos=(600, 400), 
                      text_input="QUIT", font=WORD_FONT, base_color="#d7fcd4", hovering_color="White")

  win.blit(MENU_TEXT, MENU_RECT)

  for button in [PLAY_BUTTON, QUIT_BUTTON]:
    button.changeColor(MENU_MOUSE_POS)
    button.update(win)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
        select_sfx.play()
        play()
      if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
        pygame.quit()

  pygame.display.update()


while True:
  main()

pygame.quit()
