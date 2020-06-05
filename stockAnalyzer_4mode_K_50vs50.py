import sys
import math
#print("Plz give threshold_toBuy4w and threshold_toSell8w")
#print("threshold_toBuy4w:{}, threshold_toSell8w:{}".format(sys.argv[1], sys.argv[2]))

# dates of allocating money
allocMoneyDates0050 = {
    "104/10/26": {
        "money": "2000",
        "stock": "0",
        "ref_stock": "63.9",
    },
    "105/07/28": {
        "money": "850",
        "stock": "0",
        "ref_stock": "68.85",
    },
    "106/02/08": {
        "money": "1700",
        "stock": "0",
        "ref_stock": "71.6",
    },
    "106/07/31": {
        "money": "700",
        "stock": "0",
        "ref_stock": "81.4",
    },
    "107/01/29": {
        "money": "2200",
        "stock": "0",
        "ref_stock": "85.3",
    },
    "107/07/23": {
        "money": "700",
        "stock": "0",
        "ref_stock": "83.95",
    },
    "108/01/22": {
        "money": "2300",
        "stock": "0",
        "ref_stock": "74.2",
    },
    "108/07/19": {
        "money": "700",
        "stock": "0",
        "ref_stock": "82.0",
    },
    "109/01/31": {
        "money": "2900",
        "stock": "0",
        "ref_stock": "89.25",
    },
}

allocMoneyDates006208 = {
    "104/10/29": {
        "money": "840",
        "stock": "0",
        "ref_stock": "36.49",
    },
    "105/08/02": {
        "money": "40",
        "stock": "0",
        "ref_stock": "39.75",
    },
    "106/07/27": {
        "money": "1000",
        "stock": "0",
        "ref_stock": "47.6",
    },
    "106/11/30": {
        "money": "1650",
        "stock": "0",
        "ref_stock": "47.78",
    },
    "107/07/26": {
        "money": "650",
        "stock": "0",
        "ref_stock": "48.43",
    },
    "107/11/29": {
        "money": "2000",
        "stock": "0",
        "ref_stock": "42.61",
    },
    "108/07/18": {
        "money": "660",
        "stock": "0",
        "ref_stock": "46.74",
    },
    "108/11/20": {
        "money": "1140",
        "stock": "0",
        "ref_stock": "51.95",
    },
}

class aStock():
    def __init__(self, path, allocMoneyDate, stock_scale, stock_price_with_chg_file):
        self.stock_filePath = path                      # TODO: adjust this
        self.allocMoneyDates = allocMoneyDate           # TODO: adjust this
        self.stock_scale = stock_scale                  # TODO: control to use around 4w to buy each time
        self.stock_price_with_chg_filePath = stock_price_with_chg_file
        self.stockAmount = 0.0      # have no stock at first
        self.buyAmount = 0
        self.sellAmount = 0
        self.buyMoreAmount = 0
        self.sellMoreAmount = 0
        self.notEnoughMoneyAmount = 0
        self.notEnoughStockAmount = 0

        self.sum5 = self.sum4 = self.sum3 = self.sum2 = self.chg5 = self.chg4 = self.chg3 = self.chg2 = self.chg1 = 0.0
        self.sum6 = self.chg6 = 0.0
        self.chg_abs_buy_t = 0.0   # accumulated chg
        self.chg_abs_sell_t = 0.0   # accumulated chg
        self.chg_buy_t = 0.0   # accumulated relative chg
        self.chg_sell_t = 0.0   # accumulated relative chg
        self.pre_day_price = 0.0 # used to calculate the price affected by the allocated money
    def updateSumChg(self, chg):
        self.sum6 = self.sum6 - self.chg6 + chg
        self.sum5 = self.sum5 - self.chg5 + chg
        self.sum4 = self.sum4 - self.chg4 + chg
        self.sum3 = self.sum3 - self.chg3 + chg
        self.sum2 = self.sum2 - self.chg2 + chg
        self.chg6 = self.chg5
        self.chg5 = self.chg4
        self.chg4 = self.chg3
        self.chg3 = self.chg2
        self.chg2 = self.chg1
        self.chg1 = chg  

        if chg > 0:
            self.chg_abs_sell_t += chg
            self.chg_abs_buy_t = 0
        elif chg < 0:
            self.chg_abs_sell_t = 0
            self.chg_abs_buy_t += chg
        #else:
            # do nothing 
    def clearBuySumChg(self, threshold_toBuy4w):
        self.sum5 = self.sum4 = self.sum3 = self.sum2 = self.chg5 = self.chg4 = self.chg3 = self.chg2 = self.chg1 = 0.0
        self.sum6 = self.chg6 = 0.0
        self.chg_abs_buy_t -= threshold_toBuy4w
    def clearSellSumChg(self, threshold_toSell8w):
        self.sum5 = self.sum4 = self.sum3 = self.sum2 = self.chg5 = self.chg4 = self.chg3 = self.chg2 = self.chg1 = 0.0
        self.sum6 = self.chg6 = 0.0
        self.chg_abs_sell_t -= threshold_toSell8w

    def updateBuySellChg_by_analyze_mode(self, analyze_mode):
        if analyze_mode == "abs":   #abs/absBuy_relativeSell/absSell_relativeBuy/relative
            self.chg_buy_t = self.chg_abs_buy_t
            self.chg_sell_t = self.chg_abs_sell_t
        elif analyze_mode == "absBuy_relativeSell":
            self.chg_buy_t = self.chg_abs_buy_t
            #self.chg_sell_t = max(self.sum5, self.sum4, self.sum3, self.sum2, self.chg1)
            self.chg_sell_t = max(self.sum6, self.sum5, self.sum4, self.sum3, self.sum2, self.chg1)
        elif analyze_mode == "absSell_relativeBuy":
            self.chg_buy_t = min(self.sum5, self.sum4, self.sum3, self.sum2, self.chg1)
            self.chg_sell_t = self.chg_abs_sell_t
        elif analyze_mode == "relative":
            self.chg_buy_t = min(self.sum5, self.sum4, self.sum3, self.sum2, self.chg1)
            self.chg_sell_t = max(self.sum5, self.sum4, self.sum3, self.sum2, self.chg1)
        else:
            print("what's this??")
            exit(0)

def computeStockPriceWithChg(stock_filePath, stock_price_with_chg_filePath):
    fp = open(stock_filePath)
    fp_chg = open(stock_price_with_chg_filePath, "w")

    # generate stock chg file
    line = fp.readline().strip()
    date, price_s = line.split()
    while price_s == "--":
        fp_chg.write("{}\t{}\t{}\n".format(date, price_s, "--"))
        line = fp.readline().strip()
        date, price_s = line.split()
    
    pre_day_price = float(price_s)
    line = fp.readline().strip()
    while line:
        date, price_s = line.split()
        while price_s == "--":
            fp_chg.write("{}\t{}\t{}\n".format(date, price_s, "--"))
            line = fp.readline().strip()
            date, price_s = line.split()
        fp_chg.write("{}\t{}\t{}\n".format(date, price_s, 100*(float(price_s) - pre_day_price)/pre_day_price))
        pre_day_price = float(price_s)
        line = fp.readline().strip()

    fp.close()
    fp_chg.close()


moneyLeft = 400000  # I have 60w right now  # TODO: adjust this cost
originMoney = 400000  # I have 60w at first # TODO: adjust this cost
buyingTaxCost = 0.000334                   # TODO: adjust this cost
sellingTaxCost = 0.001334                  # TODO: adjust this cost
toBuyStock_amount = 0.5                      
toSellStock_amount = 1.0                    

threshold_toBuy4w = float(sys.argv[1])     # TODO: adjust this
threshold_toSell8w = float(sys.argv[2])    # TODO: adjust this
investigate_ratio_toSellMore = float(sys.argv[3])   # TODO: adjust this
#investigate_ratio_toBuyMore = float(sys.argv[4])   # TODO: adjust this
toSellMoreStock_amount = float(sys.argv[4])   # TODO: adjust this
#toBuyMoreStock_amount = int(sys.argv[6])   # TODO: adjust this
analyze_mode = sys.argv[5]                   # TODO: adjust this, abs/absBuy_relativeSell/absSell_relativeBuy/relative

managerCost = 0     # TODO: add this cost
managingCost = 0    # TODO: add this cost
moneyInStockRatio = 0.0

stock_0050 = aStock("tsmc_0050.csv", allocMoneyDates0050, 1, "stock_price_with_chg_file_0050")
stock_006208 = aStock("tsmc_006208.csv", allocMoneyDates006208, 2, "stock_price_with_chg_file_006208")

computeStockPriceWithChg(stock_0050.stock_filePath, stock_0050.stock_price_with_chg_filePath)
computeStockPriceWithChg(stock_006208.stock_filePath, stock_006208.stock_price_with_chg_filePath)

# read stock chg file
fp_chg1 = open(stock_0050.stock_price_with_chg_filePath)
fp_chg2 = open(stock_006208.stock_price_with_chg_filePath)
line1 = fp_chg1.readline().strip()
line2 = fp_chg2.readline().strip()
while line1 and line2:
    date, price_s2, chg_s2 = line2.split('\t')
    '''
    while price_s2 == "--":
        line1 = fp_chg1.readline().strip()
        line2 = fp_chg2.readline().strip()
        date, price_s2, chg_s2 = line2.split('\t')
    '''
    date, price_s1, chg_s1 = line1.split('\t')

    price1 = float(price_s1)
    if price_s2 != "--": price2 = float(price_s2)
    chg1 = float(chg_s1)
    if price_s2 != "--": chg2 = float(chg_s2)
    
    
    if date in stock_0050.allocMoneyDates: # at this day, the allocated money would affect stock price, it should be ignored
        #print("stockAmount:{}, moneyLeft:{}, chg:{} ".format(stockAmount, moneyLeft, chg))
        moneyLeft += stock_0050.stockAmount * int(stock_0050.allocMoneyDates[date]["money"])
        stock_0050.stockAmount += stock_0050.stockAmount * (int(stock_0050.allocMoneyDates[date]["stock"])/1000)
        allocatedDeductedChg = (float(stock_0050.allocMoneyDates[date]["ref_stock"]) - stock_0050.pre_day_price) / stock_0050.pre_day_price
        allocatedDeductedChg = allocatedDeductedChg * 100
        chg1 = chg1 - allocatedDeductedChg
        moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
        moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
        #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
        #print("stockAmount:{}, moneyLeft:{}, allocatedDeductedChg:{}, chg:{} ".format(stockAmount, moneyLeft, allocatedDeductedChg, chg))
    if date in stock_006208.allocMoneyDates: # at this day, the allocated money would affect stock price, it should be ignored
        #print("stockAmount:{}, moneyLeft:{}, chg:{} ".format(stockAmount, moneyLeft, chg))
        moneyLeft += stock_006208.stockAmount * int(stock_006208.allocMoneyDates[date]["money"])
        stock_006208.stockAmount += stock_006208.stockAmount * (int(stock_006208.allocMoneyDates[date]["stock"])/1000)
        allocatedDeductedChg = (float(stock_006208.allocMoneyDates[date]["ref_stock"]) - stock_006208.pre_day_price) / stock_006208.pre_day_price
        allocatedDeductedChg = allocatedDeductedChg * 100
        chg2 = chg2 - allocatedDeductedChg
        moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
        moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
        #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
        #print("stockAmount:{}, moneyLeft:{}, allocatedDeductedChg:{}, chg:{} ".format(stockAmount, moneyLeft, allocatedDeductedChg, chg))

    stock_0050.updateSumChg(chg1)
    stock_006208.updateSumChg(chg2)
    
    stock_0050.updateBuySellChg_by_analyze_mode(analyze_mode)
    stock_006208.updateBuySellChg_by_analyze_mode(analyze_mode)

    if stock_0050.chg_buy_t <= threshold_toBuy4w or stock_006208.chg_buy_t <= threshold_toBuy4w:
        stockAmount_add1 = toBuyStock_amount*stock_0050.stock_scale
        stockAmount_add2 = toBuyStock_amount*stock_006208.stock_scale
        price_addCost1 = price1*1000*toBuyStock_amount*stock_0050.stock_scale*(1+buyingTaxCost)
        price_addCost2 = price2*1000*toBuyStock_amount*stock_006208.stock_scale*(1+buyingTaxCost)

        if stock_0050.chg_buy_t <= threshold_toBuy4w and stock_006208.chg_buy_t <= threshold_toBuy4w:
            if stock_0050.chg_buy_t <= stock_006208.chg_buy_t and moneyLeft >= price_addCost1:
                stock_0050.stockAmount += stockAmount_add1
                stock_0050.buyAmount += stockAmount_add1
                moneyLeft -= price_addCost1
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Buy 1 stock! Date:{}, stockAmount:{}, buyAmount:{}, moneyLeft:{}".format(date, stockAmount, buyAmount, moneyLeft))
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                stock_0050.clearBuySumChg(threshold_toBuy4w)
                stock_006208.clearBuySumChg(threshold_toBuy4w)
            elif moneyLeft >= price_addCost2:
                stock_006208.stockAmount += stockAmount_add2
                stock_006208.buyAmount += stockAmount_add2
                moneyLeft -= price_addCost2
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Buy 1 stock! Date:{}, stockAmount:{}, buyAmount:{}, moneyLeft:{}".format(date, stockAmount, buyAmount, moneyLeft))
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                stock_0050.clearBuySumChg(threshold_toBuy4w)
                stock_006208.clearBuySumChg(threshold_toBuy4w)
            else:
                stock_0050.notEnoughMoneyAmount += stockAmount_add1
                #print("skip 1 buy. Date:{}, notEnoughMoneyAmount:{}".format(date, notEnoughMoneyAmount))
        else:
            if stock_0050.chg_buy_t <= threshold_toBuy4w and moneyLeft >= price_addCost1:
                stock_0050.stockAmount += stockAmount_add1
                stock_0050.buyAmount += stockAmount_add1
                moneyLeft -= price_addCost1
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Buy 1 stock! Date:{}, stockAmount:{}, buyAmount:{}, moneyLeft:{}".format(date, stockAmount, buyAmount, moneyLeft))
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                stock_0050.clearBuySumChg(threshold_toBuy4w)
                stock_006208.clearBuySumChg(threshold_toBuy4w)
            elif stock_006208.chg_buy_t <= threshold_toBuy4w and moneyLeft >= price_addCost2:
                stock_006208.stockAmount += stockAmount_add2
                stock_006208.buyAmount += stockAmount_add2
                moneyLeft -= price_addCost2
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Buy 1 stock! Date:{}, stockAmount:{}, buyAmount:{}, moneyLeft:{}".format(date, stockAmount, buyAmount, moneyLeft))
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                stock_0050.clearBuySumChg(threshold_toBuy4w)
                stock_006208.clearBuySumChg(threshold_toBuy4w)
            else:
                stock_0050.notEnoughMoneyAmount += stockAmount_add1
                #print("skip 1 buy. Date:{}, notEnoughMoneyAmount:{}".format(date, notEnoughMoneyAmount))
    elif stock_0050.chg_sell_t >= threshold_toSell8w or stock_006208.chg_sell_t >= threshold_toSell8w:
        stockAmount_sub1 = toSellStock_amount*stock_0050.stock_scale
        stockAmount_sub2 = toSellStock_amount*stock_006208.stock_scale
        if stock_0050.chg_sell_t >= threshold_toSell8w and stock_006208.chg_sell_t >= threshold_toSell8w:
            if (moneyInStockRatio >= investigate_ratio_toSellMore):    # sell more (more)
                stockAmount_more_sub1 = stock_0050.stockAmount
                stockAmount_more_sub2 = stock_006208.stockAmount
                priceSubCost1 = price1*1000*stockAmount_more_sub1*(1-sellingTaxCost)
                priceSubCost2 = price2*1000*stockAmount_more_sub2*(1-sellingTaxCost)
                stock_0050.stockAmount -=   stockAmount_more_sub1
                stock_006208.stockAmount -= stockAmount_more_sub2
                stock_0050.sellAmount +=    stockAmount_more_sub1
                stock_006208.sellAmount +=  stockAmount_more_sub2
                stock_0050.sellMoreAmount +=    stockAmount_more_sub1
                stock_006208.sellMoreAmount +=  stockAmount_more_sub2
                moneyLeft += priceSubCost1
                moneyLeft += priceSubCost2
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                #print("sell more! moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Sell 2 stock! Date:{}, stockAmount:{}, sellAmount:{}, moneyLeft:{}".format(date, stockAmount, sellAmount, moneyLeft))
                stock_0050.clearSellSumChg(threshold_toSell8w)
                stock_006208.clearSellSumChg(threshold_toSell8w)
            elif stock_0050.chg_sell_t >=  stock_006208.chg_sell_t and stock_0050.stockAmount >= stockAmount_sub1:
                priceSubCost1 = price1*1000*toSellStock_amount*stock_0050.stock_scale*(1-sellingTaxCost)
                stock_0050.stockAmount -= stockAmount_sub1
                stock_0050.sellAmount += stockAmount_sub1
                moneyLeft += priceSubCost1
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Sell 2 stock! Date:{}, stockAmount:{}, sellAmount:{}, moneyLeft:{}".format(date, stockAmount, sellAmount, moneyLeft))
                stock_0050.clearSellSumChg(threshold_toSell8w)
                stock_006208.clearSellSumChg(threshold_toSell8w)
            elif stock_006208.stockAmount >= stockAmount_sub2:
                priceSubCost2 = price2*1000*toSellStock_amount*stock_006208.stock_scale*(1-sellingTaxCost)
                stock_006208.stockAmount -= stockAmount_sub2
                stock_006208.sellAmount += stockAmount_sub2
                moneyLeft += priceSubCost2
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Sell 2 stock! Date:{}, stockAmount:{}, sellAmount:{}, moneyLeft:{}".format(date, stockAmount, sellAmount, moneyLeft))
                stock_0050.clearSellSumChg(threshold_toSell8w)
                stock_006208.clearSellSumChg(threshold_toSell8w)
            else:
                stock_0050.notEnoughStockAmount += stockAmount_sub1
                #print("skip 2 sell. Date:{}, notEnoughStockAmount:{}".format(date, notEnoughStockAmount))
        else:
            if stock_0050.chg_sell_t >= threshold_toSell8w and stock_0050.stockAmount >= stockAmount_sub1:
                priceSubCost1 = price1*1000*toSellStock_amount*stock_0050.stock_scale*(1-sellingTaxCost)
                stock_0050.stockAmount -= stockAmount_sub1
                stock_0050.sellAmount += stockAmount_sub1
                moneyLeft += priceSubCost1
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Sell 2 stock! Date:{}, stockAmount:{}, sellAmount:{}, moneyLeft:{}".format(date, stockAmount, sellAmount, moneyLeft))
                stock_0050.clearSellSumChg(threshold_toSell8w)
                stock_006208.clearSellSumChg(threshold_toSell8w)
            if stock_006208.chg_sell_t >= threshold_toSell8w and stock_006208.stockAmount >= stockAmount_sub2:
                priceSubCost2 = price2*1000*toSellStock_amount*stock_006208.stock_scale*(1-sellingTaxCost)
                stock_006208.stockAmount -= stockAmount_sub2
                stock_006208.sellAmount += stockAmount_sub2
                moneyLeft += priceSubCost2
                moneyInStock = (stock_0050.stockAmount * price1 + stock_006208.stockAmount * price2) * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Sell 2 stock! Date:{}, stockAmount:{}, sellAmount:{}, moneyLeft:{}".format(date, stockAmount, sellAmount, moneyLeft))
                stock_0050.clearSellSumChg(threshold_toSell8w)
                stock_006208.clearSellSumChg(threshold_toSell8w)
            else:
                stock_0050.notEnoughStockAmount += stockAmount_sub1
                #print("skip 2 sell. Date:{}, notEnoughStockAmount:{}".format(date, notEnoughStockAmount))

    stock_0050.pre_day_price = price1
    stock_006208.pre_day_price = price2
    line1 = fp_chg1.readline().strip()
    line2 = fp_chg2.readline().strip()

# while-loop ended
fp_chg1.close()
fp_chg2.close()

profit = (moneyLeft + (stock_0050.stockAmount * stock_0050.pre_day_price + stock_006208.stockAmount * stock_006208.pre_day_price)*1000*(1-sellingTaxCost) - originMoney)/originMoney
if profit <= 0.7:
    exit(0)
print(" mode:{} threshold_toBuy4w:{} threshold_toSell8w:{}".format(analyze_mode, threshold_toBuy4w, threshold_toSell8w))
print(" investigate_ratio_toSellMore:{} toSellMoreStock_amount:{}".format(investigate_ratio_toSellMore, toSellMoreStock_amount))
#print(" investigate_ratio_toBuyMore:{} toBuyMoreStock_amount:{}".format(investigate_ratio_toBuyMore, toBuyMoreStock_amount*stock_scale))
print("*Total Profit: {}".format(profit))
print(" 0050:\nstockAmount:{}\n sellMoreAmount:{}\n buyAmount:{}\n sellAmount:{}\n notEnoughMoneyAmount:{}\n notEnoughStockAmount:{}".format(stock_0050.stockAmount, stock_0050.sellMoreAmount, stock_0050.buyAmount, stock_0050.sellAmount, stock_0050.notEnoughMoneyAmount, stock_0050.notEnoughStockAmount))
print(" 006208:\nstockAmount:{}\n sellMoreAmount:{}\n buyAmount:{}\n sellAmount:{}\n notEnoughMoneyAmount:{}\n notEnoughStockAmount:{}\n".format(stock_006208.stockAmount, stock_006208.sellMoreAmount, +stock_006208.buyAmount, stock_006208.sellAmount, stock_006208.notEnoughMoneyAmount, stock_006208.notEnoughStockAmount))



'''
fp = open(resultpath, "w")
fp.write(" stockAmount:{}\n moneyLeft:{}\n buyAmount:{}\n sellAmount:{}\n notEnoughMoneyAmount:{}\n notEnoughStockAmount:{}\n".format(stockAmount, moneyLeft, buyAmount, sellAmount, notEnoughMoneyAmount, notEnoughStockAmount))
fp.write("\n with Total Profit: {}%".format(profit))
fp.close()
'''
