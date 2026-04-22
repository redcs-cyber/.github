from datetime import datetime


print("Jarvis aktif // 10x template")
print("Çıkmak için: exit")

while True:
    text = input(">>> ").strip()
    if text.lower() in {"exit", "quit"}:
        print("Jarvis kapanıyor.")
        break

    now = datetime.now().strftime("%H:%M:%S")
    print(f"Jarvis [{now}]: {text}")
