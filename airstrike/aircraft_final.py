from pygame import*
from random import randint

# we need these pictures:
img_back = "sky.jpg" 
img_back2 = "sky2.jpg"
img_hero = "plane.png" # character
img_jet = "jet.png" #enemy
img_bullet = "bullet.png" #bullet
img_bullet1 = "bullet1.png" #boss bullet
img_bird = "bird.png" #meteorite
img_boss = "boss.png"

#fonts
font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 50)

score = 0 #ships hit
dodged = 0 #ships missed
max_dodged = 10 #lost after missed 10
goal = 5 # win after killing this amount
bullet_count = 5 #initial bullet count
player_health = 10 #the amount of lives player has (functions only with bird and boss collision)
boss_health = 15 #amount of lives the boss has


#parent for other sprites
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Bullet(GameSprite):
    #enemys movement
    def update(self):
        self.rect.y += self.speed
        #dissapears if it reacehs the edge
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        global bullet_count
        if bullet_count > 0:
            bullet_count -= 1
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20, 45, -30)   
            bullets.add(bullet)

class Bird(GameSprite):
    # meteorite movement
    def update(self):
        self.rect.y += self.speed
        global lost
        #disappears if passes the edge
        if self.rect.y > win_height:
            self.rect.x = randint(50, win_width - 50)
            self.rect.y = 0

# enemy sprite class        
class Enemy(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y += self.speed
        global dodged
        #disappears if passes the edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            dodged = dodged + 1

class Boss(GameSprite):
    def update(self):
        if plane.rect.x-self.rect.x>10:
            self.rect.x += self.speed
        elif plane.rect.x- self.rect.x<10:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet(img_bullet1, self.rect.centerx, self.rect.bottom, 20, 45, 30)
        bossBullets.add(bullet)


#The window
win_width = 1020
win_height = 800
display.set_caption("air strike")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



# creating the sprites
plane = Player(img_hero, 5, win_height - 100, 80, 100, 10)

jets = sprite.Group()
for i in range(5):
    jet = Enemy(img_jet, randint(80, win_width - 80), -90, 95, 70, randint(1, 10))
    jets.add(jet)

bullets = sprite.Group()
bossBullets = sprite.Group()

birds = sprite.Group()
for i in range(4):
    bird = Bird(img_bird, randint(80, win_width - 80), -60, 70, 65, randint(1, 7))
    birds.add(bird)

finalBoss = Boss(img_boss, randint(80, win_width - 80), 60, 160, 100, 2)


i = 1
bossHidden = True
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                plane.fire()

    if not finish:
        window.blit(background, (0, 0))

        #writings on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_dodged = font2.render("Dodged: " + str(dodged), 1, (255, 255, 255))
        window.blit(text_dodged, (10, 50))

        text_bird = font1.render("YOU LOST", 1, (238,173,14))

        text_lost = font1.render("GAME OVER", 1, (238,173,14))

        text_win = font1.render("YOU WIN", 1, (105,89,205))
        
        text_ammo = font2.render("Bullets: " + str(bullet_count), 1, (255, 255, 255))
        window.blit(text_ammo, (10, 80))
        
        text_health = font2.render("Lives: " + str(player_health), 1, (255, 255, 255)) 
        window.blit(text_health, (10, 110))

        

        #sprite movements
        plane.update()
        jets.update()
        bullets.update()
        birds.update()

        #updating them at a new location 
        plane.reset()
        jets.draw(window)
        bullets.draw(window)
        birds.draw(window)

        
        #collision check (jet - bullet)
        collides = sprite.groupcollide(jets, bullets, True, True)
        for c in collides:
            score = score + 1
            jet = Enemy(img_jet, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            jets.add(jet)

            bullet_count = bullet_count + 1
            bullets.add(bullets)

        if sprite.spritecollide(plane, jets, False) or dodged >= max_dodged:
             finish = True
             window.blit(text_lost, (345, 240))

        if sprite.spritecollide(plane, birds, True):
            # finish = True
            # window.blit(text_lost, (425, 240))
             player_health -= 1
             
        if dodged == 10:
            bullet_count = bullet_count + 1
            bullets.add(bullets)
            
        if sprite.spritecollide(plane, bossBullets, True):
            player_health -= 1

        if sprite.spritecollide(finalBoss, bullets, True):
            boss_health -= 1
            bullet_count = bullet_count + 1
            bullets.add(bullets)


        if score >= goal and bossHidden:
            finalBoss = Boss(img_boss, randint(80, win_width - 80), 60, 160, 100, 2)
            bossHidden = False            
            for jet in jets:
                jet.kill()
            
            # finish = True
            # window.blit(text_win, (345, 240))                

        if not bossHidden:
            finalBoss.update()
            finalBoss.reset()
            if i%20==0:
                finalBoss.fire()
            i+=1
            bossBullets.update()
            bossBullets.draw(window)

        if player_health == 0:
            finish = True
            window.blit(text_bird, (330,230))

        if boss_health ==0:
            finish = True
            window.blit(text_win, (360,250))

        display.update()

    time.delay(30)

    
