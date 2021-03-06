import sys
import time
import pytest
from os.path import dirname, abspath

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from src.MA5800_E.internet_type import *
from src.MA5800_E.ont_auth import *
from src.config.initialization_config import *
from src.xinertel.renix_test import *
import allure


@allure.feature("ONU远程管理")
@allure.story("远程管理ONU")
@allure.title("去激活ONU")
@pytest.mark.run(order=15820)
def test_deactive_onu(login):
    '''
    用例描述：
    再OLT上将ONU去激活后，再重新激活。
    例如：
    ont deactivate 1 1
    ont activate 1 1
    '''
    cdata_info("=========去激活ONU=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Epon_PonID, Epon_OnuID, Epon_ONU_MAC)
    with allure.step('步骤2:在OLT上通过MAC认证的方式将ONU注册上线。'):
        assert auth_by_mac(tn, Epon_PonID, Epon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Epon_ONU_MAC)
    with allure.step('步骤3:在OLT配置ONU的service-port。'):
        assert add_service_port(tn, Epon_PonID, Epon_OnuID,[2000])
    with allure.step('步骤4:ONU的以太网口4添加NATIVE-VLAN。'):
        assert ont_native_vlan(tn, Epon_PonID, Epon_OnuID, Ont_Port_ID, User_Vlan)
    with allure.step('步骤5:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)
    with allure.step('步骤6:去激活ONU后，重新激活ONU。'):
        assert deactive_onu(tn, Epon_PonID, Epon_OnuID)
    with allure.step('步骤7:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)


@allure.feature("ONU远程管理")
@allure.story("远程管理ONU")
@allure.title("远程重启ONU")
@pytest.mark.run(order=15821)
def test_reboot_onu(login):
    '''
    用例描述：
    在OLT上远程重启ONU。
    例如：
    ont reboot 1 1
    '''
    cdata_info("=========远程重启ONU=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Epon_PonID, Epon_OnuID, Epon_ONU_MAC)
    with allure.step('步骤2:在OLT上通过MAC认证的方式将ONU注册上线。'):
        assert auth_by_mac(tn, Epon_PonID, Epon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Epon_ONU_MAC)
    with allure.step('步骤3:在OLT配置ONU的service-port'):
        assert add_service_port(tn, Epon_PonID, Epon_OnuID,[2000])
    with allure.step('步骤4:ONU的以太网口4添加NATIVE-VLAN。'):
        assert ont_native_vlan(tn, Epon_PonID, Epon_OnuID, Ont_Port_ID, User_Vlan)
    with allure.step('步骤5:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)
    with allure.step('步骤6:在OLT上远程重启ONU。'):
        assert reboot_onu(tn, Epon_PonID, Epon_OnuID)
    with allure.step('步骤7:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)

@allure.feature("ONU远程管理")
@allure.story("远程管理ONU")
@allure.title("OMCI升级ONU")
# @pytest.mark.skip("暂时不执行")
@pytest.mark.run(order=15801)
def test_upgrade_onu(login):
    '''
    用例描述：
    通过OMCI升级ONU。
    例如：
    load file tftp 192.168.5.100 FD514GB-G_V1.0.1_190909_1158_X000.bin
    ont load select 0/0 1 1
    ont load start 0/0 FD514GB-G_V1.0.1_190909_1158_X000.bin activemode immediate
    '''
    cdata_info("=========OMCI升级ONU=========")
    tn = login
    with allure.step('步骤1:发现未注册的ONU。'):
        assert autofind_onu(tn, Epon_PonID, Epon_OnuID, Epon_ONU_MAC)
    with allure.step('步骤2:在OLT上通过MAC认证的方式将ONU注册上线。'):
        assert auth_by_mac(tn, Epon_PonID, Epon_OnuID, Ont_Lineprofile_ID, Ont_Srvprofile_ID, Epon_ONU_MAC)
    with allure.step('步骤3:在OLT配置ONU的service-port'):
        assert add_service_port(tn, Epon_PonID, Epon_OnuID,[2000])
    with allure.step('步骤4:ONU的以太网口4添加NATIVE-VLAN。'):
        assert ont_native_vlan(tn, Epon_PonID, Epon_OnuID, Ont_Port_ID, User_Vlan)
    with allure.step('步骤5:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)
    with allure.step('步骤6:在OLT上通过OAM升级ONU。'):
        assert upgrade_onu(tn, Epon_PonID, Epon_OnuID, tftp_server_ip, file_name)
    with allure.step('步骤7:测试仪发送双向100000个报文'):
        assert stream_test(stream_rate, stream_num, download_capture_num, port_location)


if __name__ == '__main__':
    # case_1()
    pytest.main(["-v",'-s',"-x","test_onu_mgt.py::test_reboot_onu"])




