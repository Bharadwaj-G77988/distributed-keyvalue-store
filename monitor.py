import time,json

while True:
    try:
        with open("data.json") as f:
            data=json.load(f)
            store=data.get("store",{})
            print("\n====== MONITOR ======")
            print("Total Keys:",len(store))
            print("Keys:",list(store.keys()))
    except:
        print("No data yet")

    time.sleep(5)
