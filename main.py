import argparse

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

# Requires time to be a string in the format "r" or "w"
def parse_time(time):
    if time == 'r':
        return 'rano'
    else:
        return 'wieczorem'

# Requires months and days to be of the same length
def generate_paths(months, days, times):
    paths = []
    time_index = 0;
    for i in range(len(months)):
        month = months[i]
        for day in parse_day_range(days[i]):
            if time_index >= len(times):
                time = 'rano'
            else:
                time = parse_time(times[time_index])

            path = month + "/" + day + "/" + time
            paths.append(path)
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
    parser.add_argument('--dni', nargs='+', required=True, help="Po tej opcji wpisujemy skróty dni tygodnia które nas interesują. Np. pn, pn-śr(wybór przedziału)")
    parser.add_argument('--pora', nargs='*', default=['r'], help="Pora dnia: r (rano) / w (wieczór) dla każdego dnia z osobna. Domyślnie r(rano) dla każdego z wybranych dni.")

    args = parser.parse_args()
    if not args.csv and not args.json:
        parser.error("Musisz wybrać przynajmniej jeden format pliku: -c/--csv lub -j/--json.")
    
    if len(args.msc) != len(args.dni):
        parser.error("Liczba podanych przez ciebie miesięcy musi być równa liczbie podanych dni!")

    return args

def main():
    args = parse_arguments()
    # Main logic to be implemented


main()
