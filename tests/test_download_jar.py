import serverjars
import time


def test(type, category):
    start = time.time()
    serverjars.download_jar(type, category, fp=f"downloaded/{ category }.jar")
    print(category, "-", time.time() - start)


test("vanilla", "release")
test("vanilla", "snapshot")
test("modded", "banner")
test("modded", "fabric")
test("modded", "mohist")
