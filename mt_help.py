import PySimpleGUI as sg
from centered_window import MTWindow


example_keys = """keys[
leaf color (yellow/white/normal),
leaf shape (wilted/normal),
stem shape (thin/normal),
stem color (red/white/normal),
spikes status (dead/empty/normal),
spikes color (white/normal),
]"""

example_rules = """rules[
if {leaf color}=yellow and {stem shape}=thin and {spikes status}=dead then nitrogen deficiency,
if {leaf shape}=wilted and {stem color}=red and {spikes status}=empty then leaf rust,
if {leaf color}=white and {stem color}=white and {spikes color}=white then powedery mildew,
if {nitrogen deficiency}=true and {leaf rust}=true and {powedery mildew}=true then all are true,
if {nitrogen deficiency}=true&{leaf rust}=true or {powedery mildew}=true then one or more are true,
]"""

example_trollscript = """keys[
leaf color (yellow/white/normal),
leaf shape (wilted/normal),
stem shape (thin/normal),
stem color (red/white/normal),
spikes status (dead/empty/normal),
spikes color (white/normal),
]
rules[
if {leaf color}=yellow and {stem shape}=thin and {spikes status}=dead then nitrogen deficiency,
if {leaf shape}=wilted and {stem color}=red and {spikes status}=empty then leaf rust,
if {leaf color}=white and {stem color}=white and {spikes color}=white then powedery mildew,
if {nitrogen deficiency}=true and {leaf rust}=true and {powedery mildew}=true then all are true,
if {nitrogen deficiency}=true&{leaf rust}=true or {powedery mildew}=true then one or more are true,
]"""


def help_screen():

    help_layout = [
        [
            sg.Text(
                "Although we would like to do",
                justification="left",
                font="Helvetica 10",
            ),
            sg.Text("moderate", justification="left", font="Vivaldi 15"),
            sg.Text(
                "amounts of trolling, we instead decided to help a little bit",
                justification="left",
                font="Helvetica 10",
            ),
            sg.Push(),
            sg.Button("Next", size=(10, 1), font="Arial 14"),
        ],
        [
            sg.Text(
                "Lets start with an example text to extract knowledge from:",
                justification="left",
                font="Helvetica 10",
            )
        ],
        [sg.Image("Example.png")],
    ]
    help_window = MTWindow(
        title="Help", layout=help_layout, icon="Troll.ico", finalize=True
    )
    while True:

        event, values = help_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return None
        elif event == "Next":
            help_screen2()


def help_screen2():

    help_layout = [
        [
            sg.Text(
                "From this text, we can deduce that the diseases causes symptoms such as changing the [[color]] and [[status]] of the plant, these are our keys",
                justification="left",
                font="Helvetica 10",
            ),
            sg.Push(),
            sg.Button("Next", size=(10, 1), font="Arial 14"),
        ],
        [sg.Image("Example.png")],
    ]
    help_window = MTWindow(
        title="Help", layout=help_layout, icon="Troll.ico", finalize=True
    )
    while True:

        event, values = help_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return None
        elif event == "Next":
            help_screen3()


def help_screen3():

    help_layout = [
        [
            sg.Text(
                "From this, defining a key that asks for whats the leaf color looks like this:",
                justification="left",
                font="Helvetica 10",
            )
        ],
        [sg.Text("leaf color (yellow/white/normal),")],
        [
            sg.Text(
                "These would be one of our key with the rest of them looking like this (keeping in mind the syntax):",
                justification="left",
                font="Helvetica 10",
            )
        ],
        [
            sg.Multiline(
                example_keys,
                disabled=True,
                size=(50, 10),
                justification="left",
                font="Helvetica 10",
            ),
            sg.Push(),
            sg.Button("Next", size=(10, 1), font="Arial 14"),
        ],
    ]
    help_window = MTWindow(
        title="Help", layout=help_layout, icon="Troll.ico", finalize=True
    )
    while True:

        event, values = help_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return None
        elif event == "Next":
            help_screen4()


def help_screen4():

    help_layout = [
        [
            sg.Text(
                "Again, from this text, we can deduce the diseases that are caused by the symptoms, these would be part of our rules:",
                justification="left",
                font="Helvetica 10",
            ),
            sg.Push(),
            sg.Button("Next", size=(10, 1), font="Arial 14"),
        ],
        [sg.Image("Example.png")],
    ]
    help_window = MTWindow(
        title="Help", layout=help_layout, icon="Troll.ico", finalize=True
    )
    while True:

        event, values = help_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return None
        elif event == "Next":
            help_screen5()


def help_screen5():

    help_layout = [
        [
            sg.Text(
                'From this, defining a rule that lists which "symptoms" appear on what disease looks like this:',
                justification="left",
                font="Helvetica 10",
            )
        ],
        [
            sg.Text(
                "if {leaf color}=yellow and {stem shape}=thin and {spikes status}=dead then nitrogen deficiency,"
            )
        ],
        [
            sg.Text(
                "These would be one our rules with the rest of them looking like this (keeping in mind the syntax):",
                justification="left",
                font="Helvetica 10",
            )
        ],
        [
            sg.Multiline(
                example_rules,
                disabled=True,
                size=(80, 10),
                justification="left",
                font="Helvetica 10",
            ),
            sg.Push(),
            sg.Button("Next", size=(10, 1), font="Arial 14"),
        ],
    ]
    help_window = MTWindow(
        title="Help", layout=help_layout, icon="Troll.ico", finalize=True
    )
    while True:

        event, values = help_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return None
        elif event == "Next":
            help_screenfinal()


def help_screenfinal():

    help_layout = [
        [sg.Text('Finally, our full "*.trollscript" file should like this:')],
        [
            sg.Multiline(
                example_trollscript,
                disabled=True,
                size=(80, 20),
                justification="left",
                font="Helvetica 10",
            )
        ],
    ]
    help_window = MTWindow(
        title="Help", layout=help_layout, icon="Troll.ico", finalize=True
    )
    while True:

        event, values = help_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return None
