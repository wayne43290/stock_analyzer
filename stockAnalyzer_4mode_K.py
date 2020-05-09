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

allocMoneyDates2884 = {
    "104/07/30": {
        "money": "430",
        "stock": "87",
        "ref_stock": "18.4",
    },
    "105/07/28": {
        "money": "430",
        "stock": "100",
        "ref_stock": "17.7",
    },
    "106/08/09": {
        "money": "490",
        "stock": "74",
        "ref_stock": "17.8",
    },
    "107/07/26": {
        "money": "610",
        "stock": "61",
        "ref_stock": "20.55",
    },
    "108/07/25": {
        "money": "710",
        "stock": "71",
        "ref_stock": "25.55",
    },
}

allocMoneyDates0056 = {
    "104/10/26": {
        "money": "1000",
        "stock": "0",
        "ref_stock": "21.65",
    },
    "105/10/26": {
        "money": "1300",
        "stock": "0",
        "ref_stock": "24.05",
    },
    "106/10/30": {
        "money": "950",
        "stock": "0",
        "ref_stock": "25.44",
    },
    "107/10/23": {
        "money": "1450",
        "stock": "0",
        "ref_stock": "24.36",
    },
    "108/10/23": {
        "money": "1800",
        "stock": "0",
        "ref_stock": "27.23",
    },
}


moneyLeft = 400000  # I have 60w right now  # TODO: adjust this cost
originMoney = 400000  # I have 60w at first # TODO: adjust this cost
buyingTaxCost = 0.000334                   # TODO: adjust this cost
sellingTaxCost = 0.001334                  # TODO: adjust this cost
stock_filePath = 'tsmc_0050.csv'        # TODO: adjust this
allocMoneyDates = allocMoneyDates0050      # TODO: adjust this
stock_scale = 1.0                          # TODO: control to use around 4w to buy each time
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
stock_price_with_chg_filePath = 'stock_price_with_chg'
stockAmount = 0.0      # have no stock at first
moneyInStockRatio = 0.0
buyAmount = 0
sellAmount = 0
buyMoreAmount = 0
sellMoreAmount = 0
notEnoughMoneyAmount = 0
notEnoughStockAmount = 0

sum5 = sum4 = sum3 = sum2 = chg5 = chg4 = chg3 = chg2 = chg1 = 0.0
chg_abs_buy_t = 0.0   # accumulated chg
chg_abs_sell_t = 0.0   # accumulated chg
chg_buy_t = 0.0   # accumulated relative chg
chg_sell_t = 0.0   # accumulated relative chg
pre_day_price = 0.0 # used to calculate the price affected by the allocated money
fp = open(stock_filePath)
fp_chg = open(stock_price_with_chg_filePath, "w")

# generate stock chg file
line = fp.readline().strip()
date, price_s = line.split()
while price_s == "--":
    line = fp.readline().strip()
    date, price_s = line.split()
pre_day_price = float(price_s)
line = fp.readline().strip()
while line:
    date, price_s = line.split()
    while price_s == "--":
        line = fp.readline().strip()
        date, price_s = line.split()
    fp_chg.write("{}\t{}\t{}\n".format(date, price_s, 100*(float(price_s) - pre_day_price)/pre_day_price))
    pre_day_price = float(price_s)
    line = fp.readline().strip()

fp.close()
fp_chg.close()

# read stock chg file
fp_chg = open(stock_price_with_chg_filePath)
line = fp_chg.readline().strip()
while line:
    date, price_s, chg_s = line.split('\t')
    price = float(price_s)
    chg = float(chg_s)
    
    
    if date in allocMoneyDates: # at this day, the allocated money would affect stock price, it should be ignored
        #print("stockAmount:{}, moneyLeft:{}, chg:{} ".format(stockAmount, moneyLeft, chg))
        moneyLeft += stockAmount * int(allocMoneyDates[date]["money"])
        stockAmount += stockAmount * (int(allocMoneyDates[date]["stock"])/1000)
        allocatedDeductedChg = (float(allocMoneyDates[date]["ref_stock"]) - pre_day_price) / pre_day_price
        allocatedDeductedChg = allocatedDeductedChg * 100
        chg = chg - allocatedDeductedChg
        moneyInStock = stockAmount * price * 1000
        moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
        #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
        #print("stockAmount:{}, moneyLeft:{}, allocatedDeductedChg:{}, chg:{} ".format(stockAmount, moneyLeft, allocatedDeductedChg, chg))

    sum5 = sum5 - chg5 + chg
    sum4 = sum4 - chg4 + chg
    sum3 = sum3 - chg3 + chg
    sum2 = sum2 - chg2 + chg
    chg5 = chg4
    chg4 = chg3
    chg3 = chg2
    chg2 = chg1
    chg1 = chg    

    if chg > 0:
        chg_abs_sell_t += chg
        chg_abs_buy_t = 0
    elif chg < 0:
        chg_abs_sell_t = 0
        chg_abs_buy_t += chg
    #else:
        # do nothing

    if analyze_mode == "abs":   #abs/absBuy_relativeSell/absSell_relativeBuy/relative
        chg_buy_t = chg_abs_buy_t
        chg_sell_t = chg_abs_sell_t
    elif analyze_mode == "absBuy_relativeSell":
        chg_buy_t = chg_abs_buy_t
        chg_sell_t = max(sum5, sum4, sum3, sum2, chg1)
    elif analyze_mode == "absSell_relativeBuy":
        chg_buy_t = min(sum5, sum4, sum3, sum2, chg1)
        chg_sell_t = chg_abs_sell_t
    elif analyze_mode == "relative":
        chg_buy_t = min(sum5, sum4, sum3, sum2, chg1)
        chg_sell_t = max(sum5, sum4, sum3, sum2, chg1)
    else:
        print("what's this??")
        exit(0)

    if chg_buy_t <= threshold_toBuy4w:
        '''
        stockAmount_more_add = toBuyMoreStock_amount*stock_scale_divideBy1000
        price_more_addCost = price*toBuyMoreStock_amount*stock_scale*(1+buyingTaxCost)
        if (moneyInStockRatio <= investigate_ratio_toBuyMore) and (moneyLeft >= price_more_addCost):    # buy more (more)
            stockAmount += stockAmount_more_add
            buyAmount += stockAmount_more_add
            buyMoreAmount += stockAmount_more_add
            moneyLeft -= price_more_addCost
            moneyInStock = stockAmount * price * 1000
            moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
            #print("moneyInStockRatio: {}".format(moneyInStockRatio))
            #print("Buy 1 stock! Date:{}, stockAmount:{}, buyAmount:{}, moneyLeft:{}".format(date, stockAmount, buyAmount, moneyLeft))
            chg_abs_buy_t -= threshold_toBuy4w
            sum5 = sum4 = sum3 = sum2 = chg5 = chg4 = chg3 = chg2 = chg1 = 0.0
        else:
        '''
        stockAmount_add = toBuyStock_amount*stock_scale
        price_addCost = price*1000*toBuyStock_amount*stock_scale*(1+buyingTaxCost)
        if moneyLeft >= price_addCost:                                              # buy less (less)
            stockAmount += stockAmount_add
            buyAmount += stockAmount_add
            moneyLeft -= price_addCost
            moneyInStock = stockAmount * price * 1000
            moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
            #print("moneyInStockRatio: {}".format(moneyInStockRatio))
            #print("Buy 1 stock! Date:{}, stockAmount:{}, buyAmount:{}, moneyLeft:{}".format(date, stockAmount, buyAmount, moneyLeft))
            #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
            chg_abs_buy_t -= threshold_toBuy4w
            sum5 = sum4 = sum3 = sum2 = chg5 = chg4 = chg3 = chg2 = chg1 = 0.0
        else:
            notEnoughMoneyAmount += stockAmount_add
            #print("skip 1 buy. Date:{}, notEnoughMoneyAmount:{}".format(date, notEnoughMoneyAmount))
    elif chg_sell_t >= threshold_toSell8w:
        if (moneyInStockRatio >= investigate_ratio_toSellMore):    # sell more (more)
            stockAmount_more_sub = stockAmount
            priceSubCost = price*1000*stockAmount_more_sub*(1-sellingTaxCost)
            stockAmount -= stockAmount_more_sub
            sellAmount += stockAmount_more_sub
            sellMoreAmount += stockAmount_more_sub
            moneyLeft += priceSubCost
            moneyInStock = stockAmount * price * 1000
            moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
            #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
            #print("sell more! moneyInStockRatio: {}".format(moneyInStockRatio))
            #print("Sell 2 stock! Date:{}, stockAmount:{}, sellAmount:{}, moneyLeft:{}".format(date, stockAmount, sellAmount, moneyLeft))
            chg_abs_sell_t -= threshold_toSell8w
            sum5 = sum4 = sum3 = sum2 = chg5 = chg4 = chg3 = chg2 = chg1 = 0.0
        else:
            stockAmount_sub = toSellStock_amount*stock_scale
            if stockAmount >= stockAmount_sub:  # sell normally (less)
                priceSubCost = price*1000*toSellStock_amount*stock_scale*(1-sellingTaxCost)
                stockAmount -= stockAmount_sub
                sellAmount += stockAmount_sub
                moneyLeft += priceSubCost
                moneyInStock = stockAmount * price * 1000
                moneyInStockRatio = moneyInStock/ (moneyLeft + moneyInStock)
                #print("date: {}, moneyInStockRatio: {}".format(date, moneyInStockRatio))
                #print("moneyInStockRatio: {}".format(moneyInStockRatio))
                #print("Sell 2 stock! Date:{}, stockAmount:{}, sellAmount:{}, moneyLeft:{}".format(date, stockAmount, sellAmount, moneyLeft))
                chg_abs_sell_t -= threshold_toSell8w
                sum5 = sum4 = sum3 = sum2 = chg5 = chg4 = chg3 = chg2 = chg1 = 0.0
            else:
                notEnoughStockAmount += stockAmount_sub
                #print("skip 2 sell. Date:{}, notEnoughStockAmount:{}".format(date, notEnoughStockAmount))

    pre_day_price = price
    line = fp_chg.readline().strip()

# while-loop ended
fp_chg.close()

profit = (moneyLeft + stockAmount * pre_day_price*1000*(1-sellingTaxCost) - originMoney)/originMoney
if profit <= 0.5:
    exit(0)
print(" mode:{} threshold_toBuy4w:{} threshold_toSell8w:{}".format(analyze_mode, threshold_toBuy4w, threshold_toSell8w))
print(" investigate_ratio_toSellMore:{} toSellMoreStock_amount:{}".format(investigate_ratio_toSellMore, toSellMoreStock_amount))
#print(" investigate_ratio_toBuyMore:{} toBuyMoreStock_amount:{}".format(investigate_ratio_toBuyMore, toBuyMoreStock_amount*stock_scale))
print("*Total Profit: {}".format(profit))
print(" stockAmount:{}\n sellMoreAmount:{}\n buyAmount:{}\n sellAmount:{}\n notEnoughMoneyAmount:{}\n notEnoughStockAmount:{}\n".format(stockAmount, sellMoreAmount, buyAmount, sellAmount, notEnoughMoneyAmount, notEnoughStockAmount))



'''
fp = open(resultpath, "w")
fp.write(" stockAmount:{}\n moneyLeft:{}\n buyAmount:{}\n sellAmount:{}\n notEnoughMoneyAmount:{}\n notEnoughStockAmount:{}\n".format(stockAmount, moneyLeft, buyAmount, sellAmount, notEnoughMoneyAmount, notEnoughStockAmount))
fp.write("\n with Total Profit: {}%".format(profit))
fp.close()
'''
