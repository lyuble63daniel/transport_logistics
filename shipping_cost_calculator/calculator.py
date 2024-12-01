class ShippingCostCalculator:
    """
    A library for calculating shipping costs based on weight, distance, 
    and additional charges for priority or fragile items.
    """

    def __init__(self, base_rate=10, weight_rate=5, distance_rate=2):
        """
        Initialize the calculator with base rates.
        :param base_rate: Base rate for shipping
        :param weight_rate: Rate per kilogram
        :param distance_rate: Rate per kilometer
        """
        self.base_rate = base_rate
        self.weight_rate = weight_rate
        self.distance_rate = distance_rate

    def calculate_cost(self, weight, distance, priority=False, fragile=False):
        """
        Calculate the shipping cost.
        :param weight: Weight of the parcel in kilograms
        :param distance: Distance to the destination in kilometers
        :param priority: Boolean for priority shipping
        :param fragile: Boolean for fragile items
        :return: Total shipping cost
        """
        cost = self.base_rate + (self.weight_rate * weight) + (self.distance_rate * distance)

        # Add additional charges
        if priority:
            cost += 20  # Priority shipping charge
        if fragile:
            cost += 15  # Fragile item charge

        return round(cost, 2)
