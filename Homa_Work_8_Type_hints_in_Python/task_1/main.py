def calculate_discount(price: float, discount: float) -> float:
    """Calculates the discounted price.
    This function takes an original price and a discount percentage, and returns the price after the discount is applied. Discounts greater than 100% result in a price of 0.
    """
    return 0.0 if discount > 100 else price - price * (discount / 100)


if __name__ == "__main__":
    print(calculate_discount(100, 20))
    print(calculate_discount(50, 110))
