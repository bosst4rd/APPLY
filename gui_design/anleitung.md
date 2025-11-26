**Verwendung in anderen Tools:**

```python
from expletus_style import *

# Am Anfang:
init_theme()

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(Sizes.WINDOW)
        self.resizable(False, False)
        
        # Header mit Logo + Titel
        create_header(self, "eXpletus APPLY", "v1.0")
        
        # Buttons
        btn_frame = create_button_row(self)
        create_start_button(btn_frame, self.start).pack(side="left", fill="x", expand=True)
        create_exit_button(btn_frame, self.quit).pack(side="right")
```

**Inhalt:**

|Element|Beschreibung|
|---|---|
|`Colors`|GREEN, RED, GRAY, SUCCESS, ERROR, MUTED|
|`Fonts`|TITLE, SUBTITLE, NORMAL, SMALL, LOG|
|`Sizes`|WINDOW (680x480), BUTTON_HEIGHT (40)|
|`Animation`|SPINNER, DOTS|
|`load_logo()`|Lädt Logo mit korrektem Seitenverhältnis|
|`create_header()`|Standard-Header mit Logo + Titel|
|`create_*_button()`|Start (grün), Stop (rot), Exit (grau)|
|`format_progress()`|Winget-Style Fortschrittsanzeige|

**Dateien für andere Tools:**

```
src/expletus_style.py   # Diese Datei kopieren
media/expletus_1.png    # Logo
```