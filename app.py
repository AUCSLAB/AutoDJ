import pygame
import os 
import tkinter as tk
from tkinter import filedialog
import random


#Directory selector
def select_directory(shuffle = False):
   #pygame has no directory selector, using tk instead to find wanted directory
    root = tk.Tk()
    root.withdraw()
    # Open directory
    selected_dir = filedialog.askdirectory()
    root.destroy()
    if not selected_dir:
        print("No directory selected.")
        return None
    try:
        directory_contents = os.listdir(selected_dir)
        songs = []
        for file in directory_contents:
           if file[-4:] in [".mp3",".wma",".ogg"]:
              songs.append(file)
        print("Selected Directory:", selected_dir)
        print("Directory Contents:", directory_contents)
        print("Songs in Directory:",songs)
        if shuffle:
           random.shuffle(songs)
        return songs, selected_dir
    except Exception as e:
        print(f"Error accessing directory contents: {e}")
        return None

songs_list = []
selected_dir = ''
print("Stored Directory Contents:", songs_list)

# pygame initilization
pygame.init()
pygame.mixer.init()

# create the screen
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
background = pygame.image.load('./images/BackGround.jpg')

# title and icon
pygame.display.set_caption('Music Player')
icon = pygame.image.load('./images/walf.jpg')
pygame.display.set_icon(icon)

# load button images and make them 200x200
play_img = pygame.image.load('./images/play.png').convert_alpha()
play_img = pygame.transform.smoothscale(play_img, (150, 150))
pause_img = pygame.image.load('./images/pause.png').convert_alpha()
pause_img = pygame.transform.smoothscale(pause_img, (150, 150))
next_img = pygame.image.load('./images/next.png').convert_alpha()
next_img = pygame.transform.smoothscale(next_img, (150, 150))
prev_img=pygame.image.load('./images/previous.jpg').convert_alpha()
prev_img=pygame.transform.smoothscale(prev_img,(150,150))
callsign_img = pygame.image.load('./images/callsign.png').convert_alpha()
callsign_img = pygame.transform.smoothscale(callsign_img, (150, 33))
X_img=pygame.image.load('./images/x.png').convert_alpha()
X_img = pygame.transform.smoothscale(X_img, (50, 50))
window_img=pygame.image.load('images/Window.png')
window_img=pygame.transform.smoothscale(window_img,(50,50))
max_img=pygame.image.load('images/max.png').convert_alpha()
max_img=pygame.transform.smoothscale(max_img,(100,50))
logo_img=pygame.image.load('./images/logo.png').convert_alpha()
logo_img=pygame.transform.smoothscale(logo_img, (800,200))
logo_rect=logo_img.get_rect(center=(screen.get_width() // 2,1/4*((screen.get_height()))-50))
logo1_img=pygame.image.load('./images/a_castlelogo_official.png').convert_alpha()
logo1_img=pygame.transform.smoothscale(logo1_img, (250,250))
logo1_rect=logo1_img.get_rect(center=((150,100)))
fdir_img = pygame.image.load('./images/fdir.png').convert_alpha()
fdir_img = pygame.transform.smoothscale(fdir_img, (70, 70))
shuffle_img = pygame.image.load('./images/shuffle.png').convert_alpha()
shuffle_img = pygame.transform.smoothscale(shuffle_img, (70, 70))
clickedshuffle_img = pygame.image.load('./images/pickedshuffle.png').convert_alpha()
clickedshuffle_img = pygame.transform.smoothscale(clickedshuffle_img, (70, 70))


class Node:
   def __init__(self, music):
      self.music = music
      self.next = None
      self.prev = None
class Playlist:
   def __init__(self):
      self.head=None
      self.current=None
   def insert(self, music):
      node=Node(music)
      if not self.head:
         self.head=node
         node.next=node
         node.prev=node
      else:
         tail=self.head.prev
         tail.next=node
         node.prev=tail
         node.next=self.head
         self.head.prev=node
      self.current=self.head
   def search (self, music):
      if not self.head:
         return False
      current=self.head
      while True:
         if current.music==music:
            return current
         current=current.next
         if current==self.head:
            break
      raise RuntimeError("Music not found in playlist")
   def play_next(self):
      if self.current is None:
         raise RuntimeError("No current song to play next.")
      self.current = self.current.next
      return self.current.music
   def play_prev(self):
      if not self.current:
         raise RuntimeError("No current song to play. The playlist might be empty.")
      self.current = self.current.prev
      return self.current.music

playlist=Playlist()
for i in songs_list:
   playlist.insert(i)
   
# play/pause button class
BUTTON_PRESSED = pygame.USEREVENT + 1
button_pressed = pygame.event.Event(BUTTON_PRESSED)
class PlayPauseButton:
   def __init__(self, play_image, pause_image):
      self.images = [play_image, pause_image]
      self.playing = 0
      self.image = self.images[self.playing]
      self.rect = self.image.get_rect()
      
      self.clicked = False

   def draw(self):
      self.rect.center = (screen.get_width() // 2, screen.get_height() - self.rect.height // 2 - 53)
      # get mouse position
      mouse_pos = pygame.mouse.get_pos()
      
      if self.rect.collidepoint(mouse_pos):
         if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
      if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
         pygame.event.post(button_pressed)
         self.clicked = False
         if self.playing:
            self.playing = 0
         else:
            self.playing = 1

      # update image
      self.image = self.images[self.playing]
      # draw button on screen
      screen.blit(self.image, (self.rect))
      
# callsign button class
CALLSIGN_BUTTON_PRESSED = pygame.USEREVENT + 3
callsign_button_pressed = pygame.event.Event(CALLSIGN_BUTTON_PRESSED)
class callsignButton():
   def __init__(self, image):
      self.image = image
      self.rect = self.image.get_rect()
      
      self.clicked = False
   
   def draw(self):
      self.rect.center = (screen.get_width() // 2, screen.get_height() - self.rect.height // 2 - 20)
      mouse_pos = pygame.mouse.get_pos()
      if self.rect.collidepoint(mouse_pos):
         if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
      if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
         pygame.event.post(callsign_button_pressed)
         self.clicked = False

      # draw button on screen
      screen.blit(self.image, (self.rect))

SHUFFLE_BUTTON_PRESSED = pygame.USEREVENT + 5
shuffle_button_pressed = pygame.event.Event(SHUFFLE_BUTTON_PRESSED)
class ShuffleUnshuffledButton:
   def __init__(self, unshuffled_img, shuffled_image):
      self.images = [unshuffled_img, shuffled_image]
      self.shuffle = 0
      self.image = self.images[self.shuffle]
      self.rect = self.image.get_rect()
      
      self.clicked = False

   def draw(self):
      self.rect.center = (screen.get_width() // 2-280, screen.get_height() -120)
      # get mouse position
      mouse_pos = pygame.mouse.get_pos()
      
      if self.rect.collidepoint(mouse_pos):
         if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
      if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
         pygame.event.post(shuffle_button_pressed)
         self.clicked = False
         if self.shuffle:
            self.shuffle = 0
         else:
            self.shuffle = 1

      # update image
      self.image = self.images[self.shuffle]
      # draw button on screen
      screen.blit(self.image, (self.rect))



class Button:
   def __init__(self,image):
      self.img=image
      self.rect=self.img.get_rect()
      self.click=False
   def draw(self):
      
      mouse_pos = pygame.mouse.get_pos()
      if self.rect.collidepoint(mouse_pos):
         if pygame.mouse.get_pressed()[0]:
            self.click=True
      screen.blit(self.img, (self.rect))

# create button instances
next_button = Button(next_img)
prev_button=Button(prev_img)
directory_button = Button(fdir_img)
button = PlayPauseButton(play_img, pause_img)
callsign_button = callsignButton(callsign_img)
shuffle_button = ShuffleUnshuffledButton(shuffle_img,clickedshuffle_img)
XButton= Button(X_img)
XButton.rect.center=(screen.get_width()-25, 0+25)
WindowButton= Button(window_img)
WindowButton.rect.center=(screen.get_width()-80, 0+25)
FullScreen=Button(max_img)
# song handling
SONG_END = pygame.USEREVENT + 2
pygame.mixer.music.set_endevent(SONG_END)

def play_song():
   song = os.path.join(curr_directory, playlist.current.music)
   print(song)
   pygame.mixer.music.load(song)
   pygame.mixer.music.play()
def play_next_song(callsign_interrupt=False):
   #Plays the next song in the playlist.
   if playlist.head:
      if callsign_interrupt == False:
         next_song = playlist.play_next()
         print(f'Currently playing {next_song}')
         song = os.path.join(curr_directory, next_song)
         pygame.mixer.music.load(song)
         pygame.mixer.music.play()
         print('next')
      else:
         callsign = './callsign/WALF-Callsign.mp3'
         print(f'Currently running {callsign}')
         pygame.mixer.music.load(callsign)
         pygame.mixer.music.play()
         callsign_interrupt = False
   else:
       print("Playlist is empty. Cannot move to the next song.")

def play_previous_song():
   #Plays the previous song in the playlist.
   if playlist.head:
       next_song = playlist.play_prev()
       print(f'Currently playing {next_song}')
       song = os.path.join(curr_directory, next_song)
       pygame.mixer.music.load(song)
       pygame.mixer.music.play() 
       print('prev')
   else:
       print("Playlist is empty. Cannot move to the next song.")

# Initialize the music player
if songs_list == []:
   pass
else:
   play_song()
   pygame.mixer.music.pause()

#Initiate variables
running = True
playing = False
callsign_played = False
pause_time = 0
skip = True
Windowed=False
x=0
y=0
start_time=pygame.time.get_ticks()
nxt=False
prev=False
my_font = pygame.font.SysFont('Comic Sans MS', screen.get_height()//36)

shuffle = False
call_sign_interrupt = False
while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT or XButton.click==True:
         running = False
      if directory_button.click:
            found_list = select_directory(shuffle)
            if found_list == None or len(found_list[0]) == 0:
               pass
            else:
               ordered_songs = found_list[0]
               songs_list = found_list[0]
               curr_directory = found_list[1]
               playlist=Playlist()
               for i in songs_list:
                  playlist.insert(i)
               #Initialize first song
               play_song()
               pygame.mixer.music.pause()
            directory_button.click = False
      if event.type == SONG_END or next_button.click or prev_button.click or callsign_played:
         if prev_button.click:
            prev_button.click=False
            #button.clicked=True
            button.playing=1
            playing=True
            prev=True
         if next_button.click:
            next_button.click=False
            #button.clicked=True
            button.playing=1
            playing=True
      
         if callsign_played: # callsign was manually played
            call_sign_interrupt=True
            callsign_played=False
            start_time=pygame.time.get_ticks()
         elif (pygame.time.get_ticks()-start_time)/(60*1000)>20:
            start_time=pygame.time.get_ticks()
            call_sign_interrupt=True
         else: # play next song after a song ends
            print('-- playing next song --')
            
            if call_sign_interrupt:
               call_sign_interrupt=False
               print('-- playing callsign --')
               play_next_song(callsign_interrupt=True)
            elif not prev:
               play_next_song()
            else:
               prev=False
               play_previous_song()
      elif event.type == BUTTON_PRESSED: # play/pause button
         if playing:
            pygame.mixer.music.pause()
            playing = False
         else:
            pygame.mixer.music.unpause()
            playing = True
      elif event.type == CALLSIGN_BUTTON_PRESSED: # callsign button pressed

         callsign_played = True

      elif event.type == SHUFFLE_BUTTON_PRESSED:
         if not shuffle:
            shuffle = True
         else:
            shuffle = False

         if shuffle:
            songs_list = random.shuffle(songs_list)
            playlist=Playlist()
            for i in songs_list:
               playlist.insert(i)
            #Initialize first song
            play_song()
            pygame.mixer.music.pause()
         else:
            pass
            curr_Song = playlist.current.music
            songs_list = ordered_songs
            playlist=Playlist()
            for i in songs_list:
               playlist.insert(i)
            #Initialize first song
            playlist.search(curr_Song)##WORK IN PROGRESS
            pygame.mixer.music.pause()

      
      elif WindowButton.click==True:
         screen = pygame.display.set_mode((900,600), pygame.RESIZABLE)         
         logo1_img=pygame.transform.smoothscale(logo1_img, (400,200))
         WindowButton.click=False
         Windowed=True
            
      elif FullScreen.click==True:
         screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)         
         logo1_img=pygame.transform.smoothscale(logo1_img, (500,250))
         FullScreen.click=False
         Windowed=False
         FullScreen.draw()
   
   background = pygame.transform.scale(background, screen.get_size())
   screen.blit(background,(0,0))  
  
   callsign_button.draw()
   button.draw()
   shuffle_button.draw()
   next_button.rect.center = (screen.get_width() // 2+150, screen.get_height() - next_button.rect.height // 2 - 53)
   next_button.draw()
   prev_button.rect.center = (screen.get_width() // 2-150, screen.get_height() - prev_button.rect.height // 2 - 53)
   prev_button.draw()
   directory_button.rect.center = (50, screen.get_height() - prev_button.rect.height // 2 )
   directory_button.draw()
      
   if Windowed:
      FullScreen.rect.center=(screen.get_width()-35, 0+25)
      FullScreen.draw()
      
      if screen.get_width()>831:
         screen.blit(logo1_img,(screen.get_width()-300,screen.get_height()-180))
   else:
      XButton.draw()
      screen.blit(logo_img,(logo_rect))
      screen.blit(logo1_img,(logo1_rect))

      WindowButton.draw()
   if len(songs_list) == 1:
      text = my_font.render(playlist.current.music[:-4], False, (255,255,255))
      screen.blit(text, (screen.get_width() // 2-160,screen.get_height() - 230))
   elif len(songs_list) > 1:
      text = my_font.render(playlist.current.music[:-4], False, (255,255,255))
      textprev = my_font.render(playlist.current.prev.music[:-4], False, (255,255,255))
      textnext = my_font.render(playlist.current.next.music[:-4], False, (255,255,255))
      nextsongtext = my_font.render("Next Song: ", False, (255,255,255))
      prevsongtext = my_font.render("Previous Song: ", False, (255,255,255))
      currsongtext = my_font.render("Current Song: ", False, (255,255,255))
      screen.blit(text, (screen.get_width() // 2-140,screen.get_height() - 230))
      screen.blit(currsongtext, (screen.get_width() // 2 - 60,screen.get_height() - 260))
      screen.blit(prevsongtext, (screen.get_width() // 2+250, screen.get_height() - prev_button.rect.height // 2 - 100))
      screen.blit(textprev, (screen.get_width() // 2 +410, screen.get_height() - prev_button.rect.height // 2 -100))
      screen.blit(nextsongtext, (screen.get_width() // 2+250, screen.get_height() - prev_button.rect.height // 2 - 70))
      screen.blit(textnext, (screen.get_width() // 2 +370, screen.get_height() - prev_button.rect.height // 2 - 70))
   
   pygame.display.update()

pygame.quit()
