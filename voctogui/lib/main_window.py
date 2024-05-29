import logging
from gi.repository import Gtk

from .helpers import with_ui_path

from .config import Config

from .mixer_panel import MixerPanel
from .info_windows import PortsWindow
from .videopreviews import VideoPreviewsController
from .audiodisplay import AudioDisplay
from .videodisplay import VideoDisplay
from .queues import QueuesWindowController
from .ports import PortsWindowController
from .presetcontroller import PresetController
from .toolbar.mix import MixToolbarController
from .toolbar.preview import PreviewToolbarController
from .toolbar.overlay import OverlayToolbarController
from .toolbar.blinder import BlinderToolbarController
from .toolbar.misc import MiscToolbarController
from .studioclock import StudioClock
from .info_windows import PortsWindow, QueueWindow

from vocto.port import Port

from .image import UiImage # this is loaded here on purpose
# This wrapps GtkImage but with our path-handling. This
# will sadly break graphical editors showing our images,
# but /shrug

@Gtk.Template(filename=with_ui_path('main-window.ui'))
class MainWindow(Gtk.Window):
    __gtype_name__ = "VoctoMainWindow"

    log: logging.Logger
    video_previews: VideoPreviewsController
    mix_audio_display: AudioDisplay
    mix_video_display: VideoDisplay

    output_aspect_ratio: Gtk.AspectFrame = Gtk.Template.Child()
    box_mixer_panel: MixerPanel = Gtk.Template.Child()
    preview_box: Gtk.Box = Gtk.Template.Child()
    video_main: Gtk.DrawingArea = Gtk.Template.Child()

    queue_win: QueueWindow = Gtk.Template.Child()
    ports_win: PortsWindow = Gtk.Template.Child()

    # TODO: Split out
    toolbar_main: Gtk.Toolbar = Gtk.Template.Child()
    close: Gtk.ToolButton = Gtk.Template.Child()
    fullscreen: Gtk.ToggleToolButton = Gtk.Template.Child()
    mute_button: Gtk.ToggleToolButton = Gtk.Template.Child()
    queue_button: Gtk.ToggleToolButton = Gtk.Template.Child()
    ports_button: Gtk.ToggleToolButton = Gtk.Template.Child()

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger('Ui')

        # check for configuration option mainwindow/force_fullscreen
        if Config.getForceFullScreen():
            self.log.info(
                'Forcing main window to full screen by configuration')
            # set window into fullscreen mode
            self.fullscreen()
        else:
            # check for configuration option mainwindow/width and /height
            if Config.getWindowSize():
                # set window size
                self.set_size_request(*Config.getWindowSize())
                self.set_resizable(False)


        # Connect Close-Handler
        self.connect('delete-event', Gtk.main_quit)

        self.output_aspect_ratio.props.ratio = Config.getVideoRatio()
        audio_box = self.box_mixer_panel.audio_box

        # Setup Preview Controller
        self.video_previews = VideoPreviewsController(
            self.preview_box,
            audio_box,
            win=self,
        )
        if Config.getPreviewsEnabled():
            for idx, source in enumerate(Config.getSources()):
                self.video_previews.addPreview(source, Port.SOURCES_PREVIEW + idx)
        elif Config.getMirrorsEnabled():
            for idx, source in enumerate(Config.getMirrorsSources()):
                self.video_previews.addPreview(source, Port.SOURCES_OUT + idx)
        else:
            self.log.warning(
                'Can not show source previews because neither previews nor mirrors are enabled (see previews/enabled and mirrors/enabled in core configuration)')

        self.mix_audio_display = AudioDisplay(audio_box, "mix")

        # Create Main-Video Display
        self.mix_video_display = VideoDisplay(
            self.video_main,
            self.mix_audio_display,
            port=Port.MIX_PREVIEW if Config.getPreviewsEnabled() else Port.MIX_OUT,
            name="MIX"
        )

        for idx, livepreview in enumerate(Config.getLivePreviews()):
            if Config.getPreviewsEnabled():
                self.video_previews.addPreview(
                    '{}-blinded'.format(livepreview), Port.LIVE_PREVIEW + idx, has_volume=False)
            else:
                self.video_previews.addPreview(
                    '{}-blinded'.format(livepreview), Port.LIVE_OUT + idx, has_volume=False)

        self.preview_toolbar_controller = PreviewToolbarController(
            win=self,
        )

        self.preset_controller = PresetController(
            win=self,
            preview_controller=self.preview_toolbar_controller,
        )

        self.overlay_toolbar_controller = OverlayToolbarController(
            win=self,
        )

        self.mix_toolbar_controller = MixToolbarController(
            win=self,
            preview_controller=self.preview_toolbar_controller,
            overlay_controller=self.overlay_toolbar_controller
        )

        self.blinder_toolbar_controller = BlinderToolbarController(
            mixer_panel=self.box_mixer_panel
        )

        self.queues_controller = QueuesWindowController(self.queue_win)
        self.ports_controller = PortsWindowController(self.ports_win)

        self.misc_controller = MiscToolbarController(
            win=self,
            queues_controller=self.queues_controller,
            ports_controller=self.ports_controller,
            video_display=self.mix_video_display
        )

        # Setup Shortcuts window
        self.connect('window-state-event', self.handle_state)

    def handle_state(self, window, event):
        # force full screen if whished by configuration
        if Config.getForceFullScreen():
            self.log.info('re-forcing fullscreen mode')
            self.win.fullscreen()
