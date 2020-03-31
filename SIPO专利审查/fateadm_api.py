# coding=utf-8
import os
import sys
import hashlib
import time
import json
import requests

FATEA_PRED_URL = "http://pred.fateadm.com"


def LOG(log):
    # 不需要测试时，注释掉日志就可以了
    print(log)
    log = None


class TmpObj():
    def __init__(self):
        self.value = None


class Rsp():
    def __init__(self):
        self.ret_code = -1
        self.cust_val = 0.0
        self.err_msg = "succ"
        self.pred_rsp = TmpObj()

    def ParseJsonRsp(self, rsp_data):
        if rsp_data is None:
            self.err_msg = "http request failed, get rsp Nil data"
            return
        jrsp = json.loads(rsp_data)
        self.ret_code = int(jrsp["RetCode"])
        self.err_msg = jrsp["ErrMsg"]
        self.request_id = jrsp["RequestId"]
        if self.ret_code == 0:
            rslt_data = jrsp["RspData"]
            if rslt_data is not None and rslt_data != "":
                jrsp_ext = json.loads(rslt_data)
                if "cust_val" in jrsp_ext:
                    data = jrsp_ext["cust_val"]
                    self.cust_val = float(data)
                if "result" in jrsp_ext:
                    data = jrsp_ext["result"]
                    self.pred_rsp.value = data


def CalcSign(pd_id, passwd, timestamp):
    md5 = hashlib.md5()
    md5.update((timestamp + passwd).encode())
    csign = md5.hexdigest()

    md5 = hashlib.md5()
    md5.update((pd_id + timestamp + csign).encode())
    csign = md5.hexdigest()
    return csign


def CalcCardSign(cardid, cardkey, timestamp, passwd):
    md5 = hashlib.md5()
    md5.update(passwd + timestamp + cardid + cardkey)
    return md5.hexdigest()


def HttpRequest(url, body_data, img_data=""):
    rsp = Rsp()
    post_data = body_data
    files = {
        'img_data': ('img_data', img_data)
    }
    header = {
        'User-Agent': 'Mozilla/5.0',
    }
    rsp_data = requests.post(url, post_data, files=files, headers=header)
    rsp.ParseJsonRsp(rsp_data.text)
    return rsp


class FateadmApi():
    # API接口调用类
    # 参数（appID，appKey，pdID，pdKey）
    def __init__(self, app_id, app_key, pd_id, pd_key):
        self.app_id = app_id
        if app_id is None:
            self.app_id = ""
        self.app_key = app_key
        self.pd_id = pd_id
        self.pd_key = pd_key
        self.host = FATEA_PRED_URL

    def SetHost(self, url):
        self.host = url

    #
    # 查询余额
    # 参数：无
    # 返回值：
    #   rsp.ret_code：正常返回0
    #   rsp.cust_val：用户余额
    #   rsp.err_msg：异常时返回异常详情
    #
    def QueryBalc(self):
        tm = str(int(time.time()))
        sign = CalcSign(self.pd_id, self.pd_key, tm)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign
        }
        url = self.host + "/api/custval"
        rsp = HttpRequest(url, param)
        # if rsp.ret_code == 0:
        #     LOG("query succ ret: {} cust_val: {} rsp: {} pred: {}".format(
        #         rsp.ret_code, rsp.cust_val, rsp.err_msg, rsp.pred_rsp.value))
        # else:
        #     LOG("query failed ret: {} err: {}".format(
        #         rsp.ret_code, rsp.err_msg.encode('utf-8')))
        return rsp

    #
    # 查询网络延迟
    # 参数：pred_type:识别类型
    # 返回值：
    #   rsp.ret_code：正常返回0
    #   rsp.err_msg： 异常时返回异常详情
    #
    def QueryTTS(self, pred_type):
        tm = str(int(time.time()))
        sign = CalcSign(self.pd_id, self.pd_key, tm)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign,
            "predict_type": pred_type,
        }
        if self.app_id != "":
            #
            asign = CalcSign(self.app_id, self.app_key, tm)
            param["appid"] = self.app_id
            param["asign"] = asign
        url = self.host + "/api/qcrtt"
        rsp = HttpRequest(url, param)
        # if rsp.ret_code == 0:
        #     LOG("query rtt succ ret: {} request_id: {} err: {}".format(
        #         rsp.ret_code, rsp.request_id, rsp.err_msg))
        # else:
        #     LOG("predict failed ret: {} err: {}".format(
        #         rsp.ret_code, rsp.err_msg.encode('utf-8')))
        return rsp

    #
    # 识别验证码
    # 参数：pred_type:识别类型  img_data:图片的数据
    # 返回值：
    #   rsp.ret_code：正常返回0
    #   rsp.request_id：唯一订单号
    #   rsp.pred_rsp.value：识别结果
    #   rsp.err_msg：异常时返回异常详情
    #
    def Predict(self, pred_type, img_data, head_info=""):
        tm = str(int(time.time()))
        sign = CalcSign(self.pd_id, self.pd_key, tm)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign,
            "predict_type": pred_type,
            "up_type": "mt"
        }
        if head_info is not None or head_info != "":
            param["head_info"] = head_info
        if self.app_id != "":
            #
            asign = CalcSign(self.app_id, self.app_key, tm)
            param["appid"] = self.app_id
            param["asign"] = asign
        url = self.host + "/api/capreg"
        files = img_data
        rsp = HttpRequest(url, param, files)
        # if rsp.ret_code == 0:
        #     LOG("predict succ ret: {} request_id: {} pred: {} err: {}".format(
        #         rsp.ret_code, rsp.request_id, rsp.pred_rsp.value, rsp.err_msg))
        #     # return rsp.pred_rsp.value
        # else:
        #     LOG("predict failed ret: {} err: {}".format(rsp.ret_code, rsp.err_msg))
        #     if rsp.ret_code == 4003:
        #         # lack of money
        #         LOG("打码平台余额不足,请充值!")
        return rsp

    #
    # 从文件进行验证码识别
    # 参数：pred_type;识别类型  file_name:文件名
    # 返回值：
    #   rsp.ret_code：正常返回0
    #   rsp.request_id：唯一订单号
    #   rsp.pred_rsp.value：识别结果
    #   rsp.err_msg：异常时返回异常详情
    #
    def PredictFromFile(self, pred_type, file_name, head_info=""):
        with open(file_name, "rb") as f:
            data = f.read()
        return self.Predict(pred_type, data, head_info=head_info)

    #
    # 识别失败，进行退款请求
    # 参数：request_id：需要退款的订单号
    # 返回值：
    #   rsp.ret_code：正常返回0
    #   rsp.err_msg：异常时返回异常详情
    #
    # 注意:
    #    Predict识别接口，仅在ret_code == 0时才会进行扣款，才需要进行退款请求，否则无需进行退款操作
    # 注意2:
    #   退款仅在正常识别出结果后，无法通过网站验证的情况，请勿非法或者滥用，否则可能进行封号处理
    #
    def Justice(self, request_id):
        if request_id == "":
            #
            return
        tm = str(int(time.time()))
        sign = CalcSign(self.pd_id, self.pd_key, tm)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign,
            "request_id": request_id
        }
        url = self.host + "/api/capjust"
        rsp = HttpRequest(url, param)
        # if rsp.ret_code == 0:
        #     print("justice succ ret: {} request_id: {} pred: {} err: {}".format(
        #         rsp.ret_code, rsp.request_id, rsp.pred_rsp.value, rsp.err_msg))
        # else:
        #     print("justice failed ret: {} err: {}".format(
        #         rsp.ret_code, rsp.err_msg.encode('utf-8')))
        return rsp

    #
    # 充值接口
    # 参数：cardid：充值卡号  cardkey：充值卡签名串
    # 返回值：
    #   rsp.ret_code：正常返回0
    #   rsp.err_msg：异常时返回异常详情
    #
    def Charge(self, cardid, cardkey):
        tm = str(int(time.time()))
        sign = CalcSign(self.pd_id, self.pd_key, tm)
        csign = CalcCardSign(cardid, cardkey, tm, self.pd_key)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign,
            'cardid': cardid,
            'csign': csign
        }
        url = self.host + "/api/charge"
        rsp = HttpRequest(url, param)
        if rsp.ret_code == 0:
            LOG("charge succ ret: {} request_id: {} pred: {} err: {}".format(
                rsp.ret_code, rsp.request_id, rsp.pred_rsp.value, rsp.err_msg))
        else:
            LOG("charge failed ret: {} err: {}".format(
                rsp.ret_code, rsp.err_msg.encode('utf-8')))
        return rsp

    ##
    # 充值，只返回是否成功
    # 参数：cardid：充值卡号  cardkey：充值卡签名串
    # 返回值： 充值成功时返回0
    ##
    def ExtendCharge(self, cardid, cardkey):
        return self.Charge(cardid, cardkey).ret_code

    ##
    # 调用退款，只返回是否成功
    # 参数： request_id：需要退款的订单号
    # 返回值： 退款成功时返回0
    #
    # 注意:
    #    Predict识别接口，仅在ret_code == 0时才会进行扣款，才需要进行退款请求，否则无需进行退款操作
    # 注意2:
    #   退款仅在正常识别出结果后，无法通过网站验证的情况，请勿非法或者滥用，否则可能进行封号处理
    ##
    def JusticeExtend(self, request_id):
        return self.Justice(request_id).ret_code

    ##
    # 查询余额，只返回余额
    # 参数：无
    # 返回值：rsp.cust_val：余额
    ##
    def QueryBalcExtend(self):
        rsp = self.QueryBalc()
        return rsp.cust_val

    ##
    # 从文件识别验证码，只返回识别结果
    # 参数：pred_type;识别类型  file_name:文件名
    # 返回值： rsp.pred_rsp.value：识别的结果
    ##
    def PredictFromFileExtend(self, pred_type, file_name, head_info=""):
        rsp = self.PredictFromFile(pred_type, file_name, head_info)
        return rsp.pred_rsp.value

    ##
    # 识别接口，只返回识别结果
    # 参数：pred_type:识别类型  img_data:图片的数据
    # 返回值： rsp.pred_rsp.value：识别的结果
    ##
    def PredictExtend(self, pred_type, img_data, head_info=""):
        rsp = self.Predict(pred_type, img_data, head_info)
        return rsp.pred_rsp.value


def TestFunc():
    pd_id = "120***"  # 用户中心页可以查询到pd信息
    pd_key = "CclJUE1FsUDtjbJAN2qZbP**********"
    app_id = "320***"  # 开发者分成用的账号，在开发者中心可以查询到
    app_key = "ccciVnxFu0SKiy57nYGXtmv**********"
    # 识别类型，
    # 具体类型可以查看官方网站的价格页选择具体的类型，不清楚类型的，可以咨询客服
    pred_type = "50100"
    api = FateadmApi(app_id, app_key, pd_id, pd_key)
    # 查询余额
    balance = api.QueryBalcExtend()   # 直接返余额
    # api.QueryBalc()

    # 通过文件形式识别：
    file_name = "code.jpg"
    # 多网站类型时，需要增加src_url参数，具体请参考api文档: http://docs.fateadm.com/web/#/1?page_id=6
    result = api.PredictFromFileExtend(pred_type, file_name)   # 直接返回识别结果
    # rsp = api.PredictFromFile(pred_type, file_name)  # 返回详细识别结果
    return result
    # print(rsp)
    '''
    # 如果不是通过文件识别，则调用Predict接口：
    # result 			= api.PredictExtend(pred_type,data)   	# 直接返回识别结果
    rsp             = api.Predict(pred_type,data)				# 返回详细的识别结果
    '''

    just_flag = False
    if just_flag:
        if rsp.ret_code == 0:
            # 识别的结果如果与预期不符，可以调用这个接口将预期不符的订单退款
            # 退款仅在正常识别出结果后，无法通过网站验证的情况，请勿非法或者滥用，否则可能进行封号处理
            api.Justice(rsp.request_id)

    #card_id         = "123"
    #card_key        = "123"
    # 充值
    #api.Charge(card_id, card_key)
    # print("print in testfunc")


if __name__ == "__main__":
    print(TestFunc())
