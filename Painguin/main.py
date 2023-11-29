import pygame
import sys
import math
import random
import os

pygame.init()
#ใส่รูปพื้นหลัง
bg = pygame.image.load("img/bg4.png")
bg_menu = pygame.image.load("img/bg2.png")
bg = pygame.transform.scale(bg,(2200,1800))
bg_menu = pygame.transform.scale(bg_menu,(800,600))
#กำหนดขนาดหน้าจอเเละรูปภาพ
display = pygame.display.set_mode((800, 600))
start_img = pygame.image.load('img/Start.png').convert_alpha()
clock = pygame.time.Clock()
pygame.display.set_caption("PAINguin Shoot")
#ใส่เสียงต่างๆ
shotmix = pygame.mixer.Sound("mix\shot.wav")
pick = pygame.mixer.Sound("mix/take.wav")
die = pygame.mixer.Sound("mix/die.wav")
s_button = pygame.mixer.Sound("mix/bt.wav")
#ใส่เพลงเกม
sound = pygame.mixer.music.load("mix\play.mp3")

#ใส่font
PAINguinfont = pygame.font.Font("font\penguin.ttf",25)
Titlefont = pygame.font.Font("font/penguin.ttf",25)
Textgame = pygame.font.Font("font\sss.ttf",60)
Textgame1 = pygame.font.Font("font\ThaleahFat.ttf",40)
Textgame2 = pygame.font.Font("font\ThaleahFat.ttf",60)
#ใส่รูปผู้เล่น
player_walk_images = [(pygame.image.load("img/player_walk_0.png")),pygame.transform.scale(pygame.image.load("img/player_walk_1.png"),(200,200)),
pygame.image.load("img/player_walk_2.png"), pygame.image.load("img/player_walk_3.png")]
player_weapon = pygame.transform.scale(pygame.image.load("img/shotgun.png"),(25,20)).convert()
player_weapon.set_colorkey((255,255,255))
#เพลง
pygame.mixer.music.play(-1)
#คลาสผู้เล่น
class Player:
    def __init__(self, x, y, width, height,hp):
        self.hp = hp 
        self.x = x
        self.y = y
        
        self.moveX = 0
        self.moveY = 0
        
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
        #อนิเมชั่นการถือปืน
    def handle_weapons(self, display):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x, rel_y = mouse_x - player.x, mouse_y - player.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        player_weapon_copy = pygame.transform.rotate(player_weapon, angle)

        display.blit(player_weapon_copy, (self.x+15-int(player_weapon_copy.get_width()/2), self.y+25-int(player_weapon_copy.get_height()/2)))

        #อนิเมชั่นการเดินของผู้เล่น
    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0

        self.animation_count += 1

        if self.moving_right:
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (50, 50)), (self.x, self.y))
        elif self.moving_left:
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (50, 50)), (self.x, self.y))
        else:
            display.blit(pygame.transform.scale(player_walk_images[0], (50, 50)), (self.x, self.y))

        self.handle_weapons(display)

        self.moving_right = False
        self.moving_left = False
#คลาสกระสุนพิเศษ     
class SuperBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lastX = x
        self.lastY = y
        
        self.animation_images = pygame.image.load("img/super_bullet.png")
        
    def show(self, display,x,y):
        changeX = x
        changeY = y
        if self.x == self.lastX:
            changeX = 0
        if self.y == self.lastY:
            changeY = 0
            
            
        display.blit(self.animation_images,(self.x-changeX, self.y-changeY))
            
        self.lastX = x
        self.lastY = y
#คลาสกระสุนชนิดที่1    
class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0,0,0), (self.x+16, self.y+16), 5)

#คลาสกระสุนชนิดที่2        
class PlayerBullet2:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0,0,0), (self.x+28, self.y+28), 5)
        pygame.draw.circle(display, (0,0,0), (self.x+5, self.y+5), 5)
#คลาสปุ่ม
class Button:
    def __init__(self,position_x,position_y,img,scale):
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img,(int(width * scale),int(height * scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft = (position_x ,position_y)
        self.clicked = False
    def ButtonDraw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.img, (self.rect.x,self.rect.y))
        return action
#คลาสศัตรู
class SlimeEnemy:
    def __init__(self, x, y,hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.animation_images = [(pygame.image.load("img/slime_animation_0.png")), pygame.image.load("img/slime_animation_1.png"),
        pygame.image.load("img/slime_animation_2.png"), pygame.image.load("img/slime_animation_3.png")]
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        #อนิเมชั่นการเดินของสไลม์
    def main(self, display):
        
        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1
        if self.reset_offset == 0:
            self.offset_x = random.randrange(-200, 200)
            self.offset_y = random.randrange(-200, 200)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1
            

        if player.x + self.offset_x > self.x-display_scroll[0]: #ขึ้น
            if self.offset_x > 100:
                self.x += 2
        elif player.x + self.offset_x < self.x-display_scroll[0]: #ลง
                self.x -= 2

        if player.y + self.offset_y > self.y-display_scroll[1]:
            self.y += 2
        elif player.y + self.offset_y < self.y-display_scroll[1]:
            self.y -= 2

        display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (45, 45)), (self.x-display_scroll[0], self.y-display_scroll[1]))
#ฟังชั่นเล่นเกม
def playing():
    playerTypeBullet = 1
    Hightscore = 0
    amountShoot = 0
    check = False
    #ตัวแปลเก็บ hight score
    hight_score1 = 0
    if os.path.exists("score.txt"):
        with open("score.txt","r") as file :
            hight_score1 = int(file.read())
#หน้าdisplayในเกม
    while True:
        
        Score = str(Hightscore)
        ShowHight = PAINguinfont.render("Hight Score",True,(255,255,255))
        ShowScore = PAINguinfont.render(Score,True,(255,255,255))
        textAmmo = Textgame2.render("Twin Ammo : ",True,(255,255,255))
        ShowAmmo = Textgame.render(str((amountShoot* -1)),True,(255,255,255))
        
        display.fill((0,0,0))
        display.blit(bg,(-400-display_scroll[0], -300-display_scroll[1]))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        #ส่วนของการสร้างสไลม์เมื่อสไลม์ตายหมด
        if len(enemies)==0:
            for i in range(0,12):
                ranx = random.randint(300,600)
                rany = random.randint(200,500)
                enemies.append(SlimeEnemy(ranx, rany,2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shotmix.play()
                    
                    '''เปลี่ยนกระสุน'''
                    
                    if(amountShoot > -1):
                        playerTypeBullet = 1
                        amountShoot = 0
                        
                    if(playerTypeBullet == 1):
                        player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))
                    elif(playerTypeBullet == 2):
                        amountShoot += 1
                        player_bullets2.append(PlayerBullet2(player.x, player.y, mouse_x, mouse_y))
        keys = pygame.key.get_pressed()


    #ส่วนกำหนดปุ่มการเดินของผู้เล่น
        if keys[pygame.K_a] and display_scroll[0] > -350 :
            display_scroll[0] -= 5
            
            player.moveX -= 5
            
            player.moving_left = True

            for bullet in player_bullets:
                bullet.x += 5
            for bullet2 in player_bullets2:
                bullet2.x += 5
        if keys[pygame.K_d] and display_scroll[0] < 500:
            display_scroll[0] += 5

            player.moveX += 5
            
            player.moving_right = True

            for bullet in player_bullets:
                bullet.x -= 5
            for bullet2 in player_bullets2:
                bullet2.x -= 5
        if keys[pygame.K_w] and display_scroll[1] > -250 :
            display_scroll[1] -= 5
            
            player.moveY -= 5

            for bullet in player_bullets:
                bullet.y += 5
            for bullet2 in player_bullets2:
                bullet2.y += 5
        if keys[pygame.K_s] and display_scroll[1] < 550:
            display_scroll[1] += 5
            
            player.moveY += 5

            for bullet in player_bullets:
                bullet.y -= 5
            for bullet2 in player_bullets2:
                bullet2.y -= 5

        player.main(display)
        #ส่วน hit box แบบ overlab สไลม์ชนผู้เล่น
        for  enemy in enemies:
            if enemy.y- display_scroll[1] >= player.y - 17 and enemy.y- display_scroll[1] <= player.y+ 17 and enemy.x- display_scroll[0] >= player.x- 17 and enemy.x- display_scroll[0] <= player.x + 17:
                    check =  True
                    if Hightscore > hight_score1:
                        hight_score1 = Hightscore
                        with open("score.txt","w") as file:
                            file.write(str(hight_score1))
                    break
            else:
                    check = False
        if check:
            die.play()
            break
          #ส่วน hit box แบบ overlab สไลม์ชนกระสุนชนิดที่1  
        for bullet in player_bullets:
            for enemy in enemies:
                if bullet.y >= enemy.y- display_scroll[1] - 17 and bullet.y <= enemy.y - display_scroll[1]+ 17 and bullet.x >= enemy.x - display_scroll[0]- 17 and bullet.x <= enemy.x - display_scroll[0]+ 17:
                    enemy.hp -= 1
                    if enemy.hp == 0:
                        rand_item =random.choice([0,0,0,0,0,0,0,1])
                        if rand_item == 1:
                            super_bullet = SuperBullet(enemy.x,enemy.y)
                            itemsDrop.append(super_bullet)
                            
                    
                    try:
                        player_bullets.pop(player_bullets.index(bullet))
                    except:
                        pass
                    if enemy.hp <= 0:
                        if random.random() < 10*0.01:
                            newDrop = SuperBullet(enemy.x- display_scroll[1], enemy.y- display_scroll[1])
                            
                            itemsDrop.append(newDrop)
                            
                        enemies.pop(enemies.index(enemy))
                        Hightscore +=1
                        
            #ส่วน hit box แบบ overlab สไลม์ชนกระสุนชนิดที่2              
        for bullet2 in player_bullets2:
            for enemy in enemies:
                if bullet2.y >= enemy.y- display_scroll[1] - 22 and bullet2.y <= enemy.y - display_scroll[1]+ 22 and bullet2.x >= enemy.x - display_scroll[0]- 22 and bullet2.x <= enemy.x - display_scroll[0]+ 22:
                    enemy.hp -= 2
                    
                    try:
                        player_bullets2.pop(player_bullets2.index(bullet))
                    except:
                        pass
                    if enemy.hp <= 0:
                        if random.random() < 10*0.01:
                            newDrop = SuperBullet(enemy.x- display_scroll[1], enemy.y- display_scroll[1])
                            
                            itemsDrop.append(newDrop)
                            
                        enemies.pop(enemies.index(enemy))
                        Hightscore +=1
            #ส่วน ดรอปกระสุนพิเศษ        
        for item in itemsDrop:
            item.show(display,display_scroll[0], display_scroll[1])
            if item.y- display_scroll[1] >= player.y - 23 and item.y- display_scroll[1] <= player.y+ 23 and item.x- display_scroll[0] >= player.x- 20 and item.x- display_scroll[0] <= player.x + 20:
                try:
                    itemsDrop.pop(itemsDrop.index(item))
                    amountShoot -= 5
                    playerTypeBullet = 2
                    pick.play()
                except:
                    pass

            
        for bullet in player_bullets:
            bullet.main(display)

        for bullet2 in player_bullets2:
            bullet2.main(display)
            
        for enemy in enemies:
            enemy.main(display)

        display.blit(ShowScore,(40,20))
        display.blit(ShowAmmo,(800 - 70,20))
        display.blit(textAmmo,(800 - 350,30))
        clock.tick(60)
        pygame.display.update()
        
start_button = Button(230, 300, start_img, 1)
#หน้าเมนู
while True:
    if os.path.exists("score.txt"):
        with open("score.txt","r") as file :
            hight_score = int(file.read())
    else:
        hight_score = 0
    Show_Score = Textgame2.render(str(hight_score),True,(255,255,255))
    title= Titlefont.render("PAINguin",True,(255,255,255))
    text_score = Textgame2.render("Hight Score : ",True,(255,255,255))
    name = Textgame1.render("Kotcharat Puttated ",True,(255,255,255))
    no = Textgame1.render("No. 64015018 ",True,(255,255,255))
    enemies = [SlimeEnemy(400, 300,2)]
    player = Player(500, 250, 60, 60,10)
    supx = random.randint(350,670)
    supy  = random.randint(250,500)
    display_scroll = [0,0]
    player_bullets = []
    player_bullets2 = []
    itemsDrop = []
    clock = pygame.time.Clock()
    display.blit(bg_menu,(0, 0))
    display.blit(Show_Score,(550,450))
    display.blit(title,(150,50))
    display.blit(text_score,(200,450))
    display.blit(name,(30,540))
    display.blit(no,(500,540))
    #Titlefont 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
            break
        #bt
    if start_button.ButtonDraw(display):
        s_button.play()
        playing()
    pygame.display.update()
pygame.quit()
#6คลาส