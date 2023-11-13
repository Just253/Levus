# https://github.com/35713N/g4f-check
# License: AGPL-3.0-Star

import sys
import g4f
import threading
import time

def process_provider(pname, results, fastest_provider, text):
    try:
        #print(f"[TRYING]:  {pname}")
        start_time = time.time()
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=getattr(getattr(getattr(sys.modules[__name__], "g4f"), "Provider"), pname),
            messages=[{"role": "user", "content": text}],
        )
        print(f"[RESPONSE - {pname}]: {response[:20]}")
        if (response.strip() == ''):
            raise Exception('Empty result')
        if ('support@chatbase.co' in response):
            raise Exception('ChatBase.co')
        end_time = time.time()
        time_taken = end_time - start_time
        results.append((pname, end_time - start_time))
        #print(f"[WORKING]: {pname}, Time taken: {time_taken:.2f} seconds")
        if time_taken < fastest_provider[1]:
            fastest_provider[0] = pname
            fastest_provider[1] = time_taken
    except Exception as e:
        pass
        #print(f"[BROKEN]:  {pname}, Error: {str(e)}")

providers = g4f.Provider.__all__

results = []
fastest_provider = ["NO WORKING PROVIDERS", 99999]
threads = []
for pname in providers:
    text = "¿Que dia es hoy?"
    thread = threading.Thread(target=process_provider, args=(pname, results, fastest_provider, text))
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

input("Press Enter to continue...")

print("====== WORKING PROVIDERS ======")
for pname, time_taken in results:
    print(f"{pname:<20} {time_taken:.2f}s")

print("====== FASTEST PROVIDER ======")
print(f"{fastest_provider[0]:<20} {fastest_provider[1]:.2f}s")

print(f"====== {len(results)}/{len(providers)} WORKING ======")