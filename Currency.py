class Currency:

    # Conversion rate: 1 USD = 100 Geld
    USD_TO_GELD_RATE = 100

    def __init__(self, amount=0, name="Geld"):
        self.amount = float(amount)
        self.name = name

    # Big 3
    def __str__(self):
        return f"{self.amount:.2f} {self.name}"

    def __repr__(self):
        return f"Currency(amount={self.amount}, name='{self.name}')"

    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.amount == other.amount
        return self.amount == other

    # Multiplication
    def __mul__(self, value):
        return Currency(self.amount * value, self.name)

    # Division
    def __truediv__(self, value):
        if value == 0:
            raise ZeroDivisionError("Cannot divide currency by zero.")
        return Currency(self.amount / value, self.name)

    # +=
    def __iadd__(self, other):
        if isinstance(other, Currency):
            self.amount += other.amount
        else:
            self.amount += other
        return self

    # -=
    def __isub__(self, other):
        if isinstance(other, Currency):
            self.amount -= other.amount
        else:
            self.amount -= other
        return self

    # <=
    def __le__(self, other):
        if isinstance(other, Currency):
            return self.amount <= other.amount
        return self.amount <= other

    # >=
    def __ge__(self, other):
        if isinstance(other, Currency):
            return self.amount >= other.amount
        return self.amount >= other

    # int()
    def __int__(self):
        return int(self.amount)

    # float()
    def __float__(self):
        return float(self.amount)

    def convert(self, target):
    
     # Converts between USD and Geld.

        target = target.upper()
        if target == "USD":
            return self.amount / Currency.USD_TO_GELD_RATE

        elif target == "GELD":
            return self.amount * Currency.USD_TO_GELD_RATE
        else:
            raise ValueError("Target must be either 'USD' or 'GELD'.")
        
   # Returns True if object has enough Geld
    def can_afford(self, cost):
        if isinstance(cost, Currency):
            return self.amount >= cost.amount
        return self.amount >= cost
    
   # Adds Geld to the object
    def deposit(self, amount):
        self.amount += amount

   # Removes Geld if balance is positive
    def withdraw(self, amount):
        if amount > self.amount:
            raise ValueError("Not enough Geld.")
        self.amount -= amount