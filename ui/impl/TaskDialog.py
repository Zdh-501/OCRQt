from ui.layout.UI_TaskDialog import TaskDialogUI

class TaskDialog(TaskDialogUI):
    def __init__(self, task_name):
        super().__init__()
        #todo 修改被检查的任务
        self.taskLabel.setText(f"检测任务：{task_name}")
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
