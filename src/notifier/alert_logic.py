class AlertLogic:
    """
    • First alert when price first falls to / below threshold.
    • While price remains below threshold:
        - ⬇ Decrease: send a new alert only after every `step`‑percent further drop.
        - ⬆ Increase: send an alert immediately on any price rise above the last‑notified price.
    • If price climbs back above threshold → full reset.
    """
    def __init__(self):
        self.last_notified_price: float | None = None
        self.has_reached_threshold: bool = False
        self.last_direction: str | None = None      # "decrease" | "increase"

    # ------------------------------------------------------------------ #
    # 1. Threshold crossing / reset
    # ------------------------------------------------------------------ #
    def evaluate_threshold(self, current_price: float, threshold: float) -> bool:
        """
        Returns True when the threshold event is *active* (price is now ≤ threshold
        or has already been below it).  
        Side‑effects:
        • First crossing → set direction='decrease', record current price, mark active.
        • Crossing back above threshold → full reset and return False.
        """
        if current_price <= threshold and not self.has_reached_threshold:
            # ↓ First time below threshold
            self.has_reached_threshold = True
            self.last_direction = "decrease"
            self.last_notified_price = current_price
            return True
        elif self.has_reached_threshold and current_price > threshold:
            # ↑ Came back above threshold → reset
            self.has_reached_threshold = False
            self.last_direction = None
            self.last_notified_price = None
            return False
        else:
            # Still in the same active / inactive state as before
            return self.has_reached_threshold

    # ------------------------------------------------------------------ #
    # 2. Decrease alerts  (step‑percent further drops)
    # ------------------------------------------------------------------ #
    def should_notify_decrease(
        self, current_price: float, threshold: float, step: float
    ) -> bool:
        """
        `step` is a positive fraction (e.g. 0.05 for 5 %).  
        Alert when price has fallen at least `step` further *below the last‑notified price*.
        Handles direction switches from increase → decrease.
        """
        if not self.has_reached_threshold or self.last_notified_price is None:
            return False

        if current_price < threshold:
            drop_pct = (self.last_notified_price - current_price) / self.last_notified_price
            if drop_pct >= step:                   # met step size
                self.last_direction = "decrease"
                self.last_notified_price = current_price
                return True
        return False

    # ------------------------------------------------------------------ #
    # 3. Increase alerts  (immediate on any uptick)
    # ------------------------------------------------------------------ #
    def should_notify_increase(
        self, current_price: float, threshold: float, step: float
    ) -> bool:
        """
        Immediate alert on any rise above `last_notified_price`
        while still below threshold. (`step` arg kept for symmetry / interface;
        it’s ignored here.)
        """
        if not self.has_reached_threshold or self.last_notified_price is None:
            return False

        if current_price > self.last_notified_price:
            self.last_direction = "increase"
            self.last_notified_price = current_price
            return True
        return False

    # ------------------------------------------------------------------ #
    # 4. Router
    # ------------------------------------------------------------------ #
    def should_notify(self, current_price: float, threshold: float, step: float) -> bool:
        """
        Call `evaluate_threshold()` first each tick.  
        Then delegate to the direction‑specific rule set.
        """
        if self.last_direction == "decrease":
            return self.should_notify_decrease(current_price, threshold, step)
        elif self.last_direction == "increase":
            return self.should_notify_increase(current_price, threshold, step)
        return False
