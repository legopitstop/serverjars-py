import serverjars


def test(type, category):
    details = serverjars.fetch_details(type=type, category=category)
    print(category, "-", details.version, "-", details.size)


test("vanilla", "release")
test("vanilla", "snapshot")
test("modded", "banner")
test("modded", "fabric")
test("modded", "mohist")
