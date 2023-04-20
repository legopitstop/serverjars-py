import serverjars

def on_finish(jar: serverjars.Jar):
    print('Downloaded', jar)

print('before')
serverjars.downloadJar('snapshot', finishcommand=on_finish)
print('after')