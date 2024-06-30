import serverjars


def test(type, category):
    res = serverjars.fetch_jar(type, category)
    print(category, "-", res)


test("vanilla", "release")
test("vanilla", "snapshot")
test("modded", "banner")
test("modded", "fabric")
test("modded", "mohist")
