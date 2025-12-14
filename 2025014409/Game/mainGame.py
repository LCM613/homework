#조작법: 방향키(이동) 스페이스(발사)

from tkinter import *
import time
import random


class mainGame():
    def __init__(self):
        self.window = Tk()
        self.window.title("Shooting Game")
        self.window.geometry("600x900")

        self.canvas = Canvas(self.window, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)

        self.startTime = time.time()

        self.stage1Image = PhotoImage(file="../image/bg1.png").zoom(2)
        self.stage1Bg = self.canvas.create_image(0, 0, image=self.stage1Image)

        self.score = 0
        self.scoreText = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill="yellow", font=("Arial", 20))

        self.heroImage = PhotoImage(file="../image/hero.png").subsample(3)
        self.hero = self.canvas.create_image(300, 450, anchor="center", image=self.heroImage)

        self.heroBulletImage = PhotoImage(file="../image/fire.png")
        self.bullets = []

        self.bulletCooltime = 0.5
        self.lastFiretime = 0
        self.bossBulletCooltime = 0.4
        self.lastBossFiretime = 0

        self.enemyImage = PhotoImage(file="../image/enemy.png").subsample(3)
        self.enemys = []

        self.enemyDelay = 0.5
        self.lastEnemy = 0

        self.bossImage = PhotoImage(file="../image/boss.png")
        self.bossBulletImage = PhotoImage(file="../image/fire2.png")
        self.bossState = "none"
        self.bossBullets = []
        self.bossHP = 30

        self.keys = set()
        self.window.bind("<KeyPress>", self.keyPress)
        self.window.bind("<KeyRelease>", self.keyRelease)
        
        self.gameLoop()
        self.window.mainloop()

    def keyPress(self, event):
        self.keys.add(event.keysym)

    def keyRelease(self, event):
        self.keys.discard(event.keysym)

    def heroMove(self):
        heroX, heroY = self.canvas.coords(self.hero)
        if "Left" in self.keys and heroX > 0:
            self.canvas.move(self.hero, -3, 0)
        if "Right" in self.keys and heroX < 600:
            self.canvas.move(self.hero, 3, 0)
        if "Up" in self.keys and heroY > 10:
            self.canvas.move(self.hero, 0, -3)
        if "Down" in self.keys and heroY < 750:
            self.canvas.move(self.hero, 0, 3)
        if "space" in self.keys:
            self.shoot()

    def shoot(self):
        now = time.time()

        if now - self.lastFiretime < self.bulletCooltime:
            return

        self.lastFiretime = now

        heroX, heroY = self.canvas.coords(self.hero)
        bullet = self.canvas.create_image(heroX, heroY - 40, image=self.heroBulletImage)
        self.bullets.append(bullet)

    def bulletMove(self):
        for _ in self.bullets[:]:
            self.canvas.move(_, 0, -6)

            heroBulletX, heroBulletY = self.canvas.coords(_)
            if heroBulletY < 10:
                self.canvas.delete(_)
                self.bullets.remove(_)

    def enemyControl(self):
        now = time.time()

        if now - self.startTime > 60 and self.bossState == "none":
            self.bossCome = self.canvas.create_image(300, -10, anchor="center", image=self.bossImage)
            self.bossState = "entering"

            return

        if hasattr(self, "boss") or self.bossState == "entering":
            return
        
        if now - self.lastEnemy < self.enemyDelay:
            return

        self.lastEnemy = now

        enemyX = random.randint(30, 570)
        enemy = self.canvas.create_image(enemyX, -10, image=self.enemyImage)
        self.enemys.append(enemy)

    def enemyMove(self):
        self.enemyControl()
        for _ in self.enemys[:]:
            self.canvas.move(_, 0, 3)

            enemyX, emenyY = self.canvas.coords(_)
            if emenyY > 900:
                self.canvas.delete(_)
                self.enemys.remove(_)

    def heroAttack(self):
        for _ in self.bullets[:]:
            heroBulletBbox = self.canvas.bbox(_)
            
            if not heroBulletBbox:
                continue

            heroBulletX1, heroBulletY1, heroBulletX2, heroBulletY2 = heroBulletBbox

            for e in self.enemys[:]:
                enemyBbox = self.canvas.bbox(e)

                if not enemyBbox:
                    continue

                enemyX1, enemyY1, enemyX2, enemyY2 = enemyBbox

                if not (heroBulletX2 < enemyX1 or heroBulletX1 > enemyX2 or heroBulletY2 < enemyY1 or heroBulletY1 > enemyY2):
                    self.canvas.delete(_)
                    self.canvas.delete(e)

                    self.bullets.remove(_)
                    self.enemys.remove(e)

                    self.score += 100
                    self.canvas.itemconfigure(self.scoreText, text=f"Score: {self.score}")

                    return

    def heroDemage(self):
        heroBbox = self.canvas.bbox(self.hero)

        if not heroBbox:
            return

        heroX1, heroY1, heroX2, heroY2 = heroBbox

        if hasattr(self, "boss"):
            bossBbox = self.canvas.bbox(self.boss)
            bossX1, bossY1, bossX2, bossY2 = bossBbox
            if not (heroX2 < bossX1 or heroX1 > bossX2 or heroY2 < bossY1 or heroY1 > bossY2):
                self.canvas.delete(self.hero)
                self.canvas.delete(self.boss)

                self.canvas.create_text(300, 350, text="GAME OVER", fill="red", font=("Arial", 50))

                return

            for _ in self.bossBullets[:]:
                bossBulletBbox = self.canvas.bbox(_)
            
                if not bossBulletBbox:
                    continue

                bossBulletX1, bossBulletY1, bossBulletX2, bossBulletY2 = bossBulletBbox

                heroBbox = self.canvas.bbox(self.hero)


                heroX1, heroY1, heroX2, heroY2 = heroBbox

                if not (bossBulletX2 < heroX1 or bossBulletX1 > heroX2 or bossBulletY2 < heroY1 or bossBulletY1 > heroY2):
                    self.canvas.delete(_)
                    self.canvas.delete(self.hero)

                    self.bossBullets.remove(_)
                    self.canvas.create_text(300, 350, text="GAME OVER", fill="red", font=("Arial", 50))

                    return

            pass

        for e in self.enemys[:]:
            enemyBbox = self.canvas.bbox(e)

            if not enemyBbox:
                continue

            enemyX1, enemyY1, enemyX2, enemyY2 = enemyBbox

            if not (heroX2 < enemyX1 or heroX1 > enemyX2 or heroY2 < enemyY1 or heroY1 > enemyY2):
                self.canvas.delete(self.hero)
                self.canvas.delete(e)

                self.enemys.remove(e)

                self.canvas.create_text(300, 350, text="GAME OVER", fill="red", font=("Arial", 50))

                return

    def bossEnter(self):
        if self.bossState != "entering":
            return

        self.canvas.move(self.bossCome, 0, 3)
        x, y = self.canvas.coords(self.bossCome)

        if y >= 100:
            self.canvas.delete(self.bossCome)
            self.boss = self.canvas.create_image(300, 100, anchor="center",image=self.bossImage)
            self.bossState = "done"

    def bossControl(self):

        if not hasattr(self, "boss"):
            return

        now = time.time()

        if now - self.lastBossFiretime < self.bossBulletCooltime:
            return

        self.lastBossFiretime = now

        bossX, bossY = self.canvas.coords(self.boss)
        randX = random.randint(-200, 200)
        bullet = self.canvas.create_image(bossX + randX, bossY + 50, image=self.bossBulletImage)
        self.bossBullets.append(bullet)

    def bossBulletMove(self):
        for _ in self.bossBullets[:]:
            self.canvas.move(_, 0, 7)

            bossBulletX, bossBulletY = self.canvas.coords(_)
            if bossBulletY > 900:
                self.canvas.delete(_)
                self.bossBullets.remove(_)

    def bossDemage(self):
        now = time.time()

        if not hasattr(self, "boss"):
            return

        for _ in self.bullets[:]:
            heroBulletBbox = self.canvas.bbox(_)
            
            if not heroBulletBbox:
                continue

            heroBulletX1, heroBulletY1, heroBulletX2, heroBulletY2 = heroBulletBbox

            bossBbox = self.canvas.bbox(self.boss)


            bossX1, bossY1, bossX2, bossY2 = bossBbox

            if not (heroBulletX2 < bossX1 or heroBulletX1 > bossX2 or heroBulletY2 < bossY1 or heroBulletY1 > bossY2):
                self.canvas.delete(_)
                self.bullets.remove(_)
                self.bossHP -= 1

                if self.bossHP <= 0:
                    self.canvas.delete(self.boss)
                    if 60 < now - self.startTime <= 120:
                        self.score += 50000
                        self.canvas.itemconfigure(self.scoreText, text=f"Score: {self.score}")
                    elif 120 < now - self.startTime <= 150:
                        self.score += 25000
                        self.canvas.itemconfigure(self.scoreText, text=f"Score: {self.score}")
                    elif 150 < now - self.startTime <= 180:
                        self.score += 10000
                        self.canvas.itemconfigure(self.scoreText, text=f"Score: {self.score}")
                    elif now - self.startTime > 180:
                        self.score += 1000
                        self.canvas.itemconfigure(self.scoreText, text=f"Score: {self.score}")

                    self.canvas.create_text(300, 350, text="GAME CLEAR", fill="blue", font=("Arial", 50))

                return
        

    def gameLoop(self):
        self.heroMove()
        self.bulletMove()
        self.enemyMove()
        self.heroAttack()
        self.heroDemage()
        self.bossEnter()
        self.bossControl()
        self.bossBulletMove()
        self.bossDemage()
        self.window.after(16, self.gameLoop)

if __name__ == "__main__":
    mainGame()