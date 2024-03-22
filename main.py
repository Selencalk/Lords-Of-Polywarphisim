import os
import random
from rich.table import Table
from rich.text import Text
from rich import print
from rich import box


class Warrior:
    def __init__(self, name, can, kaynak, hasar, gercekhasar, menzil, x, y, map_boyut, renk, sira):
        self.name = name
        self.can = can
        self.kaynak = kaynak
        self.hasar = hasar
        self.gercekhasar = gercekhasar
        self.menzil = menzil
        self.x = x
        self.y = y
        self.map_boyut = map_boyut
        self.renk = renk
        self.sira = sira
        self.komsular = self.komsulari_hesapla(x, y, map_boyut)

    def komsulari_hesapla(self, x, y, map_boyut):
        a = [[x - 1, y - 1], [x, y - 1], [x - 1, y], [x + 1, y - 1], [x - 1, y + 1], [x, y + 1], [x + 1, y + 1],
             [x + 1, y], [x, y]]
        for ID, b in enumerate(a):
            if b[0] < 0 or b[0] > map_boyut or b[1] < 0 or b[1] > map_boyut:
                a[ID] = None
        return a

    def etrafindaki_tum_dusmanlar(self, map):
        (yatay, dikey, capraz) = self.menzil

        dusmanlar = []

        for i in range(1, yatay + 1):
            if self.x - i >= 0:
                sol = map.matris[self.y][self.x - i]
                if self.dusman_mi(sol) and sol.renk == self.renk:
                    dusmanlar.append(sol)

            if self.x + i < map.map_boyut - 1:
                sag = map.matris[self.y][self.x + i]
                if self.dusman_mi(sag) and sag.renk == self.renk:
                    dusmanlar.append(sag)

        for i in range(1, dikey + 1):
            if self.y - i >= 0:
                ust = map.matris[self.y - i][self.x]
                if self.dusman_mi(ust) and ust.renk == self.renk:
                    dusmanlar.append(ust)

            if self.y + i < map.map_boyut - 1:
                alt = map.matris[self.y + i][self.x]
                if self.dusman_mi(alt) and alt.renk == self.renk:
                    dusmanlar.append(alt)

        for i in range(1, capraz + 1):
            if self.y - i >= 0 and self.x - i >= 0:
                sol_ust = map.matris[self.y - i][self.x - i]
                if self.dusman_mi(sol_ust) and sol_ust.renk == self.renk:
                    dusmanlar.append(sol_ust)

            if self.y - i >= 0 and self.x + i < map.map_boyut - 1:
                sag_ust = map.matris[self.y - i][self.x + i]
                if self.dusman_mi(sag_ust) and sag_ust.renk == self.renk:
                    dusmanlar.append(sag_ust)

            if self.x - i >= 0 and self.y + i < map.map_boyut - 1:
                sol_alt = map.matris[self.y + i][self.x - i]
                if self.dusman_mi(sol_alt) and sol_alt.renk == self.renk:
                    dusmanlar.append(sol_alt)

            if self.x + i < map.map_boyut - 1 and self.y + i < map.map_boyut - 1:
                sag_alt = map.matris[self.y + i][self.x + i]
                if self.dusman_mi(sag_alt) and sag_alt.renk == self.renk:
                    dusmanlar.append(sag_alt)

        print(self.etrafindaki_tum_dusmanlar(map))

        return dusmanlar

    @staticmethod
    def dusman_mi(kare):
        if kare != 0:
            return True
        return False


class Guard(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Muhafız", 80, 10, 20, True, (1, 1, 1), x, y, map_boyut, renk, sira)


class Archer(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Okçu", 30, 20, 60, False, (2, 2, 2), x, y, map_boyut, renk, sira)


class Swordsman(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Topçu", 30, 50, 100, False, (2, 2, 0), x, y, map_boyut, renk, sira)


class Rider(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Atlı", 40, 30, 30, True, (0, 0, 3), x, y, map_boyut, renk, sira)


class Medic(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Sağlıkçı", 100, 10, 50, False, (2, 2, 2), x, y, map_boyut, renk, sira)


class Player:
    def __init__(self, name, renk):
        self.name = name
        self.resources = 200
        self.warriors = []  # Savaşçıları tutmak için bir liste eklendi
        self.renk = renk
        self.savasci_sayisi = 0
        self.muhafiz_sayisi = 0
        self.okcu_sayisi = 0
        self.topcu_sayisi = 0
        self.atli_sayisi = 0
        self.saglikci_sayisi = 0

    def add_warrior(self, warrior):
        self.warriors.append(warrior)

    def remove_warrior(self, warrior):
        self.warriors = [w for w in self.warriors if w[0] != warrior]

    def get_warrior_positions(self):
        return [warrior[1] for warrior in self.warriors]

    def komsular(self):
        a = []
        for warrior in self.warriors:
            a += warrior.komsular

        b = []
        [
            b.append(komsu)
            for komsu in a
            if komsu not in b
        ]
        return b


class World:
    def __init__(self, size):
        self.size = size
        self.grid = [['-' for _ in range(size)] for _ in range(size)]
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def print_world(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Ekran temizleme
        matris = []
        komsular = {}

        for players in self.players:
            komsular[players.renk] = []

        for y in range(self.size):
            row = []
            for x in range(self.size):
                block = self.grid[y][x]
                if block == '-':
                    row.append(Text("."))
                else:
                    komsular[block.renk] += block.komsular
                    row.append(Text(block.name[0] + str(block.sira), style=block.renk))
            matris.append(row)

        for players in self.players:
            for komsu in komsular[players.renk]:
                if komsu:
                    if self.grid[komsu[0]][komsu[1]] == '-':
                        matris[komsu[0]][komsu[1]] = Text("-", style=players.renk)

        table = Table(show_header=False, show_lines=True, box=box.DOUBLE)
        for row in matris:
            table.add_row(*row)

        print(table)

        table = Table(show_header=False, show_lines=True, box=box.SQUARE)

        for row in self.players:

            table.add_row(*[str(row.name), str(row.resources)])

        print(table)

    def get_player_color(self, pos):
        for i, player in enumerate(self.players):
            for warrior in player.get_warrior_positions():  # Savaşçı pozisyonlarına erişmek için değişiklik yapıldı
                if pos in self.get_adjacent_positions(warrior):
                    return i + 1
        return None

    def get_adjacent_positions(self, pos):
        adjacent_positions = []
        x, y = pos
        for i in range(max(0, x - 1), min(self.size, x + 2)):
            for j in range(max(0, y - 1), min(self.size, y + 2)):
                adjacent_positions.append((i, j))
        return adjacent_positions

    def show_possible_placements(self, warrior, player):
        possible_placements = []
        if warrior.renk == player.renk:
            for i in range(self.size):
                for j in range(self.size):
                    if self.grid[i][j] == '-':
                        if (i > 0 and self.grid[i - 1][j] != '-') or \
                                (i < self.size - 1 and self.grid[i + 1][j] != '-') or \
                                (j > 0 and self.grid[i][j - 1] != '-') or \
                                (j < self.size - 1 and self.grid[i][j + 1] != '-') or \
                                (j < self.size - 1 and i < self.size - 1 and self.grid[i + 1][j + 1] != '-') or \
                                (j > 0 and i > 0 and self.grid[i - 1][j - 1] != '-') or \
                                (i < self.size - 1 and j > 0 and self.grid[i + 1][j - 1] != '-') or \
                                (i > 0 and j < self.size - 1 and self.grid[i - 1][j + 1] != '-') or \
                                (self.grid[i][j] != '-'):

                            possible_placements.append((i, j))
            print(f"Possible placements for {warrior.name}: {possible_placements}")


class Game:
    def __init__(self):
        self.world = None
        self.num_players = 0
        self.turn_count = 0
        self.current_player_index = 0
        self.renkler = ["red", "blue", "green", "yellow"]

    def start_game(self):
        while True:
            print("1= 16x16")
            print("2= 24x24")
            print("3= 32x32")
            print("4= Kendi boyutumu seçmek istiyorum.")
            size = int(input("Lütfen dünya boyutunu seçiniz: "))
            if size == 1:
                self.world = World(16)
                break
            elif size == 2:
                self.world = World(24)
                break
            elif size == 3:
                self.world = World(32)
                break
            elif size == 4:
                size = int(input("İstediğiniz dünya boyutunu giriniz: "))
                if size < 8 or size > 32:
                    print("Geçerli bir boyut giriniz")
                else:
                    self.world = World(size)
                    break
            else:
                print("Geçersiz boyut girdiniz!")
                break

        while True:
            print("1= 1 Oyuncu")
            print("2= 2 Oyuncu")
            print("3= 3 Oyuncu")
            print("4= 4 Oyuncu")
            size = int(input("Oyuncu sayısını seçiniz: "))
            if size == 1:
                self.num_players = 1
                break
            elif size == 2:
                self.num_players = 2
                break
            elif size == 3:
                self.num_players = 3
                break
            elif size == 4:
                self.num_players = 4
                break
            else:
                print("Geçersiz oyuncu sayısı!")
                break

        for i in range(self.num_players):
            print(Text(f"{i + 1}. oyuncunun adını girin: ", style="purple", end=""))
            player_name = input()

            self.world.add_player(Player(player_name, renk=self.renkler[i]))

        for i in range(self.num_players):
            x = random.randint(0, self.world.size - 1)
            y = random.randint(0, self.world.size - 1)
            self.world.grid[x][y] = Guard(x=x, y=y, map_boyut=self.world.size,
                                          renk=self.renkler[i], sira=self.world.players[i].muhafiz_sayisi + 1)
            self.world.players[i].add_warrior(self.world.grid[x][y])
            self.world.players[i].muhafiz_sayisi += 1

        self.play_game()

    def play_game(self):
        while True:
            print(f"Sıra {self.world.players[self.current_player_index].name} oyuncusunda.")
            self.turn_count += 1
            self.world.print_world()

            self.take_turn()

            if self.check_game_end():
                break

            self.current_player_index = (self.current_player_index + 1) % self.num_players

    def take_turn(self):
        player = self.world.players[self.current_player_index]
        print(Text(f"{player.name}, elinizde {player.resources} kaynak var.", style=player.renk))

        while True:
            action = input("Savaşçı eklemek için 'E', pas geçmek için 'P' girin: ").upper()

            if action == 'E':
                if player.resources >= 10:
                    warrior_type = input(
                        "Eklemek istediğiniz savaşçı türünü girin "
                        "(Muhafız / Okçu / Atlı / Topçu / Sağlıkçı): ").capitalize()
                    if warrior_type == 'Muhafız':
                        warrior = Guard(x=0, y=0, map_boyut=self.world.size, renk=player.renk,
                                        sira=player.muhafiz_sayisi + 1)
                        player.muhafiz_sayisi += 1
                    elif warrior_type == 'Okçu':
                        warrior = Archer(x=0, y=0, map_boyut=self.world.size, renk=player.renk,
                                         sira=player.okcu_sayisi + 1)
                        player.okcu_sayisi += 1
                    elif warrior_type == 'Atlı':
                        warrior = Rider(x=0, y=0, map_boyut=self.world.size, renk=player.renk,
                                        sira=player.atli_sayisi + 1)
                        player.atli_sayisi += 1
                    elif warrior_type == 'Topçu':
                        warrior = Swordsman(x=0, y=0, map_boyut=self.world.size, renk=player.renk,
                                            sira=player.topcu_sayisi + 1)
                        player.topcu_sayisi += 1
                    elif warrior_type == 'Sağlıkçı':
                        warrior = Medic(x=0, y=0, map_boyut=self.world.size, renk=player.renk,
                                        sira=player.saglikci_sayisi + 1)
                        player.saglikci_sayisi += 1

                    else:
                        print("Geçersiz savaşçı türü!")
                        continue

                    print(player.komsular())

                    x = int(input("X koordinatını girin: "))
                    y = int(input("Y koordinatını girin: "))

                    warrior.x = x
                    warrior.y = y
                    warrior.komsular = warrior.komsulari_hesapla(x, y, self.world.size)

                    if self.is_valid_placement(x, y):
                        if self.world.grid[x][y] != "-":
                            player.resources += self.world.grid[x][y].kaynak * 80 / 100

                        self.world.grid[x][y] = warrior
                        player.add_warrior(warrior)
                        player.resources -= warrior.kaynak
                        break
                    else:
                        print("Geçersiz konum!")
                else:
                    print("Yeterli kaynağınız yok!")
            elif action == 'P':
                break
            else:
                print("Geçersiz eylem!")

    def is_valid_placement(self, x, y):
        if self.world.grid[x][y] != '-':
            return True
        
        for i in range(max(0, x - 1), min(self.world.size, x + 2)):
            for j in range(max(0, y - 1), min(self.world.size, y + 2)):
                if self.world.grid[i][j] != '-':
                    return True

        return False

    def check_game_end(self):
        if self.turn_count >= 3:
            num_players_with_warriors = sum(1 for player in self.world.players if player.warriors)
            if num_players_with_warriors <= 1:
                print("Oyun bitti, kazanan yok.")
                return True

        return False


game = Game()
game.start_game()
