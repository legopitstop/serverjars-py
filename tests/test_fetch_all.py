import serverjars

all = serverjars.fetch_all(type="vanilla", category="snapshot", max=10)
print(all)
