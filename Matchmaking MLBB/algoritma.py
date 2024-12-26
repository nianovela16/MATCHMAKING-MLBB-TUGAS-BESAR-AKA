import random
import time
import matplotlib.pyplot as plt
import sys

# Mengatur batas rekursi untuk menangani jumlah pemain besar
sys.setrecursionlimit(3000)

# Contoh daftar pemain dengan MMR dan peran
def generate_players(num_players):
    roles = ["Tank", "Marksman", "Mage", "Support", "Fighter"]
    players = [
        {"id": i + 1, "mmr": random.randint(2000, 3000), "role": random.choice(roles)}
        for i in range(num_players)
    ]
    return players

def matchmaking_iterative(players):
    """
    Algoritma matchmaking versi iteratif.
    Membagi pemain menjadi dua tim yang seimbang berdasarkan MMR.
    """
    players = sorted(players, key=lambda x: x['mmr'], reverse=True)  # Urutkan berdasarkan MMR
    team1, team2 = [], []

    for i, player in enumerate(players):
        if i % 2 == 0:
            team1.append(player)
        else:
            team2.append(player)

    return team1, team2

def matchmaking_recursive(players, team1=None, team2=None):
    """
    Algoritma matchmaking versi rekursif.
    Membagi pemain menjadi dua tim yang seimbang berdasarkan MMR.
    """
    if team1 is None:
        team1 = []
    if team2 is None:
        team2 = []

    # Basis rekursi: jika tidak ada pemain yang tersisa
    if not players:
        return team1, team2

    # Ambil pemain dengan MMR tertinggi
    player = players.pop(0)

    # Tambahkan ke tim dengan total MMR lebih rendah
    if sum(p['mmr'] for p in team1) <= sum(p['mmr'] for p in team2):
        team1.append(player)
    else:
        team2.append(player)

    return matchmaking_recursive(players, team1, team2)

# Pengukuran waktu untuk berbagai ukuran pemain
num_players_list = [10, 50, 100, 500, 1000, 1500, 2000]
iterative_times = []
recursive_times = []

for num_players in num_players_list:
    players = generate_players(num_players)

    # Waktu untuk iteratif
    start_time_iter = time.time()
    matchmaking_iterative(players.copy())
    end_time_iter = time.time()
    iterative_times.append(end_time_iter - start_time_iter)

    # Waktu untuk rekursif
    try:
        start_time_rec = time.time()
        matchmaking_recursive(players.copy())
        end_time_rec = time.time()
        recursive_times.append(end_time_rec - start_time_rec)
    except RecursionError:
        print(f"RecursionError: Jumlah pemain terlalu besar untuk rekursi pada {num_players} pemain.")
        recursive_times.append(None)

# Menampilkan Running Time dalam bentuk tabel
print("\nTabel Running Time : \n")
print("Jumlah Pemain | Waktu Iteratif (detik) | Waktu Rekursif (detik) | Selisih (detik)")
print("-" * 58)
for n, t_iter, t_rec in zip(num_players_list, iterative_times, recursive_times):
    if t_rec is not None:
        selisih = t_rec - t_iter
        print(f"{n:<14} | {t_iter:<21.6f} | {t_rec:<21.6f} | {selisih:.6f}")
    else:
        print(f"{n:<14} | {t_iter:<21.6f} | RecursionError          | -")

# Visualisasi Perbandingan Waktu
plt.plot(num_players_list, iterative_times, marker='o', label='Iteratif (Pembagian Tim)', color='orange')
plt.plot(
    [x for x, y in zip(num_players_list, recursive_times) if y is not None],
    [y for y in recursive_times if y is not None],
    marker='o', label='Rekursif (Sorting)', color='blue')
plt.xlabel('Jumlah Pemain')
plt.ylabel('Waktu Eksekusi (detik)')
plt.title('Running Time: Rekursif vs Iteratif')
plt.legend()
plt.grid(True)
plt.show()
