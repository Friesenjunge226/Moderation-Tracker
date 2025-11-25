import time
import numbers
import decimal

OUTPUT_FILE = "count.txt"
MainVar = 0


def countdown():

    end_time = time.perf_counter() + total_time

    while True:
        remaining = end_time - time.perf_counter()
            
        if remaining <= 0:
            output = "00:00"
            with open(OUTPUT_FILE, "w") as f:
                    f.write(output)
            print("\r" + output, end="", flush=True)
            break

        else:
                # Normales Format mm:ss
            mins = int(remaining // 60)
            secs = int(remaining % 60)
            output = f"{mins:02}:{secs:02}"
            time.sleep(1 - (time.perf_counter() % 1))  # auf volle Sekunde warten

            # In Datei schreiben
            with open(OUTPUT_FILE, "w") as f:
                f.write(output)

            # In Konsole anzeigen
            print("\r" + output, end="", flush=True)

def count(): 
    MainVar = 0
    while True:
        with open(OUTPUT_FILE, "w") as f:
                f.write(str(MainVar))

        user_input = input("+1?")
        if user_input == "y":
            
            MainVar = MainVar + 1
            print("\r" + str(MainVar), end="", flush=True)

        if user_input == "N" or user_input == "n" or user_input == "No" or user_input == "no":
            with open(OUTPUT_FILE, "w") as f:
                f.write("0")
            print(0)
            Counter = 0
        
        if user_input == "No" or user_input == "no" or user_input == "Nah" or user_input == "nah":
            exit()


# === Startzeit abfragen ===
user_input = input("Startzeit eingeben (mm:ss oder nur Sekunden) oder y/n/no für Counter: ").strip()



if ":" in user_input:
    mins, secs = map(int, user_input.split(":"))
    total_time = mins * 60 + secs
    countdown()

elif "y" in user_input or "n" in user_input or "o" in user_input:
     count()
else:
   total_time = int(user_input)
   countdown() 






