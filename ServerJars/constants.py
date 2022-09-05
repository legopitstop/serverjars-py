from enum import Enum

class Category(Enum):
    # bedrock
    nukkitx='nukkitx'
    pocketmine='pocketmine'
    # modded
    mohist='mohist'
    forge='forge'
    catserver='catserver'
    fabric='fabric'
    # proxies
    bungeecord='bungeecord'
    velocity='velocity'
    waterfall='waterfall'
    flamecord='flamecord'
    # servers
    bukkit='bukkit'
    paper='paper'
    spigot='spigot'
    purpur='purpur'
    tuinity='tuinity'
    sponge='sponge'
    # vanilla
    snapshot='snapshot'
    vanilla='vanilla'

    def __str__(self):
        return super().__str__().replace('Category.', '')

class Type(Enum):
    bedrock='bedrock'
    modded='modded'
    proxies='proxies'
    servers='servers'
    vanilla='vanilla'

    def __str__(self):
        return super().__str__().replace('Type.', '')

class Stability(Enum):
    stable = 'stable'
    experimental = 'experimental'

    def __str__(self):
        return super().__str__().replace('Stability.', '')
