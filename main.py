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

    def attack(self):
        pass

class Guard(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Muhafız", 80, 10, 20, True, (1,1,1), x, y, map_boyut, renk, sira)

class Archer(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Okçu",  30, 20, 60, False, (2,2,2), x, y, map_boyut, renk, sira)


class Swordsman(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Topçu",  30, 50, 100, False, (2,2,0), x, y, map_boyut, renk, sira)


class Rider(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Atlı",  40, 30, 30, True, (0,0,3), x, y, map_boyut, renk, sira)


class Medic(Warrior):
    def __init__(self, x, y, map_boyut, renk, sira):
        super().__init__("Sağlıkçı", 100, 10, 50, False, (2,2,2), x, y, map_boyut, renk, sira)
    

class Player:
    def __init__(self, name):
        self.name = name
        self.resources = 200
        self.warriors = []  # Savaşçıları tutmak için bir liste eklendi

    def add_warrior(self, warrior, position):
        self.warriors.append((warrior, position))

    def remove_warrior(self, warrior):
        self.warriors = [w for w in self.warriors if w[0] != warrior]

    def get_warrior_positions(self):
        return [warrior[1] for warrior in self.warriors]

class World:
    def __init__(self, size):
        self.size = size
        self.grid = [['-' for _ in range(size)] for _ in range(size)]
        self.players = []

    def add_player(self, player):
        self.players.append(player)



    def print_world(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Ekran temizleme
        table = Table(show_header=False, show_lines=True, box= box.ASCII_DOUBLE_HEAD)

        for y in range(self.size):
            row = []
            for x in range(self.size):
                if self.grid[x][y] == '-':
                    row.append(Text(".", style="blue on red"))
                else:
                    row.append(Text(self.grid[x][y].name[0]))
            table.add_row(*row)
        print (table)
    

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

    def show_possible_placements(self, warrior):
        possible_placements = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == '-':
                    if (i > 0 and self.grid[i - 1][j] != '-') or \
                       (i < self.size - 1 and self.grid[i + 1][j] != '-') or \
                       (j > 0 and self.grid[i][j - 1] != '-') or \
                       (j < self.size - 1 and self.grid[i][j + 1] != '-'):
                        possible_placements.append((i, j))
        print(f"Possible placements for {warrior.name}: {possible_placements}")

class Game:
    def __init__(self):
        self.world = None
        self.num_players = 0
        self.turn_count = 0
        self.current_player_index = 0

    def start_game(self):
        while True:
            size = int(input("Dünya boyutunu girin (8 ile 32 arası bir sayı): "))
            if size < 8 or size > 32:
                print("Geçersiz boyut!")
            else:
                self.world = World(size)
                break

        while True:
            self.num_players = int(input("Oyuncu sayısını girin (1 ile 4 arası bir sayı): "))
            if self.num_players < 1 or self.num_players > 4:
                print("Geçersiz oyuncu sayısı!")
            else:
                break

        for i in range(self.num_players):
            player_name = input(f"{i+1}. oyuncunun adını girin: ")
            self.world.add_player(Player(player_name))

        for i in range(self.num_players):
            x = random.randint(0, self.world.size - 1)
            y = random.randint(0, self.world.size - 1)
            self.world.grid[x][y]= Guard(x=x, y=y, map_boyut=self.world.size, renk= "red", sira= i)
           

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
        print(f"{player.name}, elinizde {player.resources} kaynak var.")

        while True:
            action = input("Savaşçı eklemek için 'E', pas geçmek için 'P' girin: ").upper()

            if action == 'E':
                if player.resources >= 10:
                    warrior_type = input("Eklemek istediğiniz savaşçı türünü girin (Muhafız / Okçu / Atlı / Topçu / Sağlıkçı): ").capitalize()
                    if warrior_type == 'Muhafız':
                        warrior = Guard(x=0, y=0, map_boyut=self.world.size, renk="white", sira=1)
                    elif warrior_type == 'Okçu':
                        warrior = Archer(x=0, y=0, map_boyut=self.world.size, renk="red", sira=1)
                    elif warrior_type == 'Atlı':
                        warrior = Rider(x=0, y=0, map_boyut=self.world.size, renk="green", sira=1)
                    elif warrior_type == 'Topçu':
                        warrior = Swordsman(x=0, y=0, map_boyut=self.world.size, renk="blue", sira=1)
                    elif warrior_type == 'Sağlıkçı':
                        warrior = Medic(x=0, y=0, map_boyut=self.world.size, renk="orange", sira=1)

                    else:
                        print("Geçersiz savaşçı türü!")
                        continue

                    self.world.show_possible_placements(warrior)
                
                    x = int(input("X koordinatını girin: "))
                    y = int(input("Y koordinatını girin: "))

                    warrior.x = x
                    warrior.y = y

                    if self.is_valid_placement(x, y):
                        self.world.grid[x][y] = warrior
                        player.add_warrior(warrior, (x, y))  # position parametresi ekleniyor
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
            return False

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
