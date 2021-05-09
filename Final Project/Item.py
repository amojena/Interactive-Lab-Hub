class Item:
    def __init__(self, id, filename, stock, daysSinceLastSale):
        self.ID = id
        self.filename = filename
        self.stock = stock
        self.daysSinceLastSale = daysSinceLastSale
    
    def checkConditions(self):
        return self.stock >= 100 or self.daysSinceLastSale >= 14


def GetAllItems():
    filename = "products.txt"
    items = []

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        print(filename)
        id, filename, stock, lastSale = line.split(",")
        lastSale = lastSale.rstrip()
        items.append(Item(id, filename, stock, lastSale))
    