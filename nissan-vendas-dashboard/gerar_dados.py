# Script auxiliar so para GERAR os dados de exemplo (voce nao precisa mexer nele).
import csv, random
from datetime import date, timedelta

random.seed(42)

modelos = ["Kicks", "kicks", " Sentra", "Sentra ", "Versa", "VERSA",
           "Frontier", "frontier ", "March", "Leaf"]
concessionarias = ["Nissan Centro", "Nissan Centro ", "Nissan Zona Sul",
                   "nissan zona sul", "Nissan Norte", "Nissan Oeste"]
regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
vendedores = ["Ana Souza", "Bruno Lima", "Carla Dias", "Diego Reis", "Elaine Costa"]
preco_base = {"kicks": 135000, "sentra": 190000, "versa": 120000,
              "frontier": 260000, "march": 90000, "leaf": 320000}

def formata_data(d):
    f = random.choice(["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"])
    return d.strftime(f)

def formata_preco(v):
    # metade vem como numero puro, metade como texto "R$ 1.234,56" (padrao BR)
    if random.random() < 0.5:
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return str(v)

linhas = []
inicio = date(2025, 1, 1)
for i in range(220):
    d = inicio + timedelta(days=random.randint(0, 240))
    modelo = random.choice(modelos)
    conc = random.choice(concessionarias)
    reg = random.choice(regioes)
    unidades = random.randint(1, 8)
    chave = modelo.strip().lower()
    preco = round(preco_base[chave] * random.uniform(0.95, 1.08), 2)
    vend = random.choice(vendedores)
    if random.random() < 0.05: unidades = ""
    if random.random() < 0.05: reg = ""
    linhas.append([formata_data(d), modelo, conc, reg, unidades, formata_preco(preco), vend])

for _ in range(8):
    linhas.append(random.choice(linhas[:]))  # duplicatas de proposito

with open("dados/vendas_brutas.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)  # o csv.writer poe aspas automaticamente quando precisa
    w.writerow(["data","modelo","concessionaria","regiao","unidades","preco_unitario","vendedor"])
    w.writerows(linhas)

print(f"Gerado dados/vendas_brutas.csv com {len(linhas)} linhas")
