from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from datetime import datetime
# 将is_valid_date函数定义在类外部
def is_valid_date(date_str):
    """检查日期字符串是否符合YYYY/MM/DD格式，并且是有效的日期。"""
    try:
        datetime.strptime(date_str, "%Y/%m/%d")
        return True
    except ValueError:
        return False
class TaskInfo(ComplexModel):
    # 工单号：字符类型，长度为20，必填
    ORDER_NO = Unicode(max_length=20)
    # 批次号：字符类型，长度为20，必填
    BATCH_NO = Unicode(max_length=20)
    # 产品编码：字符类型，长度为20，必填
    PRODUCT_CODE = Unicode(max_length=20)
    # 产品名称：字符类型，长度为20，必填
    PRODUCT_NAME = Unicode(max_length=20)
    # 生产线：字符类型，长度为20，必填
    PRODUCTION_LINE = Unicode(max_length=20)
    # 识别任务标识符：字符类型，长度为20，必填，格式为操作名+IPC编号
    TASK_IDENTIFIER = Unicode(max_length=20)
    # 识别任务key：整型，必填
    TASK_KEY = Integer
    # 识别物料类型：整型，必填，可能的值为10（内包材）、20（小盒）、30（瓶签）
    MATERIAL_TYPE = Integer
    # 识别类型：整型，必填，可能的值为10（单面）、20（双面）
    IDENTIFY_TYPE = Integer
    # 识别总数：整型，必填
    IDENTIFY_NUMBER = Integer
    # 生产日期：字符类型，必填，格式为YYYY/MM/DD
    PRODUCTION_DATE = Unicode(max_length=20)
    # 有效期至：字符类型，必填，格式为YYYY/MM/DD
    EXPIRY_DATE = Unicode(max_length=20)
    # 识别设备标识符：字符类型，长度为20，必填
    EQUIPMENT_NO = Unicode(max_length=20)
    # 是否已处理：整型，必填，可能的值为1（处理成功）、2（处理失败）
    IS_PROCESSED = Integer
    # 错误消息反馈：字符类型，长度为512，非必填（可为空）
    ERROR_MSG = Unicode(max_length=512, nillable=True)


class taskService(ServiceBase):
    @rpc(TaskInfo, _returns=Unicode)
    def receive_task_info(ctx, task_info):
        # 检查数据有效性
        required_fields = ['ORDER_NO', 'BATCH_NO', 'PRODUCT_CODE', 'PRODUCT_NAME', 'PRODUCTION_LINE', 'TASK_IDENTIFIER', 'TASK_KEY', 'MATERIAL_TYPE', 'IDENTIFY_TYPE', 'IDENTIFY_NUMBER', 'PRODUCTION_DATE', 'EXPIRY_DATE', 'EQUIPMENT_NO', 'IS_PROCESSED']
        for field in required_fields:
            if getattr(task_info, field, None) in [None, '']:
                return f'错误: {field} 是必填项。'

        if not is_valid_date(task_info.PRODUCTION_DATE) or not is_valid_date(task_info.EXPIRY_DATE):
            return '错误: 日期格式不正确，应为YYYY/MM/DD。'

        # 如果数据有效，开始处理任务
        print("Received task: ", task_info)
        # 这里进行任务处理逻辑
        # 假设任务处理成功
        return '任务已成功接收'


# 创建应用
application = Application([taskService],
                          tns='taskService',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# WSGI应用
wsgi_app = WsgiApplication(application)

def run_server():
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()

# 在Web服务器上运行服务
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
