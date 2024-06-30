import serverjars


def test(type, category):
    all = serverjars.fetch_all(type=type, category=category, max=3)
    print(category)
    for jar in all:
        print("-", jar.version)


test("vanilla", "release")
test("vanilla", "snapshot")
test("modded", "banner")
test("modded", "fabric")
test("modded", "mohist")
