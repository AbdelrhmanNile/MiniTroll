import PySimpleGUI as sg
from centered_window import MTWindow
from minitroll import MiniTroll
from mt_help import help_screen

ts_scheme = """keys[
// write your keys in here,
]

rules[
// write rules in here,
]"""

menu_def = [["Need Help?", ["Click Here!"]]]


def popup_ts():

    popup_layout = [
        [
            sg.Input(key="load_path"),
            sg.FileBrowse(file_types=(("Trollscript", "*.trollscript"),)),
        ],
        [sg.Push(), sg.Button("Run", size=(10, 1), font="Arial 14")],
    ]
    popup_window = MTWindow(
        title="File Name", layout=popup_layout, icon="Troll.ico", finalize=True
    )
    while True:

        event, values = popup_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return None
        elif event == "Run" and values["load_path"] != "":
            return values["load_path"]


def welcome_screen():

    welcome_layout = [
        [
            sg.Text(
                "MiniTroll Rule-Based Knowledge System",
                size=(40, 1),
                justification="center",
                font="Helvetica 20",
            ),
        ],
        [
            sg.Button("New", size=(10, 1), font="Arial 14"),
            sg.Text(
                "=> Create a New TrollScript",
                size=(40, 1),
                justification="left",
                font="Arial 14",
            ),
        ],
        [
            sg.Button("Edit", size=(10, 1), font="Arial 14"),
            sg.Text(
                "=> Edit an Existing TrollScript",
                size=(40, 1),
                justification="left",
                font="Arial 14",
            ),
        ],
        [
            sg.Button("Run", size=(10, 1), font="Arial 14"),
            sg.Text(
                "=> Run a TrollScript",
                size=(40, 1),
                justification="left",
                font="Arial 14",
            ),
            sg.Push(),
            sg.Button("About", size=(10, 1), font="Arial 14"),
        ],
    ]

    welcome_window = MTWindow(
        title="MiniTroll", layout=welcome_layout, icon="Troll.ico", finalize=True
    )
    return welcome_window


def new_screen():

    new_layout = [
        [sg.Menu(menu_def)],
        [sg.Multiline(ts_scheme, size=(100, 30), enable_events=True, key="textbox")],
        [sg.Text("File Path"), sg.Input(key="save_path"), sg.FolderBrowse()],
        [
            sg.Text("Select the FOLDER to save in"),
            sg.Push(),
            sg.Button("Save", size=(10, 1)),
        ],
    ]

    new_window = MTWindow(
        title="New", layout=new_layout, icon="Troll.ico", finalize=True
    )
    while True:

        event, values = new_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return
        elif event == "Save":
            ts_name = sg.popup_get_text("File Name", "Please enter the file name")
            write_trollscript(values["textbox"], values["save_path"], ts_name)
        elif event == "Click Here!":
            help_screen()


def edit_screen():

    edit_layout = [
        [sg.Text("Path", size=(8, 1))],
        [
            sg.Input(key="load_path", enable_events=True),
            sg.FileBrowse(file_types=(("Trollscript", "*.trollscript"),)),
        ],
        [sg.Multiline(size=(100, 30), enable_events=True, key="editbox")],
        [sg.Push(), sg.Button("Save", size=(10, 1))],
    ]
    edit_window = MTWindow(
        title="Edit", layout=edit_layout, icon="Troll.ico", finalize=True
    )

    while True:

        event, values = edit_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return
        elif event == "load_path":
            ts_load = read_trollscript(values["load_path"])
            edit_window["editbox"].update(ts_load)
        elif event == "Save":
            write_trollscript(
                values["editbox"],
                values["load_path"],
                values["load_path"].split("/")[-1],
            )


def run_popup(key, options: list):
    r_layout = [
        [sg.Text(f"{key}: "), sg.Combo(options, key="run_popup", size=(20, 1))],
        [sg.Push(), sg.Button("Next", size=(10, 1))],
    ]

    rp_window = MTWindow(title=key, layout=r_layout, icon="Troll.ico", finalize=True)
    while True:
        event, values = rp_window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return
        elif event == "Next":
            val = values["run_popup"]
            rp_window.close()
            return val


def run_screen():

    ts = popup_ts()
    mt = MiniTroll()
    if ts == None:
        return
    mt.init(ts)
    rt_v = {"_filler": True}
    ins = ""
    for i, key in enumerate(list(mt.keys.keys())):
        while ins not in mt.hints[key]:
            ins = run_popup(key, mt.hints[key])
            if ins != None:
                rt_v[key] = ins
        ins = ""

    infer_res = mt.run(rt_v)
    for i in infer_res:
        sg.Print(i, do_not_reroute_stdout=False)


def write_trollscript(ts, path, filename):
    if ".trollscript" not in filename:
        filename = f"{filename}.trollscript"
        open_path = f"{path}/{filename}"
    else:
        open_path = path
    with open(open_path, "w") as f:
        f.write(ts)


def read_trollscript(path):
    with open(path, "r") as f:
        return f.read()
