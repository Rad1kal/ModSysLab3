import random
import math
from itertools import count
from json import loads

Account = 10000
BasicStore = 80
ShopStore = 0
Time = 0 # текущий день
TimeCount = 10 # количество дней
TransferRate = 150
OptOfferBaseVolume = 40
Max_Demand = 30
MeanDPrice = 100
RentRate = 200
WagesAndTaxes = 500
BasicOptOfferVol = 50
BasicOptOfferPrice = 35
CountLoadsGoods = 40
Truck = 0

while Time <= TimeCount:
    Time += 1

    print(f"--- День {Time} ---")
    print(f"Расчетный счет: {Account}")
    print(f"BasicStore: {BasicStore}")
    print(f"ShopStore: {ShopStore}")

    # Мелкооптовое предложение
    BasicPriceRnd = BasicOptOfferVol * random.uniform(0.7, 1.3)
    AddPriceByTime = (
        BasicOptOfferPrice * 0.03 * Time
        + BasicOptOfferPrice * 0.01 * Time * random.uniform(0, 1)
    )
    OfferOnePrice = AddPriceByTime + BasicPriceRnd
    RndOfferVolume = round(OptOfferBaseVolume * random.uniform(0.75, 1.25))
    print(
        f"Мелкооптовое предложение: \n Объем партии {RndOfferVolume} \n Цена за единицу {OfferOnePrice:.2f}"
    )

    # Расходы
    total_expenses = RentRate + WagesAndTaxes
    print(f"Расходы (аренда и зарплаты): {total_expenses}")

    # Предлагаем пользователю ввести свои данные
    try:
        TransferVol = float(input("Введите объем переноса товара (TransferVol): "))
        TransferDecision_input = input(
            "Принять решение о переносе товара? (TransferDecision) (1 - Да, 0 - Нет): "
        )
        TransferDecision = bool(int(TransferDecision_input))
        OptOfferAcceptDecision_input = input(
            "Принять мелкооптовое предложение? (OptOfferAcceptDecision) (1 - Да, 0 - Нет): "
        )
        OptOfferAcceptDecision = bool(int(OptOfferAcceptDecision_input))
        Ret_Price = float(input("Введите розничную цену (Ret_Price): "))
        STOP_SELL_input = input("Остановить продажи? (STOP_SELL) (1 - Да, 0 - Нет): ")
        STOP_SELL = bool(int(STOP_SELL_input))
    except ValueError:
        print("Неверный ввод. Пожалуйста, введите числовые значения.")
        continue

    # Расчеты
    BasicPriceRnd = BasicOptOfferVol * random.uniform(0.7, 1.3)
    AddPriceByTime = (
        BasicOptOfferPrice * 0.03 * Time
        + BasicOptOfferPrice * 0.01 * Time * random.uniform(0, 1)
    )
    OfferOnePrice = AddPriceByTime + BasicPriceRnd

    # TransferActualVol
    if Account >= TransferRate:
        TransferActualVol = min(BasicStore, TransferVol * TransferDecision)
    else:
        TransferActualVol = 0

    # RndOfferVolume
    RndOfferVolume = round(OptOfferBaseVolume * random.uniform(0.75, 1.25))

    # OfferFullPrice
    OfferFullPrice = OfferOnePrice * RndOfferVolume

    # OfferAcceptPossibility
    if Account >= OfferFullPrice:
        OfferAcceptPossibility = 1
    else:
        OfferAcceptPossibility = 0

    # SmallOptIncom
    SmallOptIncom = OfferAcceptPossibility * OptOfferAcceptDecision * RndOfferVolume

    # Demand
    Demand = round(
        Max_Demand
        * (1 - 1 / (1 + math.exp(-0.05 * (Ret_Price - MeanDPrice))))
    )

    # RND_Demand
    RND_Demand = round(Demand * random.uniform(0.7, 1.2))

    # SoldRet
    if STOP_SELL:
        SoldRet = 0
    else:
        SoldRet = min(RND_Demand, ShopStore)

    if Truck > 0:
        GoodsLoading = 0
        GoodsUnloading = CountLoadsGoods
    else:
        GoodsLoading = CountLoadsGoods
        GoodsUnloading = 0

    Truck += GoodsLoading
    Truck -= GoodsUnloading

    # GoodsTransfer
    GoodsTransfer = math.trunc(TransferActualVol)

    # Обновление BasicStore
    BasicStore += SmallOptIncom
    BasicStore -= GoodsLoading

    # Обновление ShopStore
    ShopStore += GoodsUnloading
    ShopStore -= SoldRet

    # Selling
    Selling = SoldRet

    # Sp_Opt_Value
    if OfferAcceptPossibility * OptOfferAcceptDecision > 0:
        Sp_Opt_Value = OfferFullPrice
    else:
        Sp_Opt_Value = 0

    # Income
    Income = Ret_Price * SoldRet

    # Обновление Account
    Account += Income

    # TransSpend
    if TransferActualVol > 0:
        TransSpend = TransferRate
    else:
        TransSpend = 0

    # DailySpending
    DailySpending = min(RentRate + WagesAndTaxes + Ad_Spend, Account)
    Spend_for_Offer = Sp_Opt_Value

    # Обновление Account
    Account -= TransSpend + DailySpending + Spend_for_Offer

    # Вывод результатов
    print(f"Общие расходы за день: {total_expenses}")
    print(f"Доход от продаж: {Income}")

    # Проверка баланса счета
    if Account <= 0:
        print("Баланс исчерпан. Вы банкрот.")
        break
