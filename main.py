import json, os, sys, subprocess, tkinter as tk
from tkinter import simpledialog, messagebox

TITLE = "G Apps Launcher"
DATA = os.path.join(os.getenv("APPDATA", os.path.expanduser("~")), "GAppsLauncher", "shortcuts.json")
BG, WHITE, TEXT, MUTED, BLUE, BORDER = "#F6F8FC", "#FFFFFF", "#202124", "#5F6368", "#1A73E8", "#E2E6EF"
DEFAULT = [
 ("Gmail","https://mail.google.com","gmail","Work"),
 ("Google Search","https://www.google.com","google","Google"),
 ("YouTube","https://www.youtube.com","youtube","Video"),
 ("Google Calendar","https://calendar.google.com","calendar","Work"),
 ("Google News","https://news.google.com","news","Google"),
 ("Gemini","https://gemini.google.com","gemini","Google"),
 ("Google Drive","https://drive.google.com","drive","Work"),
 ("Google Docs","https://docs.google.com","docs","Work"),
 ("Google Sheets","https://sheets.google.com","sheets","Work"),
 ("Google Slides","https://slides.google.com","slides","Work"),
 ("Google Sites","https://sites.google.com","sites","Work"),
 ("Google Forms","https://forms.google.com","forms","Work"),
 ("Google Maps","https://maps.google.com","maps","Google"),
 ("Google Play","https://play.google.com","play","Google"),
 ("Google Photos","https://photos.google.com","photos","Google"),
 ("Google Translate","https://translate.google.com","translate","Google"),
 ("Google Keep","https://keep.google.com","keep","Work"),
 ("Google Chrome","https://www.google.com/chrome/","chrome","Google"),
 ("Google Meet","https://meet.google.com","meet","Work"),
 ("Google Contacts","https://contacts.google.com","contacts","Work"),
 ("Google Tasks","https://tasks.google.com","tasks","Work"),
 ("Google Chat","https://chat.google.com","chat","Work"),
]
ICON_URLS = {
 "google": "https://www.google.com/favicon.ico",
 "gmail": "https://mail.google.com/favicon.ico",
 "drive": "https://drive.google.com/favicon.ico",
 "youtube": "https://www.youtube.com/favicon.ico",
 "maps": "https://maps.google.com/favicon.ico",
 "calendar": "https://calendar.google.com/favicon.ico",
 "photos": "https://photos.google.com/favicon.ico",
 "meet": "https://meet.google.com/favicon.ico",
 "docs": "https://docs.google.com/favicon.ico",
 "sheets": "https://sheets.google.com/favicon.ico",
 "slides": "https://slides.google.com/favicon.ico",
 "gemini": "https://gemini.google.com/favicon.ico",
 "news": "https://news.google.com/favicon.ico",
 "sites": "https://sites.google.com/favicon.ico",
 "forms": "https://forms.google.com/favicon.ico",
 "play": "https://play.google.com/favicon.ico",
 "translate": "https://translate.google.com/favicon.ico",
 "keep": "https://keep.google.com/favicon.ico",
 "chrome": "https://www.google.com/chrome/static/images/favicons/favicon-96x96.png",
 "contacts": "https://contacts.google.com/favicon.ico",
 "tasks": "https://tasks.google.com/favicon.ico",
 "chat": "https://chat.google.com/favicon.ico",
}
def defaults():
 return [dict(name=n,url=u,icon_key=key,icon=n[:1].upper(),color="#FFFFFF",category=cat) for n,u,key,cat in DEFAULT]

_ICON_CACHE = os.path.join(os.getenv("APPDATA", os.path.expanduser("~")), "GAppsLauncher", "icons")
_ICON_IMAGES = {}
def load_icon(key, url, size=48):
    if key in _ICON_IMAGES:
        return _ICON_IMAGES[key]
    try:
        from PIL import Image, ImageTk
        import urllib.request
        os.makedirs(_ICON_CACHE, exist_ok=True)
        path = os.path.join(_ICON_CACHE, key + ".ico")
        if not os.path.exists(path):
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=6) as response:
                data = response.read()
            with open(path, "wb") as f:
                f.write(data)
        im = Image.open(path).convert("RGBA")
        im.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), (255,255,255,0))
        canvas.alpha_composite(im, ((size-im.width)//2, (size-im.height)//2))
        photo = ImageTk.PhotoImage(canvas)
        _ICON_IMAGES[key] = photo
        return photo
    except Exception:
        return None

def open_webview(name, url):
    import webview
    # Keep one persistent WebView2 profile so website cookies/sign-in sessions can survive app restarts.
    profile_dir = os.path.join(os.getenv("LOCALAPPDATA", os.path.expanduser("~")), "GAppsLauncher", "WebView2Profile")
    os.makedirs(profile_dir, exist_ok=True)
    # Set before WebView2 initializes; this directory persists across launches.
    os.environ["WEBVIEW2_USER_DATA_FOLDER"] = profile_dir
    try:
        webview.create_window(name, url, width=1200, height=800, min_size=(700, 500))
        webview.start(gui="edgechromium", debug=False, private_mode=False, storage_path=profile_dir)
    except TypeError:
        # Compatibility fallback for pywebview versions that do not accept storage_path.
        webview.start(gui="edgechromium", debug=False, private_mode=False)

class Launcher:
 def __init__(self, root):
  self.r=root; root.title(TITLE); root.geometry("900x720"); root.minsize(650,550); root.configure(bg=BG)
  try:
   with open(DATA,encoding="utf-8") as f: self.apps=json.load(f)
  except Exception: self.apps=defaults()
  if not self.apps: self.apps=defaults()
  self.q=tk.StringVar(); self.cat="All apps"
  h=tk.Frame(root,bg=WHITE,height=74,highlightbackground=BORDER,highlightthickness=1); h.pack(fill="x"); h.pack_propagate(False)
  brand=tk.Frame(h,bg=WHITE); brand.pack(side="left",padx=20)
  cv=tk.Canvas(brand,width=38,height=38,bg=WHITE,highlightthickness=0); cv.pack(side="left",pady=17)
  cv.create_oval(2,2,36,36,fill=BLUE,outline=BLUE); cv.create_text(19,19,text="G",fill="white",font=("Segoe UI",19,"bold"))
  tk.Label(brand,text="Apps",bg=WHITE,fg=TEXT,font=("Segoe UI",17,"bold")).pack(side="left",padx=8)
  box=tk.Frame(h,bg="#F1F3F4",highlightbackground=BORDER,highlightthickness=1); box.pack(side="left",fill="x",expand=True,padx=8,pady=16)
  tk.Label(box,text="⌕",bg="#F1F3F4",fg=MUTED,font=("Segoe UI",18)).pack(side="left",padx=8)
  tk.Entry(box,textvariable=self.q,relief="flat",bd=0,bg="#F1F3F4",font=("Segoe UI",11)).pack(side="left",fill="both",expand=True,ipady=8)
  tk.Button(h,text="+ Add app",command=self.add,bg=BLUE,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=12,pady=9).pack(side="right",padx=16)
  tk.Label(root,text="Your apps",bg=BG,fg=TEXT,font=("Segoe UI",22,"bold")).pack(anchor="w",padx=28,pady=(22,0))
  tk.Label(root,text="Open your favorite apps in their own window",bg=BG,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w",padx=29,pady=(4,12))
  tabs=tk.Frame(root,bg=BG); tabs.pack(fill="x",padx=24,pady=(0,10)); self.buttons={}
  for c in ["All apps","Google","Work","Video","Custom"]:
   b=tk.Button(tabs,text=c,command=lambda x=c:self.setcat(x),relief="flat",bd=0,padx=13,pady=7,font=("Segoe UI",9,"bold")); b.pack(side="left",padx=(0,7)); self.buttons[c]=b
  self.count=tk.Label(root,bg=BG,fg=MUTED,font=("Segoe UI",9)); self.count.pack(anchor="w",padx=29)
  outer=tk.Frame(root,bg=BG); outer.pack(fill="both",expand=True,padx=20,pady=12)
  self.can=tk.Canvas(outer,bg=BG,highlightthickness=0); sb=tk.Scrollbar(outer,command=self.can.yview); self.grid=tk.Frame(self.can,bg=BG)
  self.grid.bind("<Configure>",lambda e:self.can.configure(scrollregion=self.can.bbox("all")))
  self.wid=self.can.create_window((0,0),window=self.grid,anchor="nw"); self.can.configure(yscrollcommand=sb.set)
  self.can.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y"); self.can.bind("<Configure>",lambda e:self.can.itemconfigure(self.wid,width=e.width))
  # Enable mouse-wheel scrolling when the pointer is over the app list.
  self.can.bind("<Enter>", self._bind_mousewheel)
  self.can.bind("<Leave>", self._unbind_mousewheel)
  self.grid.bind("<Enter>", self._bind_mousewheel)
  self.grid.bind("<Leave>", self._unbind_mousewheel)
  self.q.trace_add("write",lambda *_:self.render()); self.render()
 def _bind_mousewheel(self, event=None):
  self.r.bind_all("<MouseWheel>", self._on_mousewheel)
  self.r.bind_all("<Button-4>", self._on_mousewheel_linux)
  self.r.bind_all("<Button-5>", self._on_mousewheel_linux)
 def _unbind_mousewheel(self, event=None):
  self.r.unbind_all("<MouseWheel>")
  self.r.unbind_all("<Button-4>")
  self.r.unbind_all("<Button-5>")
 def _on_mousewheel(self, event):
  if event.delta:
   self.can.yview_scroll(int(-event.delta/120), "units")
 def _on_mousewheel_linux(self, event):
  self.can.yview_scroll(-1 if event.num == 4 else 1, "units")
 def save(self):
  os.makedirs(os.path.dirname(DATA),exist_ok=True)
  with open(DATA,"w",encoding="utf-8") as f: json.dump(self.apps,f,ensure_ascii=False,indent=2)
 def setcat(self,c): self.cat=c; self.render()
 def render(self):
  for w in self.grid.winfo_children(): w.destroy()
  for c,b in self.buttons.items():
   active=c==self.cat; b.configure(bg=BLUE if active else BG,fg="white" if active else MUTED)
  q=self.q.get().lower().strip()
  apps=[a for a in self.apps if (self.cat=="All apps" or a.get("category","Custom")==self.cat) and (not q or q in a["name"].lower() or q in a["url"].lower())]
  self.count.configure(text=f"{len(apps)} apps")
  cols=6 if self.can.winfo_width()>850 else 5 if self.can.winfo_width()>700 else 4 if self.can.winfo_width()>520 else 3
  for i,a in enumerate(apps):
   card=tk.Frame(self.grid,bg=WHITE,highlightbackground=BORDER,highlightthickness=1,cursor="hand2",width=120,height=110)
   card.grid(row=i//cols,column=i%cols,padx=7,pady=7,sticky="nsew"); card.grid_propagate(False); self.grid.grid_columnconfigure(i%cols,weight=1,uniform="cards")
   icon=tk.Canvas(card,width=64,height=64,bg=WHITE,highlightthickness=0); icon.pack(pady=(7,2))
   key=a.get("icon_key") or {"Google":"google","Google Search":"google","Gmail":"gmail","Drive":"drive","Google Drive":"drive","YouTube":"youtube","Maps":"maps","Google Maps":"maps","Calendar":"calendar","Google Calendar":"calendar","Photos":"photos","Google Photos":"photos","Meet":"meet","Google Meet":"meet","Docs":"docs","Google Docs":"docs","Sheets":"sheets","Google Sheets":"sheets","Slides":"slides","Google Slides":"slides","Gemini":"gemini","Google News":"news","Google Sites":"sites","Google Forms":"forms","Google Play":"play","Google Translate":"translate","Google Keep":"keep","Google Chrome":"chrome","Google Contacts":"contacts","Google Tasks":"tasks","Google Chat":"chat"}.get(a.get("name",""))
   img=load_icon(key, ICON_URLS.get(key,""), 56) if key and ICON_URLS.get(key) else None
   if img:
    icon.create_image(32,32,image=img)
   else:
    icon.create_oval(7,7,57,57,fill=a.get("color",BLUE),outline=a.get("color",BLUE))
    icon.create_text(32,32,text=a.get("icon",a["name"][:1]),fill="white",font=("Segoe UI",16,"bold"))
   tk.Label(card,text=a["name"],bg=WHITE,fg=TEXT,font=("Segoe UI",8)).pack()
   for w in (card,icon):
    w.bind("<Button-1>",lambda e,x=a:self.open_app(x))
    w.bind("<Button-3>",lambda e,x=a:self.remove(x))
    w.bind("<MouseWheel>", self._on_mousewheel)
   for w in card.winfo_children():
    w.bind("<MouseWheel>", self._on_mousewheel)
 def open_app(self,a):
  try:
   # In a frozen build, launch a second copy of this EXE in a special mode.
   if getattr(sys,"frozen",False):
    cmd=[sys.executable,"--webview-child",a["name"],a["url"]]
   else:
    cmd=[sys.executable,os.path.abspath(__file__),"--webview-child",a["name"],a["url"]]
   subprocess.Popen(cmd,close_fds=True)
  except Exception as e:
   messagebox.showerror("Cannot open app",f"Could not start app window.\n\n{e}",parent=self.r)
 def add(self):
  n=simpledialog.askstring("Add app","App name:",parent=self.r)
  if not n:return
  u=simpledialog.askstring("Add app","Website URL:",parent=self.r)
  if not u:return
  if not u.startswith(("http://","https://")):u="https://"+u
  self.apps.append(dict(name=n.strip(),url=u.strip(),icon=n.strip()[:1].upper(),color="#5F6368",category="Custom"))
  self.save(); self.cat="All apps"; self.render()
 def remove(self,a):
  if messagebox.askyesno("Remove app",f"Remove {a['name']}?",parent=self.r):
   self.apps.remove(a); self.save(); self.render()

if __name__=="__main__":
 if len(sys.argv)>=4 and sys.argv[1]=="--webview-child":
  open_webview(sys.argv[2],sys.argv[3])
 else:
  root=tk.Tk(); Launcher(root); root.mainloop()
