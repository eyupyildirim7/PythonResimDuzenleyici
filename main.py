import tkinter as tk 
from tkinter import ttk, filedialog , messagebox , colorchooser 
from PIL import Image ,ImageTk,ImageEnhance,ImageFilter,ImageDraw,ImageFont
import os 

class ResimDuzenleyici:
    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.title("Kodlama Kampi - Resim Düzenleyici")
        self.pencere.geometry("1200x1200")

        self.guncel_resim = None
        self.orjinal_resim= None
        self.dosya_yolu = None
        self.metin_rengi= "#000000"
        self.gosterim_resim= None

        self.parlaklik_degeri= tk.DoubleVar(value=1.0)
        self.kontrast_degeri =tk.DoubleVar(value=1.0)
        self.keskinlik_degeri=tk.DoubleVar(value=1.0)
        self.yazi_boyutu = tk.IntVar(value=24)
        self.yazi_metni=tk.StringVar(value="")
        self.yeni_genislik=tk.IntVar(value=800)
        self.yeni_yukseklik=tk.IntVar(value=600)


        self.arayuz_olustur()


    def arayuz_olustur(self):
        self.sol_panel=ttk.Frame(self.pencere,padding="10")
        self.sol_panel.pack(side=tk.LEFT,fill=tk.Y)

        self.resim_alani=ttk.Label(self.pencere)
        self.resim_alani.pack(expand=True)
        self.resim_alani.bind("<Button-1>",self.yazi_ekle_tikla)


        self.resim_sec_button=ttk.Button(
            self.sol_panel,
            text="Resim Sec",
            command=self.resim_sec
            )
        
        self.resim_sec_button.pack(pady=5)

        ttk.Label(self.sol_panel,text="Parlaklik:").pack(pady=(10,0))
        self.parlaklik_slider =ttk.Scale(
            self.sol_panel,
            from_ = 0.0,
            to=2.0,
            variable=self.parlaklik_degeri,
            command=lambda x:self.efekt_uygula()
        )
        self.parlaklik_slider.pack()
        ttk.Label(self.sol_panel,text="Kontrast:").pack(pady=(10.0))
        self.kontrast_slider=ttk.Scale(
            self.sol_panel,
            from_=0.0,
            to=2.0,
            variable=self.kontrast_degeri,
            command=lambda x:self.efekt_uygula()
        )
        self.kontrast_slider.pack()

        ttk.Label(self.sol_panel,text="Kesinlik:").pack(pady=10.0)
        self.keskinlik_slider= ttk.Scale(
            self.sol_panel,
            from_=0.0,
            to=2.0,
            variable=self.keskinlik_degeri,
            command=lambda x:self.efekt_uygula())
        
        self.keskinlik_slider.pack()

        ttk.Label(self.sol_panel,text=" Yazi Ekleme:").pack()
        ttk.Entry(
            self.sol_panel,
            textvariable=self.yazi_metni,
        ).pack(pady=5)

        ttk.Label(self.sol_panel,text="Yazi Boyutu:").pack()
        ttk.Scale(
            self.sol_panel,
            from_=8,
            to=72,
            variable=self.yazi_boyutu
        ).pack()


        ttk.Button(
            self.sol_panel,
            text="Yazi Rengi Sec:",
            command=self.yazi_rengi_sec
        ).pack(pady=5)


        ttk.Label(self.sol_panel,text="  Boyutlandirma:").pack()
        ttk.Label(self.sol_panel,text="Genislik:").pack()
        ttk.Entry(
            self.sol_panel,
            textvariable=self.yeni_genislik
        ).pack()

        ttk.Label(self.sol_panel,text="Yukseklik:").pack()
        ttk.Entry(
            self.sol_panel,
            textvariable=self.yeni_yukseklik
        ).pack()
        ttk.Button(
            self.sol_panel,
            text="Boyutlandir",
            command=self.resim_boyutlandir
        ).pack(pady=5)

        ttk.Label(self.sol_panel,text="  Renk Efektleri:").pack()
        ttk.Button(
            self.sol_panel,
            text="Siyah Beyaz",
            command=lambda:self.renk_efekti_uygula("siyah_beyaz")
        ).pack(pady=2)


        ttk.Button(
            self.sol_panel,
            text="Sepya",
            command=lambda:self.renk_efekti_uygula("sepya")
        ).pack(pady=2)


        ttk.Label(self.sol_panel,text="  Filtreler:").pack(pady=(10,0))
        self.filtre_butonlari_olustur()
        self.kaydet_button=ttk.Button(
            self.sol_panel,
            text="Resim Kaydet",
            command=self.resim_kaydet
        )
        self.kaydet_button.pack(pady=(10))
        self.sifirla_button=ttk.Button(
            self.sol_panel,
            text="Orjinale Don",
            command=self.resim_sifirla
        )
        self.sifirla_button.pack(pady=5)


    def filtre_butonlari_olustur(self):
        filtreler_frame=ttk.Frame(self.sol_panel)
        filtreler_frame.pack(pady=5)

        filtreler = [
            ("Bulanik",ImageFilter.BLUR),
            ("Keskin",ImageFilter.SHARPEN),
            ("Kabartma",ImageFilter.EMBOSS),
            ("Kenar Bulma",ImageFilter.FIND_EDGES)
            
        ]

        for isim, filtre in filtreler:
            ttk.Button(
                filtreler_frame,
                text=isim,
                command=lambda f=filtre: self.filtre_uygula(f)
            ).pack(pady=2)

    
    def resim_sec(self):
        self.dosya_yolu=filedialog.askopenfilename(
            filetypes=[
                ("Resim Dosyalari","*.png *.jpg *.jpeg *.gif *.bmp")
            ]
        )
        if self.dosya_yolu:
            self.orjinal_resim=Image.open(self.dosya_yolu)
            self.guncel_resim=self.orjinal_resim.copy()
            self.resim_goster()
        


    def efekt_uygula(self):
        if self.orjinal_resim:
            self.guncel_resim=self.orjinal_resim.copy()
            parlaklik = ImageEnhance.Brightness(self.guncel_resim)
            self.guncel_resim = parlaklik.enhance(self.parlaklik_degeri.get())


            kontrast = ImageEnhance.Contrast(self.guncel_resim)
            self.guncel_resim=kontrast.enhance(self.kontrast_degeri.get())

            keskinlik =ImageEnhance.Sharpness(self.guncel_resim)
            self.guncel_resim=keskinlik.enhance(self.keskinlik_degeri.get())

            self.resim_goster()



    def  filtre_uygula(self,filtre):
        if self.guncel_resim:
            self.guncel_resim=self.guncel_resim.filter(filtre)
            self.resim_goster()


    def resim_sifirla(self):
        if self.orjinal_resim:
            self.parlaklik_degeri.set(1.0)
            self.kontrast_degeri.set(1.0)
            self.keskinlik_degeri.set(1.0)
            self.guncel_resim=self.orjinal_resim.copy()
            self.resim_goster()


    def resim_kaydet(self):
        if self.guncel_resim:
            kayit_yolu=filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG","*.png"),
                    ("JPG","*.jpg"),
                    ("BMP","*.bmp")
                ]
            )
            if kayit_yolu:
                self.guncel_resim.save(kayit_yolu)
                messagebox.showinfo(
                    "Basarili ile kayit edildi.",
                    "Resminiz Basari ile kayit edildi"
                )   

    def resim_goster(self):
        if self.guncel_resim:
            en = 800 
            boy = 600 
            gosterim_resmi=self.guncel_resim.copy()
            gosterim_resmi.thumbnail((en , boy ))


            foto =ImageTk.PhotoImage(gosterim_resmi)
            self.resim_alani.configure(image=foto)
            self.resim_alani.image = foto
            self.gosterim_resmi= foto


    def yazi_rengi_sec(self):
        renk = colorchooser.askcolor(title="Yazi Rengi Sec")
        if renk[1]:
            self.metin_rengi=renk[1]


    def yazi_ekle_tikla(self,event):
        if self.guncel_resim and self.yazi_metni.get():
            gosterim_en=self.gosterim_resmi.width()
            gosterim_boy =self.gosterim_resmi.height()

            orjinal_en,orjinal_boy=self.guncel_resim.size


            x = int(event.x *(orjinal_en / gosterim_en))
            y = int(event.y *(orjinal_boy / gosterim_boy))

            draw = ImageDraw.Draw(self.guncel_resim)
            font = ImageFont.truetype("arial.ttf",self.yazi_boyutu.get())
            draw.text((x,y),self.yazi_metni.get(),fill=self.metin_rengi, font=font)
            self.resim_goster()






    def resim_boyutlandir(self):
        if self.guncel_resim:
            yeni_boyut=(self.yeni_genislik.get(),self.yeni_yukseklik.get())
            self.guncel_resim =self.guncel_resim.resize(yeni_boyut,Image.LANCZOS)
            self.resim_goster()

    
    def renk_efekti_uygula(self,efekt_tipi):
        if self.guncel_resim:
            if efekt_tipi == "siyah_beyaz" :
                self.guncel_resim = self.guncel_resim.convert("L")
            elif efekt_tipi == "sepya":
                gri = self.guncel_resim.convert("L")
                self.guncel_resim =Image.merge('RGB',[
                    gri.point(lambda x:x*1.05),
                    gri.point(lambda x:x*0.95),
                    gri.point(lambda x:x*.80)
                ])
            self.resim_goster()


if __name__ == "__main__":
    uygulama = ResimDuzenleyici()
    uygulama.pencere.mainloop()