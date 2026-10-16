import json, os, sys, subprocess, tkinter as tk
from tkinter import simpledialog, messagebox
TITLE="G Apps Launcher"
DATA=os.path.join(os.getenv("APPDATA",os.path.expanduser("~")),"GAppsLauncher","shortcuts.json")
BG="#F6F8FC"; WHITE="#FFFFFF"; TEXT="#202124"; MUTED="#5F6368"; BLUE="#1A73E8"; BORDER="#E2E6EF"
DEFAULT=[
("Google","https://www.google.com","G","#4285F4","Google"),("Gmail","https://mail.google.com","✉","#EA4335","Google"),
("Drive","https://drive.google.com","▲","#0F9D58","Google"),("YouTube","https://www.youtube.com","▶","#FF0033","Video"),
("Maps","https://maps.google.com","⌖","#34A853","Google"),("Calendar","https://calendar.google.com","31","#4285F4","Google"),
("Photos","https://photos.google.com","✿","#FBBC04","Google"),("Meet","https://meet.google.com","●","#00897B","Google"),
("Docs","https://docs.google.com","▧","#4285F4","Work"),("Sheets","https://sheets.google.com","▦","#0F9D58","Work"),
("Slides","https://slides.google.com","▰","#F4B400","Work"),("Gemini","https://gemini.google.com","✦","#8E75FF","Google")]
def defaults(): return [dict(name=n,url=u,icon=i,color=c,category=cat) for n,u,i,c,cat in DEFAULT]

def webview_child(name, url):
    import webview
    webview.create_window(name, url, width=1200, height=800, min_size=(700, 500))
    webview.start(gui="edgechromium", debug=False)

class Launcher:
 def __init__(self,r):
  self.r=r; r.title(TITLE); r.geometry("900x720"); r.minsize(650,550); r.configure(bg=BG)
  try:
   with open(DATA,encoding="utf-8") as f:self.apps=json.load(f)
  except:self.apps=defaults()
  if not self.apps:self.apps=defaults()
  self.q=tk.StringVar(); self.cat="All apps"
  h=tk.Frame(r,bg=WHITE,height=74,highlightbackground=BORDER,highlightthickness=1);h.pack(fill="x");h.pack_propagate(False)
  brand=tk.Frame(h,bg=WHITE);brand.pack(side="left",padx=20)
  cv=tk.Canvas(brand,width=38,height=38,bg=WHITE,highlightthickness=0);cv.pack(side="left",pady=17);cv.create_oval(2,2,36,36,fill=BLUE,outline=BLUE);cv.create_text(19,19,text="G",fill="white",font=("Segoe UI",19,"bold"))
  tk.Label(brand,text="Apps",bg=WHITE,fg=TEXT,font=("Segoe UI",17,"bold")).pack(side="left",padx=8)
  box=tk.Frame(h,bg="#F1F3F4",highlightbackground=BORDER,highlightthickness=1);box.pack(side="left",fill="x",expand=True,padx=8,pady=16)
  tk.Label(box,text="⌕",bg="#F1F3F4",fg=MUTED,font=("Segoe UI",18)).pack(side="left",padx=8)
  tk.Entry(box,textvariable=self.q,relief="flat",bd=0,bg="#F1F3F4",font=("Segoe UI",11)).pack(side="left",fill="both",expand=True,ipady=8)
  tk.Button(h,text="+ Add app",command=self.add,bg=BLUE,fg="white",relief="flat",font=("Segoe UI",10,"bold"),padx=12,pady=9).pack(side="right",padx=16)
  tk.Label(r,text="Your apps",bg=BG,fg=TEXT,font=("Segoe UI",22,"bold")).pack(anchor="w",padx=28,pady=(22,0))
  tk.Label(r,text="Open your favorite apps in their own window",bg=BG,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w",padx=29,pady=(4,12))
  tabs=tk.Frame(r,bg=BG);tabs.pack(fill="x",padx=24,pady=(0,10));self.buttons={}
  for c in ["All apps","Google","Work","Video","Custom"]:
   b=tk.Button(tabs,text=c,command=lambda x=c:self.setcat(x),relief="flat",bd=0,padx=13,pady=7,font=("Segoe UI",9,"bold"));b.pack(side="left",padx=(0,7));self.buttons[c]=b
  self.count=tk.Label(r,bg=BG,fg=MUTED,font=("Segoe UI",9));self.count.pack(anchor="w",padx=29)
  outer=tk.Frame(r,bg=BG);outer.pack(fill="both",expand=True,padx=20,pady=12)
  self.can=tk.Canvas(outer,bg=BG,highlightthickness=0);sb=tk.Scrollbar(outer,command=self.can.yview);self.grid=tk.Frame(self.can,bg=BG)
  self.grid.bind("<Configure>",lambda e:self.can.configure(scrollregion=self.can.bbox("all")))
  self.wid=self.can.create_window((0,0),window=self.grid,anchor="nw");self.can.configure(yscrollcommand=sb.set)
  self.can.pack(side="left",fill="both",expand=True);sb.pack(side="right",fill="y");self.can.bind("<Configure>",lambda e:self.can.itemconfigure(self.wid,width=e.width))
  self.q.trace_add("write",lambda *_:self.render());self.render()
 def save(self):
  os.makedirs(os.path.dirname(DATA),exist_ok=True)
  with open(DATA,"w",encoding="utf-8") as f:json.dump(self.apps,f,ensure_ascii=False,indent=2)
 def setcat(self,c):self.cat=c;self.render()
 def render(self):
  for w in self.grid.winfo_children():w.destroy()
  for c,b in self.buttons.items():
   s=c==self.cat;b.configure(bg=BLUE if s else BG,fg="white" if s else MUTED)
  q=self.q.get().lower().strip();apps=[a for a in self.apps if (self.cat=="All apps" or a.get("category","Custom")==self.cat) and (not q or q in a["name"].lower() or q in a["url"].lower())]
  self.count.configure(text=f"{len(apps)} apps");cols=4 if self.can.winfo_width()>750 else 3 if self.can.winfo_width()>550 else 2
  for i,a in enumerate(apps):
   card=tk.Frame(self.grid,bg=WHITE,highlightbackground=BORDER,highlightthickness=1,cursor="hand2");card.grid(row=i//cols,column=i%cols,padx=8,pady=8,sticky="nsew");self.grid.grid_columnconfigure(i%cols,weight=1,uniform="cards")
   icon=tk.Canvas(card,width=54,height=54,bg=WHITE,highlightthickness=0);icon.pack(pady=(15,7));icon.create_oval(2,2,52,52,fill=a.get("color",BLUE),outline=a.get("color",BLUE));icon.create_text(27,27,text=a.get("icon","?"),fill="white",font=("Segoe UI",16,"bold"))
   tk.Label(card,text=a["name"],bg=WHITE,fg=TEXT,font=("Segoe UI",10,"bold")).pack()
   tk.Label(card,text=a["url"].replace("https://","").split("/")[0],bg=WHITE,fg=MUTED,font=("Segoe UI",8)).pack(pady=(3,14))
   for w in (card,icon):
    w.bind("<Button-1>",lambda e,x=a:self.open_app(x))
    w.bind("<Button-3>",lambda e,x=a:self.remove(x))
 def open_app(self,a):
  # Separate process lets the launcher stay responsive and supports multiple app windows.
  try:
   if getattr(sys,"frozen",False):
    cmd=[sys.executable,"--webview-child",a["name"],a["url"]]
   else:
    cmd=[sys.executable,os.path.abspath(__file__),"--webview-child",a["name"],a["url"]]
   subprocess.Popen(cmd, close_fds=True)
  except Exception as e:
   messagebox.showerror("Cannot open app",f"Could not start the app window.\n\n{e}",parent=self.r)
 def add(self):
  n=simpledialog.askstring("Add app","App name:",parent=self.r)
  if not n:return
  u=simpledialog.askstring("Add app","Website URL:",parent=self.r)
  if not u:return
  if not u.startswith(("http://","https://")):u="https://"+u
  self.apps.append(dict(name=n.strip(),url=u.strip(),icon=n.strip()[:1].upper(),color="#5F6368",category="Custom"));self.save();self.cat="All apps";self.render()
 def remove(self,a):
  if messagebox.askyesno("Remove app",f"Remove {a['name']}?",parent=self.r):self.apps.remove(a);self.save();self.render()

if __name__=="__main__":
 if len(sys.argv)>=4 and sys.argv[1]=="--webview-child":
  webview_child(sys.argv[2],sys.argv[3])
 else:
  root=tk.Tk();Launcher(root);root.mainloop()
