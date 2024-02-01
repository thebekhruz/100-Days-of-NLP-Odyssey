class Solution(object):
    def maxProfit(self, prices):
        profit = 0
        valley = float('inf')

        for price in prices:
            if price < valley:
                valley = price  # find the new minimum (valley)
            else:
                # if current price is higher than the valley, calculate potential profit
                profit += price - valley  
                valley = price  # update valley to current price after selling

        return profit





        

        