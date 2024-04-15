import serverjars
import time

start = time.time()
serverjars.download_jar("vanilla", "vanilla")
print(time.time() - start)
