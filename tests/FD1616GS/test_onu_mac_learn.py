#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI
from src.xinertel.unicast66 import *
from src.FD1616GS.mac_learn import *
from src.FD1616GS.ont_auth import *
from src.config.initialization_config import *
import pytest
import allure

import os
import sys

p = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
if p not in sys.path:
    sys.path.append(p)

# @pytest.fixture()
# def ont_mac_learn_suit(login):
#     cdata_info("=========ONU MAC地址上报测试=========")
#     tn = login
#     Vlan_list = [2000]
#     with allure.step('步骤1:发现未注册的ONU。'):
#         assert autofind_onu(tn, Gpon_PonID,  Gpon_OnuID, Gpon_SN)
#     with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
#         assert auth_by_sn(tn ,Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
#     with allure.step("步骤3:配置虚端口vlan2000透传"):
#         assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, Vlan_list)
#     yield tn

@allure.feature("onu mac地址上报测试")
@allure.story("onu mac地址上报测试")
@allure.title("onu mac地址上报测试")
@pytest.mark.run(order=1620)
def test_ont_mac_learn(login):
    '''
    用例描述
    测试目的： 测试onu端口mac地址学习是否正常
    测试步骤：
    步骤1: 发现未注册的ONU
    步骤2: 在OLT上通过Gpon_SN的方式将ONU注册上线
    步骤3: 配置虚端口vlan2000透传
    步骤4: 打流测试,查看onu端口mac地址表
    1）上下行各发送流00:00:00:22:22:21递增5条，在olt上查看onu端口mac地址表
    down_stream_header = (
        'ethernetII_1.sourceMacAdd=00:00:00:11:11:11 vlan_1.id=2000 ethernetII_1.destMacAdd=00:00:00:22:22:21',
        'ethernetII_1.sourceMacAdd=00:00:00:11:11:12 vlan_1.id=2001 ethernetII_1.destMacAdd=00:00:00:22:22:22')
    up_stream_header = (
        'ethernetII_1.sourceMacAdd=00:00:00:22:22:21 vlan_1.id=2000 ethernetII_1.destMacAdd=00:00:00:11:11:11',
        'ethernetII_1.sourceMacAdd=00:00:00:22:22:22 vlan_1.id=2001 ethernetII_1.destMacAdd=00:00:00:11:11:12',)

    预期结果: 上下行正常通，在olt上查看onu端口mac地址表有5条（00:00:00:22:22:21递增5条）
    '''
    renix_info("=========ONU MAC地址上报测试=========")
    cdata_info("=========ONU MAC地址上报测试=========")
    tn = login
    Vlan_list = [2000]
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Gpon_PonID,  Gpon_OnuID, Gpon_SN)
    with allure.step('步骤2:在OLT上通过Gpon_SN的方式将ONU注册上线。'):
        assert auth_by_sn(tn ,Gpon_PonID, Gpon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Gpon_SN)
    with allure.step("步骤3:配置虚端口vlan2000透传"):
        assert add_service_port(tn, Gpon_PonID, Gpon_OnuID, Gemport_ID, Vlan_list)

    with allure.step("步骤4:打流测试,查看onu端口mac地址表"):
        # 清除测试仪的对象，防止影响下个用例的执行
        time.sleep(8)
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()

        # 发流量测试，发送两条流2000+pri2，和vlan2000+pri3
        # port_location = ['//192.168.0.180/1/9', '//192.168.0.180/1/10']
        duration = 10
        down_stream_header = (
            'ethernetII_1.sourceMacAdd=00:00:00:11:11:11 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:22:22:21 ipv4_1.source=192.168.1.11 ipv4_1.destination=192.168.1.21',
            'ethernetII_1.sourceMacAdd=00:00:00:11:11:12 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:22:22:22 ipv4_1.source=192.168.1.12 ipv4_1.destination=192.168.1.22',
            'ethernetII_1.sourceMacAdd=00:00:00:11:11:13 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:22:22:23 ipv4_1.source=192.168.1.13 ipv4_1.destination=192.168.1.23',
            'ethernetII_1.sourceMacAdd=00:00:00:11:11:14 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:22:22:24 ipv4_1.source=192.168.1.14 ipv4_1.destination=192.168.1.24',
            'ethernetII_1.sourceMacAdd=00:00:00:11:11:15 vlan_1.id=2000  ethernetII_1.destMacAdd=00:00:00:22:22:25 ipv4_1.source=192.168.1.15 ipv4_1.destination=192.168.1.25',)

        up_stream_header = (
            'ethernetII_1.sourceMacAdd=00:00:00:22:22:21 vlan_1.id=2000 ethernetII_1.destMacAdd=00:00:00:11:11:11 ipv4_1.source=192.168.1.21 ipv4_1.destination=192.168.1.11',
            'ethernetII_1.sourceMacAdd=00:00:00:22:22:22 vlan_1.id=2000 ethernetII_1.destMacAdd=00:00:00:11:11:12 ipv4_1.source=192.168.1.22 ipv4_1.destination=192.168.1.12',
            'ethernetII_1.sourceMacAdd=00:00:00:22:22:23 vlan_1.id=2000 ethernetII_1.destMacAdd=00:00:00:11:11:13 ipv4_1.source=192.168.1.23 ipv4_1.destination=192.168.1.13',
            'ethernetII_1.sourceMacAdd=00:00:00:22:22:24 vlan_1.id=2000 ethernetII_1.destMacAdd=00:00:00:11:11:14 ipv4_1.source=192.168.1.24 ipv4_1.destination=192.168.1.14',
            'ethernetII_1.sourceMacAdd=00:00:00:22:22:25 vlan_1.id=2000 ethernetII_1.destMacAdd=00:00:00:11:11:15 ipv4_1.source=192.168.1.25 ipv4_1.destination=192.168.1.15',
        )
        # 获取所有流量的统计值
        result_stats = unicast_test(port_location=port_location, down_stream_header=down_stream_header,
                                    up_stream_header=up_stream_header, num=5, dataclassname=PortStats,
                                    duration=duration)

        #判断流上下行接收是否正常
        result_stream  = check_port_static(result_stats[0],result_stats[1])
        #判断olt上是否能查看onu学习的mac地址
        tn = login
        result_show = ont_mac_learn(tn,Gpon_PonID,Gpon_OnuID,Ont_Port_ID)
        result_mac = 'PASS'

        if '00:00:00:22:22:21' in result_show and '00:00:00:22:22:22' in result_show and '00:00:00:22:22:23' in result_show \
                and '00:00:00:22:22:24' in result_show and '00:00:00:22:22:25' in result_show:
            result_mac = 'PASS'
        else:
            result_mac = 'FAIL'

        # for i in range(len(result_show)):
        #     if '00:00:00:22:22:21'==result_show[i]:
        #         continue
        #     elif '00:00:00:22:22:22'==result_show[i]:
        #         continue
        #     elif '00:00:00:22:22:23'==result_show[i]:
        #         continue
        #     elif '00:00:00:22:22:24'==result_show[i]:
        #         continue
        #     elif '00:00:00:22:22:25'==result_show[i]:
        #         continue
        #     else:
        #         result_mac='FAIL'

        if result_mac == 'PASS':
            cdata_error("ONT MAC地址上报:MAC地址学习正常")
        else:
            cdata_error("ONT MAC地址上报:MAC地址学习失败")

        if result_stream == 'PASS':
            cdata_error("ONT MAC地址上报:打流正常")
        else:
            cdata_error("ONT MAC地址上报:打流失败")

        assert result_stream=='PASS' and result_mac =='PASS'


if __name__ == '__main__':
    pytest.main(['-v',"-s",'test_onu_mac_learn.py::test_ont_mac_learn'])



