import csv
import os


def save_csv(res_list, csv_file_name):
    L_itemId = []

    path = './csv/'
    # 判断\新建文件夹
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, ' 文件夹创建成功')
    file_name = path+csv_file_name
    # 判断\新建文件
    if not os.path.exists(file_name):
        header = ["dsrDeliver", "dsrDeliverGap", "dsrDescribe", "dsrDescribeGap", "dsrService", "dsrServiceGap", "imgUrl", "ismall",
                  "itemId", "loc", "price", "promoPrice", "redkeys", "sellCount", "sellerPayPostfee", "spGoldMedal", "title", "wangwangId"]
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    # 写入文件
    for item in res_list:
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            L_itemId.append(item["itemId"])
            writer = csv.writer(f)
            L = [item["dsrDeliver"], item["dsrDeliverGap"], item["dsrDescribe"], item["dsrDescribeGap"], item["dsrService"], item["dsrServiceGap"], 'https:'+item["imgUrl"], item["ismall"],
                 item["itemId"], item["loc"], item["price"], item["promoPrice"], item["redkeys"], item["sellCount"], item["sellerPayPostfee"], item["spGoldMedal"], item["title"], item["wangwangId"]]
            writer.writerow(L)

    return L_itemId
