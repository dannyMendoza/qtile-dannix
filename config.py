# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import socket
import subprocess as sp
from qtilescripts.musicplayer import MusicPlayer as mp

from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Screen, ScratchPad, \
        DropDown, KeyChord, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import base
from Xlib import display as xdisplay
from libqtile import extension
from libqtile.command.client import InteractiveCommandClient as qicc
from time import sleep

# [Start] Testing
from qtilescripts.test import multiply as ttm
from libqtile.log_utils import logger
# [End] Testing


## Commented lines from core.py
## /usr/lib/python3.10/site-packages/libqtile/backend/x11/core.py
## logger.exception('Got an exception in getting the window pid')
## Commented lines from __init__.py
## /usr/lib/python3.10/site-packages/xcffib/
## raise ConnectionException(err)

mod = 'mod4'  # Super Key
mod1 = 'mod1' # Alt key

# terminal = guess_terminal()
terminal = 'xterm'
user = os.environ['USER']
hostname = socket.gethostname()

@lazy.function
def change_audio(qtile):
    ''' Switch between HEADPHONES and SPEAKERS '''
    qtile.cmd_spawn(os.path.expanduser('~/.local/bin/switch_audio_sink.py'))

@lazy.function
def change_port_monitor(qtile):
    ''' Change Monitor Port '''
    qtile.cmd_spawn(os.path.expanduser('~/.local/bin/port_monitor.py'))


keys = [
    Key(
        ["mod1"], "k",
        ttm(5,multiplier=50)
    ),
    Key([mod], 'd',
        lazy.run_extension(
            extension.DmenuRun(
            dmenu_prompt='>',
            dmenu_font='Iosevka Term:size=14',
            background='#100e15',
            foreground='#ffd103',
            selected_background='#ffd103',
            selected_foreground='#100e15',
            )  # Only supported by some dmenu forks
            )
        ),
    Key([mod], 'period', lazy.next_screen(),
        desc='Move focus to next monitor'),
    Key([mod], 's', lazy.window.toggle_floating(),
        desc='Toggle floeating screen'),
    Key([mod], 'f', lazy.window.toggle_fullscreen(),
        desc='Toggle fullscreen'),
    Key([mod1], 'Tab', lazy.screen.toggle_group(),
        desc='Move to the last visited group'),
    Key(['control'], 'Return', lazy.group['scratchpad'].dropdown_toggle('term'),
        desc='toggle visibiliy of above defined DropDown named "term"'),
    Key([], 'XF86MonBrightnessUp', lazy.spawn('xbacklight -inc 2'),
        desc='Increase the bright'),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 2'),
        desc='Decrease the bright'),
    Key([mod1], "space", lazy.widget["keyboardlayout"].next_keyboard(),
        desc="Next keyboard layout."),
    Key([mod1, 'control'], 'm', change_port_monitor,
        desc='Change external monitor port DPI/HDMI'),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer set Master 2%+'),
        desc='Increase Volume'),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer set Master 2%-'),
        desc='Decrease Volume'),
    Key([], 'XF86AudioMute', lazy.spawn('amixer set Master toggle'),
        desc='Toggle Volume'),
    Key([mod], 'a', change_audio,
        desc='Switch between Headphones or Speakers'),
    Key([], 'XF86AudioPlay', lazy.spawn(
        'playerctl --player=spotify,firefox,chromium, play-pause'),
        desc='Play or Pause current player'),
    Key([], 'XF86AudioNext', lazy.spawn(
        'playerctl --player=spotify,firefox,chromium next'),
        desc='Next Track'),
    Key([], 'XF86AudioPrev', lazy.spawn(
        'playerctl --player=spotify,firefox,chromium previous'),
        desc='Previous Track'),
    Key([mod], 'j', lazy.layout.down(),
        desc='Move focus down in stack pane'),
    Key([mod], 'k', lazy.layout.up(),
        desc='Move focus up in stack pane'),
    Key([mod], 'h', lazy.layout.left()),
    Key([mod], 'l', lazy.layout.right()),
    Key([mod, 'shift'], 'h', lazy.layout.swap_left()),
    Key([mod, 'shift'], 'l', lazy.layout.swap_right()),
    Key([mod, 'shift'], 'j', lazy.layout.shuffle_down()),
    Key([mod, 'shift'], 'k', lazy.layout.shuffle_up()),
    Key(['control'], 'space', lazy.layout.flip(),
        desc='flip windows'),
    Key([mod], 'Tab', lazy.layout.next(),
        desc='Switch window focus to oither pane(s) of stack'),
    Key([mod], 't', lazy.hide_show_bar(),
        desc='Hide or Show current screen bar'),
    Key([mod, 'shift'], 'space', lazy.layout.rotate(),
        desc='Swap panes of split stack'),
    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'),
    Key([mod], 'Return', lazy.spawn(terminal),
            desc='Launch terminal'),
    Key([mod], 'space', lazy.next_layout(),
            desc='Toggle between layouts'),
    Key([mod], 'q', lazy.window.kill(),
            desc='Kill focused window'),
    Key([mod, 'control'], 'r', lazy.restart(),
            desc='Restart qtile'),
    Key([mod, 'control'], 'q', lazy.shutdown(),
            desc='Shutdown qtile'),
    Key([mod1], 'd', lazy.spawncmd(),
        desc='Spawn a command using a prompt widget'),
    Key([mod, 'control'], 'j', lazy.layout.shrink(), desc='Grow window down'),
    Key([mod, 'control'], 'k', lazy.layout.grow(), desc='Grow window up'),
    Key([mod], 'n', lazy.layout.reset(), desc='Reset all window sizes'),
]

layouts = [
#    layout.TreeTab(
#        place_right=True,
#        bg_color='00000055',
#        panel_width=130,
#        active_fg='000000',
#        active_bg='FCD80D',
#        font='Strong', fontsize=30,
#        section_fontsize=30,
#        section_fg='FCD80D',
#        sections=['DANNY'],
#        previous_on_rm=True,
#        ),
    layout.Max(),
    layout.MonadTall(
        margin=10,
        border_focus='9cdef6',
        border_width=5,
        ),
    layout.MonadWide(
        margin=10,
        border_focus='9cdef6',
        border_width=5,
        new_at_current=False,
        ),
]

# Icon Group List
ig = ['ﲾ','ﳴ','ﱮ','ﴷ','ﰝ','ﮊ']

group_names = [
        (ig[0], {'layout': 'monadtall'}),
        (ig[1], {'layout': 'max'}),
        (ig[2], {'layout': 'monadtall'}),
        (ig[3], {'layout': 'max'}),
        (ig[4], {'layout': 'max'}),
        (ig[5], {'layout': 'max'}),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]
groups.append(
        ScratchPad('scratchpad', [
            # define a drop down terminal.
            DropDown(
                'term',
                'xterm -name FXTerm -fa "Iosevka Term" -fs 12',
                opacity=1.0,
                width=0.8,
                on_focus_lost_hide=True)])
        )

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    keys.append(Key([mod, 'shift'], str(i), lazy.window.togroup(name)))


def get_num_monitors():
    num_monitors = 0
    try:
        display = xdisplay.Display()
        screen = display.screen()
        resources = screen.root.xrandr_get_screen_resources()
        for output in resources.outputs:
            monitor = display.xrandr_get_output_info(output, resources.config_timestamp)
            preferred = False
            if hasattr(monitor, 'preferred'):
                preferred = monitor.preferred
            elif hasattr(monitor, 'num_preferred'):
                preferred = monitor.num_preferred
            if preferred:
                num_monitors += 1
    except Exception as e:
        # always setup at least one monitor
        return 1
    else:
        return num_monitors

num_monitors = get_num_monitors()

widget_defaults = dict(
    font='iMWritingDuoS Nerd Font',
    fontsize='34',
    padding=0,
)

external_monitor = dict(
    font='Iosevka Term Slab Light',
    fontsize=34,
    padding=0,
)

prompt_settings = dict(
    background='1c44aa',
    cursor_color = 'ffffff',
    prompt = f'{user}@{hostname}: ',
    fmt = ' {}',
    bell_style = 'visual',
    visual_bell_color = 'afc1ca',
    ignore_dups_history=True,
)

n_mon = 48 if num_monitors > 1 else 38

systray = widget.Systray(
        # font='NotoSansMono Nerd Font Condensed',
        font='Iosevka Term',
        icon_size=n_mon,
        background='FFFFFF00',
        foreground='000000')

prompt = widget.Prompt(**external_monitor,markup=False,**prompt_settings,) \
        if num_monitors > 1 else widget.Prompt(font='Iosevka',**prompt_settings)

sep = widget.Sep(
        padding=4,
        linewidth=0,
        size_percent=100
        )

#print(mp.get_player_metadata())
#print(mp.MusicPlayer().poll())
#print(mp().record())

def my_func(text):
    '''Used in TaskList to replace certain task names as vim, spotify, etc.'''
    dictionary = {
            ' 👁️‍🗨️ ':f'{user}@{hostname}:~/',
            ' ⛔ /':f'{user}@{hostname}:/',
            ' 🏠 ':f'{user}@{hostname}:~',
            '👨‍🎤Spotify':'Spotify',
            '':'— Mozilla Firefox',
            '\U0001F4DDVIMROOT':'svim',
            '\U0001F4DD ':' - VIM',
            '\U0001F427PACMAN':'pacman',
            }
    for key,value in dictionary.items():
        if value in text:
            text = text.replace(value,key)
    return text

photo = os.path.expanduser('~/Documents/Bash/Screenshot-tool-linux/screenShot')
screenshot = '~/.config/qtile/baricons/retrocamera.png'
screenshot_mousecallbacks={
    'Button1': lambda: qtile.cmd_spawn(
        photo,
        shell=True,
        )
    }

walldict = dict(
    directory = os.path.expanduser('~/Pictures/wallpapers'),
    foreground='05141b',
    background='8a9ea8',
    label='🎨',
    random_selection=True,
)

icon= f'/home/user/.local/share/icons/Papirus/64x64/apps/xfcalendar.svg'

def widgets():
    list_widgets = [

        widget.KeyboardLayout(
            **external_monitor,
            configured_keyboards = ['us','latam'],
            fmt = "  {}",
            ),

        widget.WidgetBox(
            close_button_location='left',
            text_open='',
            text_closed='',
            fontsize=40,
            widgets=[
                widget.LaunchBar(
                        default_icon='/home/danny/.local/share/icons/Newaita-dark/mimetypes/48@2x/application-x-executable.svg',
                        progs=[('firefox','firefox'),
                               ('spotify','spotify'),
                               ('xterm','xterm'),
                               ('system-file-manager','pcmanfm')
                               ],
                        ),
                ],
            ),

        widget.GroupBox(
            padding_x=3,
            borderwidth = 5,
            fontsize = 42,
            highlight_method='line',
            highlight_color = ['27293566'],
            active = 'c0daeb',
            inactive = 'c0daeb',
            other_current_screen_border = '2980B900',
            other_screen_border = '87CEFAaa',
            this_screen_border = '87CEFAaa',
            this_current_screen_border = '2eff89',
            hide_unused=True,
            spacing=0,
            rounded=True,
            ),

        widget.Backlight(
            backlight_name='intel_backlight',
            format='',
        ),

        widget.CurrentScreen(
            **external_monitor,
            active_text='•',
            active_color = '2eff89',
            inactive_text='·'
            ),

        prompt,

        widget.TaskList(
            **external_monitor,
            highlight_method = 'block',
            foreground='000000',
            border = '478B99',
            unfocused_border='475b73',
            borderwidth=0,
            margin_y=2,
            spacing=5,
            rounded=True,
            txt_floating='FL: ',
            txt_maximized='MA: ',
            txt_minimized='MI: ',
            parse_text = my_func,
            ),

        mp(
             font = 'Iosevka Term Slab Light',
             background = '8a9ea8',
             foreground = '000000',
             ),

        widget.Volume(
            **external_monitor,
            emoji=False,
            fmt='{}',
            background = '7499cc',
            foreground = '000000',
            mouse_callbacks={
                'Button3': lambda: qtile.cmd_spawn(
                    os.path.expanduser('~/.local/bin/switch_audio_sink.sh')
                    )
                }
            ),

        widget.Image(
            filename=screenshot,
            mouse_callbacks=screenshot_mousecallbacks,
        ),

        widget.Wallpaper(
            **walldict,
        ),

        widget.Clock(
            **external_monitor,
            background='ebf1f4',
            foreground='000000',
            format='%H:%M',
            # format='%d/%m/%Y %H:%M',
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn(
                    f'notify-send \
                        -i {icon} \
                        -t 10000 -u normal "$(cal -n 1)"',
                    shell=True),
                'Button3': lambda: qtile.cmd_spawn(
                    'pkill dunst',
                    shell=True),
                }
            ),

        systray,

        widget.WidgetBox(
            close_button_location='right',
            text_open='',
            text_closed='',
            foreground='05141b',
            background='FCD80D',
            fontsize=40,
            widgets=[
            widget.TextBox(
                **external_monitor,
                foreground='282a36',
                background='bd93f9',
                text='Exit',
                mouse_callbacks={'Button1':
                    lambda: qtile.cmd_shutdown()},
                ),
            widget.TextBox(
                **external_monitor,
                text='Reboot',
                foreground='282a36',
                background='ff5555',
                mouse_callbacks={'Button1':
                    lambda: qtile.cmd_spawn('reboot')}
                ),
            widget.TextBox(
                **external_monitor,
                text='PowerOff',
                foreground='282a36',
                background='f1fa8c',
                mouse_callbacks={'Button1':
                    lambda: qtile.cmd_spawn('poweroff')}
                ),
            ]
        ),
    ]
    return list_widgets

primary = widgets()
if num_monitors > 1:
    del primary[3]
secondary = widgets()
del secondary[-6]
secondary[-5],secondary[-4] = secondary[-4],secondary[-5]

screens = [
    Screen(
        top=bar.Bar(
            primary,
            48,
            background='27293566',
            margin=[0, 0, 0, 0],
            opacity=1,
        ),
    ),
]

if num_monitors > 1:
    for m in range(num_monitors - 1):
        screens.append(
            Screen(
                top=bar.Bar(
                    secondary,  # second monitor [laptop] 
                    48,
                    background='27293566',
                    margin=[0, 0, 0, 0],
                    opacity=1,
                ),
            )
        )

# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

floating_layout = layout.Floating(
    border_focus = '99b7cb',
    border_width = 6,
    # Run the utility of `xprop` to see the wm class and name of an X client.
    float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='confirm'),
    Match(wm_class='feh'),
    Match(wm_class='xcalc'),
    Match(wm_class='sxiv'),
    Match(wm_class='ocs-url'),
    Match(wm_class='Places'),
    Match(wm_class='Dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='zenity'),
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(title='gtk_calc'),  # Python  GTK calculators
    Match(wm_class='blueman-manager'),
    Match(func=lambda c: bool(c.is_transient_for()))
])

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/qtilescripts/autostart.sh')
    sp.call([home])

@hook.subscribe.client_new
def moveclient(window):
    c = {
            ig[0]:['xterm'],
            ig[1]:['Navigator','Chromium','chromium'],
            ig[2]:['pcmanfm','thunar'],
            ig[3]:['org.pwmt.zathura','Zathura','gimp','Thunderbird'],
            ig[4]:[None,'spotify','Spotify','crx_cinhimbnkkaeohfgghhklpknlkffjgod'], # SPOTIFY = NONE
            ig[5]:['zoom ','Zoom']
        }
    try:
        wclass_name = window.window.get_wm_class()[0]
    except IndexError as e:
        return logger.warning(f'[ERROR]: {e}')
    for k in c.keys():
        if wclass_name in c[k]:
            window.togroup(k,switch_group=True)

###############################################################################
#                          [START] STICKY WINDOW                              #
###############################################################################

sticky = []
history = None
fl_window = []
on_top_windows = (
        'DM Screenshot Tool',
        'Bluetooth File Transfer',
        'SaveImage',
        'Picture-in-Picture', # Static Windows
        'Select Device'
        )

@hook.subscribe.client_new
def floating_winds(window):
    w_name = window.window.get_name() 
    if w_name in on_top_windows:
        if w_name == 'Picture-in-Picture':
            sticky.append(window)
            logger.warning(f'[CLIENT_NEW FLOATING WINDOW]: {window.name} added to S: {sticky}')
            return
        fl_window.append(window)
        logger.warning(f'[CLIENT_NEW FLOATING WINDOW]: {window.name} added to {fl_window}')
        return fl_window

@hook.subscribe.setgroup
def move_to_current_group():
    ''' 
    if you move to different group or Picture-in-Picture window
    lose focus then window will be set as static fo current screen
    '''
    # global history
    # history = qtile.current_group.focus_history
    if sticky:
        for w in sticky:
            if w in fl_window:
                del fl_window[fl_window.index(w)]
            try:
                w.cmd_static()
                logger.warning(f'[SETGROUP STATIC]: {w}')
            except:
                logger.warning(f'[SETGROUP DELETED]: {w}')
                del sticky[sticky.index(w)]
                logger.warning(f'[LENGTH STICKY]: {len(sticky)}')

    if fl_window:
        for w in fl_window:
            w.togroup(qtile.current_group.name)
    # Causing issues while moving from one screen to another
    # zenity.cmd_set_position(900,100)
 
@hook.subscribe.focus_change
def stickywinds():
    if sticky:
        tmp = set(sticky + fl_window)
        for w in tmp:
            w.cmd_bring_to_front()
            logger.warning(f'[FOCUS_CHANGE BTF]: {w}')
        del tmp

@hook.subscribe.float_change
def f_changed():
    if sticky:
        for i in range(len(sticky)):
            try:
                sticky[i].togroup(qtile.current_group.name)
                if sticky[i] not in fl_window:
                    fl_window.append(sticky[i])
            except:
                del sticky[i]
                logger.warning(f'[ERROR] STICKY')

@hook.subscribe.client_killed
def killed(window):
    global fl_window
    if window in fl_window:
        w_index = fl_window.index(window)
        logger.warning(f'[W KILLED]: {window.name} from fl_window list')
        del fl_window[w_index]

# This runs slower that putting code in-place (above)
# @hook.subscribe.focus_change
# def float_windows():
#     sp.Popen(os.path.expanduser('~/.config/qtile/qtilescripts/floating_windows'))

###############################################################################
#                            [END] STICKY WINDOW                              #
###############################################################################

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
cursor_warp = False
bring_front_click = 'floating_only',
auto_fullscreen = True
focus_on_window_activation = 'focus'
reconfigure_screens = True
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'LG3D'
