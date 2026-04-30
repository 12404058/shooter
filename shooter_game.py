from pygame import *
from random import randint
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y,size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()#прямоугольник
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bull = Bullet('bullet.png',15,self.rect.centerx,self.rect.top,15,20)
        bullets.add(bull)

lost = 0

class Asteroid(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y > 500:
            self.rect.y = -80
            self.rect.x = randint(5,615)
            self.speed = randint(1,3)

class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -80
            self.rect.x = randint(5,615)
            lost += 1
            self.speed = randint(1,3)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()#удоляем спрайт


mixer.init()
'''mixer.music.load('space.ogg')
mixer.music.play()'''
fire_sound = mixer.Sound('fire.ogg')
font1 = font.SysFont('Arial',36)

text_lose = font1.render('Пропущено:' + str(lost),1,(255,255,255))



window = display.set_mode((700,500))
display.set_caption('shooter')

background = transform.scale(image.load('galaxy.jpg'),(700,500))



clock = time.Clock()        #отслеживает частоту кадров в секунду
FPS = 60                    #кадры в секунду

pl = Player('rocket.png',10,350,415,65,80)

run = True
finish = False
lost = 0
score = 0 #убито

num_fire = 0
rel_time = False

text_rel = font1.render('Перезарядка...',1,(0,255,255))
text_win = font1.render('Победа!',1,(0,255,0))
text_lose = font1.render('Поражение!',1,(255,0,0))


life = 3

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid('asteroid.png',randint(3,4),randint(5,615),-80,80,50)
    asteroids.add(asteroid)

monsters = sprite.Group()#создаем группу
for i in range(3):
    monster = Enemy('ufo.png',randint(1,2),randint(5,615),-80,80,50)
    monsters.add(monster)

while run == True:
    for event1 in event.get(): #перебераем очередь событий
        if event1.type == QUIT: #проверка на закрытие окна
            run = False
        elif event1.type == KEYDOWN:
            if event1.key == K_UP:
                if num_fire <= 5 and rel_time == False:
                    num_fire += 1
                    #fire_sound.play()
                    pl.fire()
                elif num_fire >= 5 and rel_time == False:
                    last_time = time.get_ticks()
                    rel_time = True
            

    if finish == False:
        window.blit(background,(0,0))
        pl.reset()
        pl.update()
        asteroids.draw(window)
        asteroids.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        collides = sprite.groupcollide(monsters,bullets,True,True)#получаем список монстров, которые столкнулись с пулей,а затем удаляем из группы
        collides1 = sprite.groupcollide(asteroids,bullets,False,True)

        list1 = sprite.spritecollide(pl,monsters,True)
        for i in list1:
            life -= 1
            monster = Enemy('ufo.png',randint(1,2),randint(5,615),-80,80,50)
            monsters.add(monster)

        list2 = sprite.spritecollide(pl,asteroids,True)
        for i in list2:
            life -= 1
            asteroid = Enemy('asteroid.png',randint(3,4),randint(5,615),-80,80,50)
            asteroids.add(asteroid)


        for c in collides:
            score += 1
            monster = Enemy('ufo.png',randint(1,2),randint(5,615),-80,80,50)
            monsters.add(monster)

        '''for a in collides1:
            score += 1
            asteroid = Enemy('asteroid.png',randint(3,4),randint(5,615),-80,80,50)
            asteroids.add(asteroid)'''

        if score >= 8:
            finish = True
            window.blit(text_win,(300,250))

        if  lost >=3  or life <= 0:
            finish = True
            window.blit(text_lose,(300,250))

        if rel_time == True:
            new_time = time.get_ticks()
            if new_time - last_time < 1000 :
                window.blit(text_rel,(300,450))
                pass
            else:
                num_fire = 0
                rel_time = False
                
                


        text_life = font1.render('Жизни:' + str(life),1,(255,255,255))
        window.blit(text_life,(5,90))
        text_miss = font1.render('Пропущено:' + str(lost),1,(255,255,255))
        window.blit(text_miss,(5,10))
        text_score = font1.render('Убито:' + str(score),1,(255,255,255))
        window.blit(text_score,(5,50))

    display.update()
    clock.tick(FPS)

    #none
