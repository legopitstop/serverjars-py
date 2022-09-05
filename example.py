import ServerJars, os
from ServerJars.constants import Category, Type

LOCAL = os.path.dirname(os.path.realpath(__file__))
# download = ServerJars.downloadJar(Category.vanilla)
# latest = ServerJars.fetchLatest(Category.paper)
# all = ServerJars.fetchAll(Category.paper, 5)
types = ServerJars.fetchTypes()
# types = ServerJars.fetchTypes(Type.bedrock)
# details = fServerJars.etchDetails(Category.paper)
print(types)
