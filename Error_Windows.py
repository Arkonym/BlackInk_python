import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton



class ErrorWin(BaseWidget):
    def __init__(self, Err_type= None , message=''):
        #Error.__init__(self)
        super().__init__('ERROR')
        self._ok = ControlButton('OK')
        self._ok.value = self._close
        self._formset= [(' ', '||', str(Err_type), '||', ' '),(str(message)), (' ', '||',  '_ok', '||', ' ')]

    def _close(self):
            close_win(self)

def close_win(win):
    win.close()

if __name__=="__main__":
    pyforms.start_app(ErrorWin, geometry=(100, 200, 200, 100))
