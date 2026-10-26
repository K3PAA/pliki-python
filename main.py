import argparse
import csv
import json
import os
import random
from pathlib import Path

def is_day_range_valid(day_range):
    valid_days = {'pn': 0, 'wt': 1, 'śr': 2, 'cz': 3, 'pt': 4, 'sb': 5, 'nd': 6}

    if day_range.count('-') > 1:
        return False

    if '-' in day_range:
        start, end = day_range.split('-')
        if start not in valid_days or end not in valid_days or valid_days[start] > valid_days[end]:
            return False
    elif day_range not in valid_days:
        return False

    return True

# Requires day_range to be a string in the format "dd-dd" or "dd"
def parse_day_range(day_range):
    day_numbers = {'pn': 0, 'wt': 1, 'śr': 2, 'cz': 3, 'pt': 4, 'sb': 5, 'nd': 6}
    day_names = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']

    days = []

    if '-' in day_range:
        start, end = day_range.split("-")
        for i in range(day_numbers[start], day_numbers[end] + 1):
            days.append(day_names[i])
    else:
        days.append(day_names[day_numbers[day_range]])

    return days

# Requires time to be a string "r" or "w"
def parse_time(time):
    if time == 'r':
        return 'rano'
    else:
        return 'wieczorem'

# Requires months and days to be of the same length
def generate_paths(months, days, times):
    paths = []
    time_index = 0
    for i in range(len(months)):
        month = months[i]
        for day in parse_day_range(days[i]):
            if time_index >= len(times):
                time = 'rano'
            else:
                time = parse_time(times[time_index])

            path = os.path.join(os.getcwd(), month, day, time)
            paths.append(Path(path))
            time_index += 1

    return paths

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='Skrypt do plików',
        description='%(prog)s to skrypt tworzący lub czytający pliki.',
        epilog="Przykładowe zapytanie: python3 main.py -t -c --msc styczen luty --dni pn-wt pt --pora r w"
    )

    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument('-t', '--tworz', action='store_true', help="Używamy tej opcji, gdy zamierzamy tworzyć dane.")
    exclusive_group.add_argument('-o', '--odczyt', action='store_true', help="Używamy tej opcji, gdy zamierzamy czytać dane.")

    parser.add_argument('-c', '--csv', action='store_true', help="Używamy tej opcji gdy korzystamy z formatu CSV.")
    parser.add_argument('-j', '--json', action='store_true', help="Używamy tej opcji gdy korzystamy z formatu JSON.")

    parser.add_argument('--msc', nargs='+', required=True, help="Po tej opcji wpisujemy nazwy miesięcy które nas interesują. Np. styczeń, luty")
    parser.add_argument('--dni', nargs='+', required=True, help="Po tej opcji wpisujemy skróty dni tygodnia które nas interesują. Np. pn, pn-śr (wybór przedziału)")
    parser.add_argument('--pora', nargs='*', default=['r'], choices=['r', 'w'], help="Pora dnia: r (rano) / w (wieczór) dla każdego dnia z osobna. Domyślnie r (rano) dla każdego z wybranych dni.")

    args = parser.parse_args()
    if not args.csv and not args.json:
        parser.error("Musisz wybrać przynajmniej jeden format pliku: -c/--csv lub -j/--json.")

    for day_range in args.dni:
        if not is_day_range_valid(day_range):
            parser.error(f"Niepoprawny zakres dni: {day_range}. Poprawne skróty to: pn, wt, śr, cz, pt, sb, nd lub zakres np. pn-śr.")

    if len(args.msc) != len(args.dni):
            parser.error("Liczba podanych przez ciebie miesięcy musi być równa liczbie podanych dni!")

    return args

def generate_random_data():
    model = random.choice(['A', 'B', 'C'])
    score = random.randint(0, 1000)
    time_val = f"{random.randint(0, 1000)}s"
    return model, score, time_val

def write_csv(dir_path):
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / "Dane.csv"

    model, score, time_val = generate_random_data()

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Model', ' Wynik', ' Czas', ''])
        writer.writerow([f"{model} ", f" {score} ", f" {time_val}", ''])

def read_csv(dir_path):
    file_path = dir_path / "Dane.csv"

    if not file_path.exists():
        print(f"Brak pliku: {file_path}")
        return 0

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)

        if len(rows) >= 2 and len(rows[1]) >= 3:
            second_row = rows[1]
            model = second_row[0].strip()
            time_str = second_row[2].strip()

            if model == 'A':
                return int(time_str.replace('s', ''))

    return 0

def write_json(dir_path):
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / "Dane.json"

    model, score, time_val = generate_random_data()

    data = {"Model": model, "Wynik": score, "Czas": time_val}

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def read_json(dir_path):
    file_path = dir_path / "Dane.json"

    if not file_path.exists():
        print(f"Brak pliku: {file_path}")
        return 0

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        if data.get('Model') == 'A':
            return int(data.get('Czas', '0').replace('s', ''))

        return 0

def main():
    args = parse_arguments()
    paths = generate_paths(args.msc, args.dni, args.pora)

    if args.csv:
        if args.tworz:
            for path in paths:
                write_csv(path)
            print("Utworzono pliki Dane.csv we wskazanych ścieżkach.")
        elif args.odczyt:
            total_time = 0
            for path in paths:
                total_time += read_csv(path)
            print(f"Suma czasu dla modelu A (CSV): {total_time}s")

    if args.json:
        if args.tworz:
            for path in paths:
                write_json(path)
            print("Utworzono pliki Dane.json we wskazanych ścieżkach.")
        elif args.odczyt:
            total_time = 0
            for path in paths:
                total_time += read_json(path)
            print(f"Suma czasu dla modelu A (JSON): {total_time}s")

if __name__ == "__main__":
    main()
