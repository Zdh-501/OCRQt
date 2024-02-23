import requests
from xml.etree import ElementTree as ET
from datetime import datetime , timedelta


class TaskInfo:
    def __init__(self, order_no, batch_no, product_code, product_name, production_line, task_identifier, task_key,
                 material_type, identify_type, identify_number, production_date, expiry_date, equipment_no,
                 is_processed, error_msg):
        self.ORDER_NO = order_no
        self.BATCH_NO = batch_no
        self.PRODUCT_CODE = product_code
        self.PRODUCT_NAME = product_name
        self.PRODUCTION_LINE = production_line
        self.TASK_IDENTIFIER = task_identifier
        self.TASK_KEY = task_key
        self.MATERIAL_TYPE = material_type
        self.IDENTIFY_TYPE = identify_type
        self.IDENTIFY_NUMBER = identify_number
        self.PRODUCTION_DATE = production_date
        self.EXPIRY_DATE = expiry_date
        self.EQUIPMENT_NO = equipment_no
        self.IS_PROCESSED = is_processed
        self.ERROR_MSG = error_msg


# 自定义任务数据
task_info = TaskInfo(
    order_no='O00001',
    batch_no='CY32404',
    product_code='P123456789',
    product_name='复方酮康唑发用洗剂15+0.25毫克50毫升成品（Rx）',
    production_line='Line 9',
    task_identifier=' ',
    task_key=123,
    material_type=10,
    identify_type=20,
    identify_number=10,
    production_date=datetime.now().strftime('%Y/%m/%d'),
    expiry_date=(datetime.now() + timedelta(days=365)).strftime('%Y/%m/%d'),
    equipment_no='E123456789',
    is_processed=1,
    error_msg=''
)


def send_task_info(task_info):
    # 构造XML数据，确保命名空间与服务端设置的tns一致
    tns = 'http://115.236.153.174/taskService'
    data_xml = ET.Element(f'{{{tns}}}receive_task_info')
    task_info_element = ET.SubElement(data_xml, f'{{{tns}}}task_info')

    for attr, value in task_info.__dict__.items():
        # 注意将属性名称转换为服务端接收的形式，通常是驼峰命名
        sub_elem = ET.SubElement(task_info_element, f'{{{tns}}}{attr}')
        sub_elem.text = str(value)

    # 将XML树转换为字符串
    data_xml_str = ET.tostring(data_xml, encoding='unicode')

    # 构建SOAP请求体
    soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:tns="{tns}">
       <soapenv:Header/>
       <soapenv:Body>
          {data_xml_str}
       </soapenv:Body>
    </soapenv:Envelope>"""

    # 服务接口URL，应该匹配您服务的实际地址和端口
    service_url = 'http://192.168.3.45:8000/soap'

    # 设置请求头
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': f'"{tns}/receive_task_info"'  # SOAPAction应与WSDL中的操作匹配
    }
    print(data_xml_str)
    # 发送POST请求
    response = requests.post(service_url, data=soap_body.encode('utf-8'), headers=headers)

    # 打印响应
    print(response.status_code)
    print(response.text)


# 发送任务信息
send_task_info(task_info)