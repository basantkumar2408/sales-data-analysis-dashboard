# ============================================================
#   SALES DATA ANALYSIS DASHBOARD  (Tkinter + Matplotlib)
#   Run: python sales_tk.py
#   Requirements: pip install pandas numpy matplotlib seaborn
#   (tkinter Windows mein already installed hota hai)
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── DATASET GENERATE ────────────────────────────────────────
np.random.seed(42)
n = 5000
categories     = ['Electronics','Clothing','Furniture','Books','Sports','Food & Grocery']
regions        = ['North','South','East','West']
cat_weights    = [0.25,0.20,0.15,0.12,0.18,0.10]
region_weights = [0.30,0.25,0.20,0.25]
cat_prices     = {
    'Electronics':(5000,50000),'Clothing':(300,5000),
    'Furniture':(3000,40000),'Books':(100,1500),
    'Sports':(500,15000),'Food & Grocery':(50,2000),
}
months_rng = pd.date_range('2023-01-01','2023-12-31',freq='D')
rows=[]
for _ in range(n):
    date     = pd.Timestamp(np.random.choice(months_rng))
    cat      = np.random.choice(categories,p=cat_weights)
    reg      = np.random.choice(regions,p=region_weights)
    lo,hi    = cat_prices[cat]
    price    = round(np.random.uniform(lo,hi),2)
    qty      = np.random.randint(1,6)
    disc     = np.random.choice([0,.05,.10,.15,.20],p=[.5,.2,.15,.10,.05])
    rev      = round(price*qty*(1-disc),2)
    rows.append({'Date':date.date(),'Category':cat,'Region':reg,
                 'Unit_Price':price,'Quantity':qty,'Discount':disc,
                 'Revenue':rev,'Month':date.strftime('%b'),'Month_Num':date.month,
                 'Discount_Label':str(int(disc*100))+'%'})
df_full = pd.DataFrame(rows)

# ── COLOURS ─────────────────────────────────────────────────
BG='#0d1117'; CARD='#161b22'; CARD2='#1c2330'
ACCENT='#58a6ff'; GREEN='#3fb950'; ORANGE='#d29922'
PURPLE='#bc8cff'; TEXT='#e6edf3'; SUBTEXT='#8b949e'; GRID='#21262d'
CAT_COLORS=['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff','#ff7b72']

plt.rcParams.update({
    'figure.facecolor':BG,'axes.facecolor':CARD,'axes.edgecolor':GRID,
    'grid.color':GRID,'text.color':TEXT,'axes.labelcolor':SUBTEXT,
    'xtick.color':SUBTEXT,'ytick.color':SUBTEXT,
    'font.family':'DejaVu Sans','axes.grid':True,
    'grid.linewidth':0.5,'grid.alpha':0.4,
})

# ── DRAW DASHBOARD ──────────────────────────────────────────
def draw_dashboard(df, canvas_widget, frame):
    for w in frame.winfo_children():
        w.destroy()

    fig = plt.figure(figsize=(16,10), facecolor=BG)
    fig.subplots_adjust(left=0.05,right=0.97,top=0.84,bottom=0.07,hspace=0.55,wspace=0.38)

    total_rev    = df['Revenue'].sum()
    total_orders = len(df)
    avg_order    = df['Revenue'].mean() if len(df)>0 else 0
    top_cat      = df.groupby('Category')['Revenue'].sum().idxmax() if len(df)>0 else 'N/A'

    kpis = [
        ("Total Revenue",   f"Rs {total_rev/1e7:.2f} Cr", ACCENT),
        ("Total Orders",    f"{total_orders:,}",           GREEN),
        ("Avg Order Value", f"Rs {avg_order:,.0f}",        ORANGE),
        ("Top Category",    top_cat,                       PURPLE),
    ]
    for i,(label,val,col) in enumerate(kpis):
        ax = fig.add_axes([0.04+i*0.236, 0.87, 0.215, 0.10])
        ax.set_facecolor(CARD2); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
        ax.add_patch(mpatches.FancyBboxPatch((0.01,0.01),0.98,0.98,
            boxstyle="round,pad=0.03",facecolor=CARD2,edgecolor=col,linewidth=1.8))
        ax.text(0.07,0.68,label,fontsize=9,color=SUBTEXT,va='center')
        ax.text(0.07,0.28,val,fontsize=14,color=col,va='center',fontweight='bold')

    fig.text(0.50,0.985,"SALES DATA ANALYSIS DASHBOARD  -  2023",
             ha='center',va='top',fontsize=16,color=TEXT,fontweight='bold')
    fig.text(0.50,0.955,f"Retail Performance  |  {len(df):,} Transactions  |  Jan-Dec 2023",
             ha='center',va='top',fontsize=9,color=SUBTEXT)

    gs = gridspec.GridSpec(2,3,figure=fig,
        left=0.05,right=0.97,top=0.83,bottom=0.07,hspace=0.55,wspace=0.38)

    # Chart 1 — Monthly Trend
    ax1 = fig.add_subplot(gs[0,:2])
    monthly = df.groupby('Month_Num')['Revenue'].sum().reindex(range(1,13),fill_value=0)
    mlabels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    ax1.plot(range(1,13),monthly.values/1e5,color=ACCENT,linewidth=2.5,
             marker='o',markersize=7,markerfacecolor=BG,markeredgewidth=2.2)
    ax1.fill_between(range(1,13),monthly.values/1e5,alpha=0.12,color=ACCENT)
    ax1.set_xticks(range(1,13)); ax1.set_xticklabels(mlabels,fontsize=9)
    ax1.set_title('Monthly Revenue Trend  (Rs in Lakhs)',color=TEXT,fontsize=11,fontweight='bold',pad=10)
    ax1.set_ylabel('Revenue (Rs Lakhs)',color=SUBTEXT,fontsize=9)
    if monthly.max()>0:
        pm = monthly.idxmax()
        ax1.annotate(f"Peak: Rs{monthly[pm]/1e5:.1f}L",
            xy=(pm,monthly[pm]/1e5),
            xytext=(pm-1.5,monthly[pm]/1e5+monthly.max()*0.09/1e5),
            arrowprops=dict(arrowstyle='->',color=GREEN,lw=1.5),
            color=GREEN,fontsize=9,fontweight='bold')
    for sp in ax1.spines.values(): sp.set_edgecolor(GRID)

    # Chart 2 — Pie
    ax2 = fig.add_subplot(gs[0,2])
    cat_rev = df.groupby('Category')['Revenue'].sum()
    if len(cat_rev)>0:
        wedges,texts,autotexts = ax2.pie(
            cat_rev,labels=cat_rev.index,autopct='%1.1f%%',
            colors=CAT_COLORS[:len(cat_rev)],startangle=140,
            wedgeprops=dict(edgecolor=BG,linewidth=1.5),
            textprops=dict(color=TEXT,fontsize=8),pctdistance=0.78)
        for at in autotexts:
            at.set_fontsize(7.5); at.set_color(BG); at.set_fontweight('bold')
    ax2.set_title('Revenue Share by Category',color=TEXT,fontsize=11,fontweight='bold',pad=10)
    ax2.set_facecolor(CARD)

    # Chart 3 — Region Bar
    ax3 = fig.add_subplot(gs[1,0])
    reg_rev = df.groupby('Region')['Revenue'].sum().sort_values()
    rc = [ACCENT,GREEN,ORANGE,PURPLE][:len(reg_rev)]
    bars = ax3.barh(reg_rev.index,reg_rev.values/1e5,color=rc,edgecolor=BG,linewidth=0.8)
    ax3.set_title('Revenue by Region  (Rs Lakhs)',color=TEXT,fontsize=11,fontweight='bold',pad=10)
    ax3.set_xlabel('Revenue (Rs Lakhs)',color=SUBTEXT,fontsize=9)
    for bar,val in zip(bars,reg_rev.values):
        ax3.text(val/1e5+reg_rev.max()*0.01/1e5,
                 bar.get_y()+bar.get_height()/2,
                 f'Rs{val/1e5:.1f}L',va='center',color=TEXT,fontsize=9,fontweight='bold')
    for sp in ax3.spines.values(): sp.set_edgecolor(GRID)

    # Chart 4 — Units vs Revenue
    ax4 = fig.add_subplot(gs[1,1])
    cat_qty  = df.groupby('Category')['Quantity'].sum()
    cat_rev2 = df.groupby('Category')['Revenue'].sum()/1e5
    x=np.arange(len(cat_rev2)); w=0.4
    ax4.bar(x-w/2,cat_qty.values,width=w,color=ACCENT,edgecolor=BG)
    ax4b=ax4.twinx()
    ax4b.bar(x+w/2,cat_rev2.values,width=w,color=ORANGE,edgecolor=BG)
    ax4.set_xticks(x)
    ax4.set_xticklabels([c.replace(' & ','\n& ') for c in cat_rev2.index],fontsize=7.5)
    ax4.set_ylabel('Units Sold',color=ACCENT,fontsize=9)
    ax4b.set_ylabel('Revenue (Rs Lakhs)',color=ORANGE,fontsize=9)
    ax4.set_title('Units Sold vs Revenue',color=TEXT,fontsize=11,fontweight='bold',pad=10)
    ax4.tick_params(axis='y',colors=ACCENT)
    ax4b.tick_params(axis='y',colors=ORANGE)
    ax4b.set_facecolor(CARD)
    for sp in ax4.spines.values():  sp.set_edgecolor(GRID)
    for sp in ax4b.spines.values(): sp.set_edgecolor(GRID)
    h=[mpatches.Patch(color=ACCENT,label='Units Sold'),
       mpatches.Patch(color=ORANGE,label='Revenue (Rs L)')]
    ax4.legend(handles=h,loc='upper right',fontsize=8,facecolor=CARD2,edgecolor=GRID,labelcolor=TEXT)

    # Chart 5 — Heatmap
    ax5 = fig.add_subplot(gs[1,2])
    try:
        heat = df.pivot_table(values='Revenue',index='Category',
                              columns='Discount_Label',aggfunc='mean')/1000
        dc = [c for c in ['0%','5%','10%','15%','20%'] if c in heat.columns]
        sns.heatmap(heat[dc],ax=ax5,cmap='YlOrRd',annot=True,fmt='.0f',
                    annot_kws={'size':8,'color':'#111'},
                    linewidths=0.5,linecolor=BG,
                    cbar_kws={'label':'Avg Rev (Rs 000s)'})
    except:
        ax5.text(0.5,0.5,'Not enough data',ha='center',va='center',color=SUBTEXT,fontsize=10)
    ax5.set_title('Avg Revenue vs Discount %',color=TEXT,fontsize=11,fontweight='bold',pad=10)
    ax5.set_xlabel('Discount %',color=SUBTEXT,fontsize=9)
    ax5.set_ylabel('',color=SUBTEXT)
    ax5.tick_params(axis='both',colors=SUBTEXT,labelsize=8)
    ax5.set_facecolor(CARD)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return fig

# ── MAIN APP ────────────────────────────────────────────────
class SalesDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Data Analysis Dashboard — 2023")
        self.root.configure(bg='#0d1117')
        self.root.state('zoomed')  # fullscreen on Windows

        self.region_vars   = {r: tk.BooleanVar(value=True) for r in regions}
        self.category_vars = {c: tk.BooleanVar(value=True) for c in categories}
        self.current_fig   = None

        self._build_ui()
        self._apply_filter()

    def _build_ui(self):
        # ── LEFT SIDEBAR ────────────────────────────────────
        sidebar = tk.Frame(self.root, bg='#161b22', width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="FILTER PANEL", bg='#161b22',
                 fg='#58a6ff', font=('Arial',13,'bold')).pack(pady=(18,4))
        tk.Frame(sidebar, bg='#21262d', height=1).pack(fill=tk.X, padx=12, pady=4)

        # Region
        tk.Label(sidebar, text="REGION", bg='#161b22',
                 fg='#58a6ff', font=('Arial',10,'bold')).pack(anchor='w', padx=18, pady=(12,4))
        for r in regions:
            cb = tk.Checkbutton(sidebar, text=f"  {r}",
                variable=self.region_vars[r],
                bg='#1c2330', fg='#e6edf3',
                selectcolor='#0f3460',
                activebackground='#1c2330', activeforeground='#58a6ff',
                font=('Arial',11), anchor='w', cursor='hand2')
            cb.pack(fill=tk.X, padx=14, pady=3, ipady=4)

        tk.Frame(sidebar, bg='#21262d', height=1).pack(fill=tk.X, padx=12, pady=10)

        # Category
        tk.Label(sidebar, text="CATEGORY", bg='#161b22',
                 fg='#58a6ff', font=('Arial',10,'bold')).pack(anchor='w', padx=18, pady=(2,4))
        for c in categories:
            cb = tk.Checkbutton(sidebar, text=f"  {c}",
                variable=self.category_vars[c],
                bg='#1c2330', fg='#e6edf3',
                selectcolor='#0f3460',
                activebackground='#1c2330', activeforeground='#58a6ff',
                font=('Arial',10), anchor='w', cursor='hand2')
            cb.pack(fill=tk.X, padx=14, pady=2, ipady=3)

        tk.Frame(sidebar, bg='#21262d', height=1).pack(fill=tk.X, padx=12, pady=12)

        # Buttons
        tk.Button(sidebar, text="Apply Filter",
            command=self._apply_filter,
            bg='#58a6ff', fg='#0d1117',
            font=('Arial',11,'bold'),
            relief='flat', cursor='hand2',
            activebackground='#79b8ff').pack(fill=tk.X, padx=14, pady=4, ipady=8)

        tk.Button(sidebar, text="Select All",
            command=self._select_all,
            bg='#21262d', fg='#e6edf3',
            font=('Arial',10),
            relief='flat', cursor='hand2').pack(fill=tk.X, padx=14, pady=2, ipady=5)

        tk.Button(sidebar, text="Deselect All",
            command=self._deselect_all,
            bg='#21262d', fg='#e6edf3',
            font=('Arial',10),
            relief='flat', cursor='hand2').pack(fill=tk.X, padx=14, pady=2, ipady=5)

        tk.Button(sidebar, text="Save as PNG",
            command=self._save_png,
            bg='#3fb950', fg='#0d1117',
            font=('Arial',11,'bold'),
            relief='flat', cursor='hand2',
            activebackground='#56d364').pack(fill=tk.X, padx=14, pady=(10,4), ipady=8)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(sidebar, textvariable=self.status_var,
                 bg='#161b22', fg='#8b949e',
                 font=('Arial',8), wraplength=190).pack(pady=8, padx=10)

        # ── RIGHT DASHBOARD AREA ────────────────────────────
        self.dash_frame = tk.Frame(self.root, bg='#0d1117')
        self.dash_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _apply_filter(self):
        sel_reg = [r for r,v in self.region_vars.items()   if v.get()]
        sel_cat = [c for c,v in self.category_vars.items() if v.get()]
        if not sel_reg: sel_reg = regions
        if not sel_cat: sel_cat = categories
        filtered = df_full[
            df_full['Region'].isin(sel_reg) &
            df_full['Category'].isin(sel_cat)
        ]
        if self.current_fig:
            plt.close(self.current_fig)
        self.current_fig = draw_dashboard(filtered, None, self.dash_frame)
        self.status_var.set(f"Showing {len(filtered):,} rows\n{len(sel_reg)} regions, {len(sel_cat)} categories")

    def _select_all(self):
        for v in self.region_vars.values():   v.set(True)
        for v in self.category_vars.values(): v.set(True)
        self._apply_filter()

    def _deselect_all(self):
        for v in self.region_vars.values():   v.set(False)
        for v in self.category_vars.values(): v.set(False)

    def _save_png(self):
        sel_reg = [r for r,v in self.region_vars.items()   if v.get()]
        sel_cat = [c for c,v in self.category_vars.items() if v.get()]
        if not sel_reg: sel_reg = regions
        if not sel_cat: sel_cat = categories
        filtered = df_full[
            df_full['Region'].isin(sel_reg) &
            df_full['Category'].isin(sel_cat)
        ]
        fig_s = plt.figure(figsize=(20,13), facecolor=BG)
        # redraw offscreen
        import copy
        fname = 'sales_dashboard_export.png'
        if self.current_fig:
            self.current_fig.savefig(fname, dpi=150, bbox_inches='tight', facecolor=BG)
        messagebox.showinfo("Saved!", f"Dashboard saved as:\n{fname}")
        self.status_var.set(f"Saved: {fname}")

if __name__ == '__main__':
    root = tk.Tk()
    app  = SalesDashboardApp(root)
    root.mainloop()
