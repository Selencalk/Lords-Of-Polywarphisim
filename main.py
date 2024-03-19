import os
import random
import numpy as np
import matplotlib.pyplot as plt

class Warrior:
    def __init__(self, name):
        self.name = name

    def attack(self):
        pass

class Guard(Warrior):
    def __init__(self):
        super().__init__("Muhafız")

    def attack(self):
        pass

class Archer(Warrior):
    def __init__(self):
        super().__init__("Okçu")

    def attack(self):
        pass

class Swordsman(Warrior):
    def __init__(self):
        super().__init__("Kılıçlı")

    def attack(self):
        pass

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

    def place_guard(self):
        corner = random.choice([(0, 0), (0, self.size - 1), (self.size - 1, 0), (self.size - 1, self.size - 1)])
        self.grid[corner[0]][corner[1]] = 'M'

    def print_world(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Ekran temizleme
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == '-':
                    print('\033[97m' + cell, end=' ')  # Beyaz renk
                else:
                    player_color = self.get_player_color((i, j))
                    if player_color:
                        print(f'\033[9{player_color}m{cell[0]}', end=' ')  # Oyuncu rengi
                    else:
                        print(cell[0], end=' ')  # Savaşçı
            print()
        print()

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
            self.world.place_guard()

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
                    warrior_type = input("Eklemek istediğiniz savaşçı türünü girin (Muhafız / Okçu / Kılıçlı): ").capitalize()
                    if warrior_type == 'Muhafız':
                        warrior = Guard()
                    elif warrior_type == 'Okçu':
                        warrior = Archer()
                    elif warrior_type == 'Kılıçlı':
                        warrior = Swordsman()
                    else:
                        print("Geçersiz savaşçı türü!")
                        continue

                    self.world.show_possible_placements(warrior)
                    x = int(input("X koordinatını girin: "))
                    y = int(input("Y koordinatını girin: "))

                    if self.is_valid_placement(x, y):
                        self.world.grid[x][y] = warrior.name[0]
                        player.add_warrior(warrior, (x, y))  # position parametresi ekleniyor
                        player.resources -= 10
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