import os
from logging import getLogger, StreamHandler, FileHandler, Formatter, ERROR

class FileNotFound(Exception):
    """ File not found """

class FileCorrupted(Exception):
    """ The file is corrupt or cannot be read/written. """

def logger(exeption, mode="console"):
    """
    Parameterized decorator.
    :exception_type: — the type of exception being caught
    :mode: — 'console' or 'file'
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = getLogger(func.__name__)

            logger.setLevel(ERROR)
            logger.handlers.clear()

            if mode == "console":
                handler = StreamHandler()
            elif mode == "file":
                handler = FileHandler("log.txt", encoding="utf-8")
            else:
                raise ValueError("Невідомий режим логування!")
        
            format = Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(format)
            logger.addHandler(handler)

            try:
                return func(*args, **kwargs)
            except exeption as e:
                logger.error(f"Помилка: {e}")
                raise
        
        return wrapper
    return decorator

class CSVFileManager:
    def __init__(self):
        self.input_dir = "input"
        self.output_dir = "output"

        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        self.input_file = os.path.join(self.input_dir, "data.csv")
        self.output_file = os.path.join(self.output_dir, "data.csv")

        if not os.path.exists(self.input_file):
            open(self.input_file, "a", encoding="utf-8").close()
        if not os.path.exists(self.output_file):
            open(self.output_file, "a", encoding="utf-8").close()
    
    @logger(FileCorrupted, mode="file")
    def read(self):
        """ Reads CSV from input, or if it is empty then from output """

        if os.path.exists(self.input_file) and os.path.getsize(self.input_file) > 0:
            read_file = self.input_file
        elif os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0:
            read_file = self.output_file
        else:
            raise FileCorrupted("Both files are missing or empty.")

        try:
            with open(read_file, "r", encoding="utf-8") as file:
                data = [line.strip().split(",") for line in file.readlines()]
                return data
            
        except Exception:
            raise FileCorrupted("The file could not be read.")
        
    @logger(FileCorrupted, mode="file")
    def rewrite_all(self, rows: list):
        """ Overwrites CSV file """
        try:
            with open(self.input_file, "w", encoding="utf-8") as file:
                for row in rows:
                    file.write(",".join(row) + "\n")
        except Exception:
            raise FileCorrupted("Failed to write file.")

    @logger(FileCorrupted, mode="file")
    def append(self, row: list):
        """ Appends rows to a CSV file """
        try:
            with open(self.input_file, "a", encoding="utf-8") as file:
                file.write(",".join(row) + "\n")
        except Exception:
            raise FileCorrupted("Could not add to file.")

if __name__ == "__main__":
    csv_file = CSVFileManager()
    num_row = 1
    while True:
        os.system("cls")

        print("Меню:")
        print("1. Прочитати файл\n2. Переписати файл\n3. Додати до файлу\n(other). Вийти")
        action = input("Що бажаєте зробити? (Введіть одне з чисел зазначених вище): ")

        if action == "1":
            os.system("cls")

            exel = csv_file.read()
            for row in exel:
                print("\t | \t".join(row))
            
            input()

        elif action == "2":
            num_row = 1
            os.system("cls")

            rows = []
            print("Введіть рядки у форматі 'значення1,значення2,...,значенняN' (порожній рядок для завершення):")
            
            while True:
                new_row = input(f"Рядок, {num_row}: ")
                if new_row == "" and num_row == 1:
                    print("Не було введено жодного рядка. Файл буде порожнім.")
                    autific = input("Продовжити? (Так(1)/Ні(2)): ")
                    if autific == "1":
                        break
                    else:
                        num_row = 1
                        continue
                
                elif new_row == "":
                    break
                num_row += 1
                rows.append(new_row.split(","))
            
            csv_file.rewrite_all(rows)

        elif action == "3":
            new_row = ""
            os.system("cls")

            print("Введіть рядок у форматі 'значення1,значення2,значення3':")

            while True:
                new_row = input(f"Рядок, {num_row}: ")
                if new_row == "":
                    break
                num_row += 1
                csv_file.append(new_row.split(","))
            
            input()

        else:
            break
