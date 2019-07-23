'''
Simple matplotlib backend showing how to display data directly in Eclipse EASE.

:author: Martin Kloesch <martin@kmh-solutions.com>
'''
import tempfile
import threading
from matplotlib.backends import backend_agg
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.backend_bases import ShowBase
from matplotlib.figure import Figure


class EventTimedShow(ShowBase):
    '''
    Custom matplotlib :class:`Show` waiting for notification about being
    shut down.
    '''
    #: Simple event to wait for window to be closed.
    show_stopper: threading.Event = threading.Event()

    @classmethod
    def mainloop(cls, block: bool=None):
        '''
        Main loop just waiting for window to be closed.

        :param block: Flag to signalize if call should block until view
                      has been closed. `None` means block.
        '''
        # Block until event is set
        if block is None or bool(block):
            cls.show_stopper.wait()

        # Reset event just to be sure
        cls.show_stopper.clear()


class FileOpener:
    '''
    java.lang.Runnable to display a given image using eclipse functionality.

    Opens image and sets callbacks for close event.
    '''
    def __init__(self, filename: str):
        '''
        Constructor only stores file to be opened.

        :param filename: File to be opened in Eclipse.
        '''
        self._filename = filename

    def run(self):
        '''
        Actually open the file in Eclipse.

        No Exception handling is performed here and all exceptions will
        be propagated to Java.
        '''
        # Get handle to local file
        filestore = org.eclipse.core.filesystem.EFS.getLocalFileSystem().getStore(java.io.File(self._filename).toURI())

        # Get current UI page and open editor
        page = org.eclipse.ui.PlatformUI.getWorkbench().getActiveWorkbenchWindow().getActivePage()
        editor = org.eclipse.ui.ide.IDE.openEditorOnFileStore(page, filestore)

        # TODO: Do something like page.addPartListener(CloseListener(self._filename)) for async shutdown here
        #       For now just stop EventTimedShow to continue with execution
        EventTimedShow.show_stopper.set()

    class Java:
        implements = ['java.lang.Runnable']


class FigureManagerEase(FigureManagerBase):
    '''
    Custom `FigureManager` for displaying matplotlib figures in Eclipse.
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor only passes data to parent constructor.
        '''
        super().__init__(*args, **kwargs)

    def destroy(self, *args):
        '''
        Close blocking call to :func:`EventTimedShow.mainloop` just to be sure.
        '''
        EventTimedShow.show_stopper.set()

    def show(self):
        '''
        Uses `self.canvas` to create a temporary file and starts Eclipse
        job to open it in view.
        '''
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            tmp_file = f.name
        self.canvas.figure.savefig(fname=tmp_file)
        org.eclipse.swt.widgets.Display.getDefault().asyncExec(FileOpener(tmp_file))


def new_figure_manager(num: int, *args, **kwargs) -> FigureManagerBase:
    '''
    Creates a new figure manager instance.

    :param num: Figure number (ignored)
    :return: New FigureManagerEase for given Figure class.
    '''
    FigureClass = kwargs.pop('FigureClass', Figure)
    thisFig = FigureClass(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig)


def new_figure_manager_given_figure(num: int, figure: Figure) -> FigureManagerBase:
    '''
    Creates new figure manager instance for given figure.

    :param num: Figure number (ignored)
    :param figure: :class:`Figure` to create manager for.
    :return: New FigureManagerEase for given :class:`Figure`
    '''
    canvas = backend_agg.FigureCanvasAgg(figure)
    manager = FigureManagerEase(canvas, num)
    return manager


# Matplotlib backend definiton
backend_version = '0.0.1'
FigureCanvas = backend_agg.FigureCanvasAgg
FigureManager = FigureManagerEase
show = EventTimedShow()
