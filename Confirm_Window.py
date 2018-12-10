import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton

class ConfirmWin(BaseWidget):
    def __init__(self, message='', sub_message='', type_flag=''):
        super().__init__('Confirm')
        self._yes = ControlButton('Yes')
        self._yes.value = self._confirm
        self._no = ControlButton('No')
        self._no.value = self._close
        self._formset= [(' ', '||', str(message), '||', ' '),(' ', '||', str(sub_message), '||', ' '),(' ', '||',  '_yes', '||', ' ', '||', '_no', '||', ' ')]

    def _confirm(self):
        if self.parent!=None:
            self.parent._admin_toggle()
        self._close()

    def _close(self):
            close_win(self)

def close_win(win):
    win.close()

if __name__=="__main__":
    pyforms.start_app(ConfirmWin,  geometry=(100, 200, 200, 100))
