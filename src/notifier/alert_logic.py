class AlertLogic:
    def __init__(self):
        # Tracks the price at which the last notification was sent
        self.last_notified_price = None
        # Indicates if the threshold has been reached at least once
        self.has_reached_threshold = False
        # Tracks the direction of the last notification ('increase' or 'decrease')
        self.last_direction = None

    def evaluate_threshold(self, current_price: float, threshold: float) -> bool:
        """
        Checks if the current price has reached or exceeded the threshold for the first time.
        Sets state variables accordingly. Returns True if threshold is reached or has already been reached.
        Resets state if price drops below threshold.
        """
        if current_price >= threshold and self.has_reached_threshold == False:
            # First time crossing the threshold
            self.has_reached_threshold = True
            self.last_direction = "increase"
            self.last_notified_price = current_price
            return True
        elif self.has_reached_threshold == True:
            # Threshold has already been reached
            return True
        else:
            # Price dropped below threshold, reset state
            self.has_reached_threshold = False
            self.last_direction = None
            self.last_notified_price = None
            return False

    def should_notify_increase(self, current_price: float, threshold: float, step: float) -> bool:
        """
        Determines if a notification should be sent for a price increase after threshold is reached.
        Notifies on every new high after threshold, and handles direction change from decrease to increase.
        """
        if self.last_notified_price is None:
            return False
        if current_price > threshold and self.last_direction == "increase":
            # Notify if price is higher than last notified price
            if current_price > self.last_notified_price:
                self.last_notified_price = current_price
                return True
            else:
                return False
        elif current_price > threshold and self.last_direction == "decrease":
            # Direction changed from decrease to increase
            if current_price > self.last_notified_price:
                self.last_direction = "increase"
                self.last_notified_price = current_price
                return True
            else:
                return False
        else:
            return False

    def should_notify_decrease(self, current_price: float, threshold: float, step: float) -> bool:
        """
        Determines if a notification should be sent for a price decrease after threshold is reached.
        Notifies on every drop of 'step' percent (e.g., 5%) from the last notified price, regardless of threshold.
        Handles direction change from increase to decrease.
        """
        if self.last_notified_price is None or not self.has_reached_threshold:
            return False
        # Calculate percentage drop from last notified price
        percentage_drop = (self.last_notified_price - current_price) / self.last_notified_price
        if percentage_drop >= step:
            self.last_direction = "decrease"
            self.last_notified_price = current_price
            return True
        else:
            return False

    def should_notify(self, current_price: float, threshold: float, step: float) -> bool:
        """
        Main orchestrator: routes to the appropriate notification logic based on last direction.
        Call evaluate_threshold before this to ensure threshold state is up to date.
        """
        if self.last_direction == "increase":
            return self.should_notify_increase(current_price, threshold, step)
        elif self.last_direction == "decrease":
            return self.should_notify_decrease(current_price, threshold, step)
        else:
            return False
