from random import randint
import pyxel

class App:
    def __init__(self):
        pyxel.init(120, 120, caption="Bark and Whine")
        pyxel.load("asset.pyxres")
        self.player_x = 55
        self.player_y = 55
        self.player_d = 1 # 方向
        self.player_is_alive = True #不使用
        self.x = 0
        self.y = 0
        self.score = 100
        # dir, kyori from center, is_active 0:noattive,1:active,2:coming 3:going
        self.meat = [(randint(1, 4), 60, 1) for i in range(1)]
        self.oran = [(randint(1, 4), 60, 1) for i in range(1)]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # sound
        if (pyxel.btnp(pyxel.KEY_RIGHT)
            or pyxel.btnp(pyxel.KEY_LEFT)
            or pyxel.btnp(pyxel.KEY_UP)
            or pyxel.btnp(pyxel.KEY_DOWN)):
            # whine
            if not pyxel.btn(pyxel.KEY_SPACE):
                pyxel.playm(1, loop=False)
            # bark
            elif pyxel.btn(pyxel.KEY_SPACE):
                pyxel.playm(0, loop=False)
        
        self.update_player()

        for i, v in enumerate(self.meat):
            self.meat[i] = self.update_meat(*v)

        for i, v in enumerate(self.oran):
            self.oran[i] = self.update_oran(*v)


    def update_player(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_d = 1
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_d = 2
        if pyxel.btn(pyxel.KEY_UP):
            self.player_d = 3
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_d = 4

        if self.score < 0:
            pyxel.playm(2, loop=False)
            self.score = 100

    def update_meat(self, dir, r, is_active):
        if is_active == 1:
            if (r <= 10):
                is_active = 0
                self.score += 10
        elif is_active == 2:
            r -= 2 # 加速
            if (r <= 10):
                is_active = 0
                self.score += 10
        elif is_active == 3:
            r += 4 # 外へ
        elif is_active == 0:
            r = 70

        r -= 2

        if r > 60:
            r = 60
            dir = randint(1,4)
            is_active = 1

        if (dir == 1
            and pyxel.btn(pyxel.KEY_RIGHT)):
            if not pyxel.btn(pyxel.KEY_SPACE):
                is_active = 2
            else:
                is_active = 3
        if (dir == 2
            and pyxel.btn(pyxel.KEY_LEFT)):
            if not pyxel.btn(pyxel.KEY_SPACE):
                is_active = 2
            else:
                is_active = 3
        if (dir == 3
            and pyxel.btn(pyxel.KEY_UP)):
            if not pyxel.btn(pyxel.KEY_SPACE):
                is_active = 2
            else:
                is_active = 3
        if (dir == 4
            and pyxel.btn(pyxel.KEY_DOWN)):
            if not pyxel.btn(pyxel.KEY_SPACE):
                is_active = 2
            else:
                is_active = 3

        return dir, r, is_active

    # to do
    def update_oran(self, dir, r, is_active):
        if is_active == 1:
            if (r<= 10):
                r = 80
                self.score -= 20
        elif is_active == 0:
            r += 4

        r -= 2

        #範囲外に出たらリセット
        if r > 60:
            r = 60
            dir = randint(1,4)
            is_active = 1

        if (
            dir == 1
            and pyxel.btn(pyxel.KEY_SPACE)
            and pyxel.btn(pyxel.KEY_RIGHT)
        ):
            is_active = 0
        if (
            dir == 2
            and pyxel.btn(pyxel.KEY_SPACE)
            and pyxel.btn(pyxel.KEY_LEFT)
        ):
            is_active = 0
        if (
            dir == 3
            and pyxel.btn(pyxel.KEY_SPACE)
            and pyxel.btn(pyxel.KEY_UP)
        ):
            is_active = 0
        if (
            dir == 4
            and pyxel.btn(pyxel.KEY_SPACE)
            and pyxel.btn(pyxel.KEY_DOWN)
        ):
            is_active = 0

        return dir, r, is_active
        
    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, 51, 51, 1)
        pyxel.rect(68, 0, 51, 51, 2)
        pyxel.rect(0, 68, 51, 51, 3)
        pyxel.rect(68, 68, 51, 51, 4)
        pyxel.circb(60, 60, 15, 7)
        #draw player
        # to do 方向をかえる
        pyxel.blt(52,52,0,0,0,16,12)
        #draw meat
        for dir, r, is_active in self.meat:
                if dir == 1: # Right
                    pyxel.blt(60+r, 52, 2, 0, 0, 16, 16, 12)
                elif dir == 2: # Left
                    pyxel.blt(60-r, 52, 2, 0, 0, 16, 16, 12)
                elif dir == 3: # Up
                    pyxel.blt(52, 60-r, 2, 0, 0, 16, 16, 12)
                elif dir == 4: # Down
                    pyxel.blt(52, 60+r, 2, 0, 0, 16, 16, 12)
        # draw oran
        for dir, r, is_active in self.oran:
                if dir == 1: # Right
                    pyxel.blt(60+r, 52, 1, 0, 0, 16, 16, 12)
                elif dir == 2: # Left
                    pyxel.blt(60-r, 52, 1, 0, 0, 16, 16, 12)
                elif dir == 3: # Up
                    pyxel.blt(52, 60-r, 1, 0, 0, 16, 16, 12)
                elif dir == 4: # Down
                    pyxel.blt(52, 60+r, 1, 0, 0, 16, 16, 12)

        # draw score
        s = "TAGHNES {:>4}".format(self.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)

App()