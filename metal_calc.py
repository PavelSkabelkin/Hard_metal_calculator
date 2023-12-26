import csv
from tabulate import tabulate

standards = {
    1: "ГОСТ 8239-89 Двутавровая балка",
    2: "ГОСТ 8240-97 Швеллер",
    3: "ГОСТ 8509-93 Уголок"
}

def calculate_total_weight_and_length(data, length):
    total_weight = 0
    total_length = 0
    result = []

    for roll_number, weight_per_meter, standard in data:
        try:
            weight_per_meter = float(weight_per_meter)
            total_weight_per_profile = weight_per_meter * length
            total_weight += total_weight_per_profile
            total_length += length
            result.append((roll_number, weight_per_meter, total_weight_per_profile, standard, length))
        except ValueError:
            print(f"Ошибка: Неверное значение веса на метре для профиля {roll_number}. Пропускаем.")

    return total_weight, total_length, result

def read_data_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Пропускаем заголовок
        return [tuple(row) for row in reader]

def display_profiles(data):
    print("\nВыберите номер профиля:")
    for i, (roll_number, weight_per_meter, standard) in enumerate(data, start=1):
        print(f"{i}. Профиль {roll_number} ({weight_per_meter} кг/м) - {standard}")

def main():
    file_paths = [
        '/app/gost_8239_89_d_beam_202312252235.csv',
        '/app/gost_8240_97_202312252235.csv',
        '/app/gost_8509_93_202312252236.csv'
    ]

    try:
        total_weight_data = []
        total_weight = 0
        total_length = 0

        while True:
            print("\nВыберите стандарт:")
            for i, standard_description in standards.items():
                print(f"{i}. {standard_description}")

            choice = int(input("Введите номер стандарта (0 для завершения): "))
            if choice == 0 or choice > len(file_paths):
                break

            data = read_data_from_csv(file_paths[choice - 1])
            display_profiles(data)

            profile_choice = int(input("Введите номер профиля: "))
            if 1 <= profile_choice <= len(data):
                chosen_profile = data[profile_choice - 1]

                length = float(input("Введите длину металлопроката в метрах: "))

                profile_total_weight, profile_total_length, profile_data = calculate_total_weight_and_length([chosen_profile], length)
                total_weight += profile_total_weight
                total_length += profile_total_length
                total_weight_data.extend(profile_data)

                print("\nРезультаты:")
                print(tabulate(total_weight_data, headers=["Roll Number", "Weight Per Meter", "Total Weight", "Standard", "Length"],
                               tablefmt="pretty"))

                add_more = input("Желаете добавить еще прокат? (y/n): ").lower()
                if add_more != 'y':
                    break
            else:
                print("Ошибка: Неверный номер профиля. Пожалуйста, выберите существующий номер профиля.")

    except ValueError as e:
        print(f"Ошибка: {e}")


    print(tabulate(total_weight_data, headers=["Roll Number", "Weight Per Meter", "Weight", "Standard", "Length"],
                   tablefmt="pretty"))
    print(f"Общая масса всего запроса: {total_weight} кг")
    print(f"Общая длина всего запроса: {total_length} м")
if __name__ == "__main__":
    main()
