import argparse

def main():
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
    print(args.tworz, args.odczyt, args.csv, args.json, args.msc, args.dni, args.pora)



main()