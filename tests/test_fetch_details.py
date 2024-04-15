import serverjars

details = serverjars.fetch_details(
    type="vanilla", category="snapshot", version="1.20.3"
)
print(details)
