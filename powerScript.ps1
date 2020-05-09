
For($threshold_toBuy500 = -2.3; $threshold_toBuy500 -ge -2.5; $threshold_toBuy500-=0.1){
    Write-Host "threshold_toBuy500: $threshold_toBuy500"
    For($threshold_toSell1000 = 4.9; $threshold_toSell1000 -le 5.1; $threshold_toSell1000+=0.1){
        Write-Host "threshold_toSell1000: $threshold_toSell1000"
        For($investigate_ratio_toSellMore = 0.9; $investigate_ratio_toSellMore -le 1.0; $investigate_ratio_toSellMore+=0.05){
            Write-Host "investigate_ratio_toSellMore: $investigate_ratio_toSellMore"
            #For($investigate_ratio_toBuyMore = -1; $investigate_ratio_toBuyMore -le -1; $investigate_ratio_toBuyMore+=0.1){
                #Write-Host "investigate_ratio_toBuyMore: $investigate_ratio_toBuyMore"
            For($toSellMoreStock_amount = 1.0; $toSellMoreStock_amount -le 1.0; $toSellMoreStock_amount+=0.05){
                Write-Host "toSellMoreStock_amount: $toSellMoreStock_amount"
                #For($toBuyMoreStock_amount = 0; $toBuyMoreStock_amount -le 0; $toBuyMoreStock_amount+=500){
                    #Write-Host "toBuyMoreStock_amount: $toBuyMoreStock_amount"
                python ./stockAnalyzer_4mode_K.py $threshold_toBuy500 $threshold_toSell1000 $investigate_ratio_toSellMore $toSellMoreStock_amount "absBuy_relativeSell" >> result.txt
                    #python ./stockAnalyzer_abs_K.py $threshold_toBuy500 $threshold_toSell1000 $investigate_ratio_toSellMore $toSellMoreStock_amount >> result.txt
                    #python ./stockAnalyzer_relative_K.py $threshold_toBuy500 $threshold_toSell1000 $investigate_ratio_toSellMore $toSellMoreStock_amount >> result.txt
                    #python ./stockAnalyzer_4mode_K.py $threshold_toBuy500 $threshold_toSell1000 $investigate_ratio_toSellMore $investigate_ratio_toBuyMore $toSellMoreStock_amount $toBuyMoreStock_amount "absBuy_relativeSell" >> result.txt
                    #python ./stockAnalyzer_relativeAbs_K.py $threshold_toBuy500 $threshold_toSell1000 $investigate_ratio_toSellMore $toSellMoreStock_amount >> result.txt
                #}
            }
            #}
        }
    }
}