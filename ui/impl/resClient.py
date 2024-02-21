import requests
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta

# 假设这是BES系统期望的任务信息结构
class TaskInfo:
    def __init__(self, task_identifier, task_key, identify_number, order_no, production_date, expiry_date, image, cwid, operation_time):
        self.TASK_IDENTIFIER = task_identifier
        self.TASK_KEY = task_key
        self.IDENTIFY_NUMBER = identify_number
        self.ORDER_NO = order_no
        self.PRODUCTION_DATE = production_date
        self.EXPIRY_DATE = expiry_date
        self.IMAGE = image
        self.CWID = cwid
        self.OPERATIONTIME = operation_time

# 自定义任务数据
task_info = TaskInfo(
    task_identifier='T12345',
    task_key=1,
    identify_number=100,
    order_no='O12345',
    production_date=datetime.now().strftime('%Y-%m-%d'),
    expiry_date=(datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
    image='base64EncodedImageString',
    cwid='CW12345',
    operation_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
)

def send_results_to_bes(task_info):
    # 构建要发送的XML数据
    data_xml = ET.Element('DATA')
    ET.SubElement(data_xml, 'TASK_IDENTIFIER').text = str(task_info.TASK_IDENTIFIER)
    ET.SubElement(data_xml, 'TASK_KEY').text = str(task_info.TASK_KEY)
    ET.SubElement(data_xml, 'SEQUENCE').text = str(task_info.IDENTIFY_NUMBER)
    ET.SubElement(data_xml, 'ORDER_NO').text = task_info.ORDER_NO
    ET.SubElement(data_xml, 'PRODUCTION_DATE').text = task_info.PRODUCTION_DATE
    ET.SubElement(data_xml, 'EXPIRY_DATE').text = task_info.EXPIRY_DATE
    # 假设图片数据和其他信息已经准备好
    ET.SubElement(data_xml, 'IMAGE').text = '图片数据'
    ET.SubElement(data_xml, 'CWID').text = '操作员CWID'
    ET.SubElement(data_xml, 'OPERATIONTIME').text = '操作时间'

    # 将构建的XML转换为字符串，并包装在CDATA标签内
    wrapped_data_xml = f"<![CDATA[{ET.tostring(data_xml, encoding='unicode', method='xml')}]>"
    # 将Element转换为字符串
    data_xml_str = ET.tostring(data_xml, encoding='unicode', method='xml')
    # 包装CDATA，确保不添加XML声明
    wrapped_data_xml = f"<![CDATA[{data_xml_str}]]>"
    # 构建SOAP请求体
    soap_body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                       xmlns:web="http://localhost/BOI/">
       <soapenv:Header/>
       <soapenv:Body>
          <web:synInvoke>
             <web:from>SmartWork@123</web:from>
             <web:token></web:token>
             <web:funcName>IF-EQ-02</web:funcName>
             <web:parameters>{wrapped_data_xml}</web:parameters>
          </web:synInvoke>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    # BES系统的接口地址
    bes_url = 'http://36.250.224.10:8084/SmartWorkESB_KMSC/services/XmlService'

    # 构建请求头部
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': ''  # 如果BES系统没有指定SOAPAction，可以尝试留空
    }

    # 发送POST请求到BES系统
    response = requests.post(bes_url, data=soap_body.encode('utf-8'), headers=headers)

    # 输出响应
    print(response.text)
send_results_to_bes(task_info)