import serverjars

def test(type):
    types = serverjars.fetch_types(type)
    print(types)

test("vanilla")
test("modded")
