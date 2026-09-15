# TPowerPlanSwitcher

A tiny Windows system tray app that switches between two power plans with a single click.

*Tek tıkla iki güç planı arasında geçiş yapan küçük bir Windows sistem tepsisi uygulaması.*

---

## English

### What it does

TPowerPlanSwitcher lives in the notification area next to the clock and shows which Windows power plan is currently active. By default it toggles between **Balanced** and **Power saver**.

- **Left click** — switches to the other plan immediately.
- **Right click** — a menu with both plans (the active one is marked) and *Exit*.
- The icon and tooltip always reflect the real active plan, including when you change it from Windows Settings or the battery flyout.

The app is a single Python file. Both tray icons are embedded in it as base64 PNG data, so there are no image files to ship alongside it.

### How it works

Power plans are read and written through `PowerGetActiveScheme` and `PowerSetActiveScheme` in `powrprof.dll`. The app never launches `powercfg.exe`, so no process is spawned and no console window flashes on screen.

External plan changes are detected with `RegNotifyChangeKeyValue` on the registry key that holds the active scheme. The watcher thread blocks on a Windows event object and consumes no CPU until something actually changes — there is no polling loop.

A named mutex prevents a second copy of the app from running, and DPI awareness is enabled so the tray icon stays sharp on scaled displays.

### Requirements

- Windows 10 or Windows 11
- Python 3.9 or newer
- `pip install pystray pillow`

### Running from source

```
pip install pystray pillow
python TPowerPlanSwitcher.py
```

The icon appears next to the clock. If you do not see it, click the arrow to open the overflow area — you can drag the icon out to keep it permanently visible.

### Building the .exe

```
pip install pyinstaller
pyinstaller --onefile --noconsole --name "TPowerPlanSwitcher" --icon "TPowerPlanSwitcher.ico" TPowerPlanSwitcher.py
```

The result is `dist\TPowerPlanSwitcher.exe`. It is fully self-contained and can be moved anywhere. The `build` folder and the generated `.spec` file can be deleted afterwards.

`--noconsole` is required; without it an empty console window stays open behind the app. `TPowerPlanSwitcher.ico` is the same orange bolt used for the Balanced tray icon, and it becomes the icon of the executable itself.

### Changing the plans before you compile

Open `TPowerPlanSwitcher.py` and edit these lines near the top of the file:

```python
BALANCED_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e"
POWER_SAVER_GUID = "a1841308-3541-4fab-bc81-f71556f20b4a"

PLAN_NAMES = {
    BALANCED_GUID: "Balanced",
    POWER_SAVER_GUID: "Power saver",
}
```

Replace a GUID with the plan you want, and change the matching entry in `PLAN_NAMES` so the menu label and tooltip stay correct. Then build again.

The standard Windows plan GUIDs are:

| Plan | GUID |
| --- | --- |
| Balanced | `381b4222-f694-41f0-9685-ff5bb260df2e` |
| Power saver | `a1841308-3541-4fab-bc81-f71556f20b4a` |
| High performance | `8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c` |
| Ultimate performance | `e9a42b02-d5df-448d-aa00-03f14749eb61` |

To see every plan available on your own machine, including custom and OEM ones, run:

```
powercfg /list
```

High performance and Ultimate performance are hidden by default on many Windows 11 installations. If a GUID does not appear in `powercfg /list`, make it available first:

```
powercfg -duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

Note that this command creates a **copy** with a new GUID. Run `powercfg /list` again afterwards and use the GUID that was actually created.

To replace the tray icons, generate new 128×128 PNG images, encode them as base64, and replace the contents of `ICON_BALANCED_B64` and `ICON_POWER_SAVER_B64`.

### Starting automatically with Windows

Press `Win+R`, type `shell:startup`, and place a shortcut to `TPowerPlanSwitcher.exe` in the folder that opens. Move the executable to a permanent location first, otherwise the shortcut breaks when you move the file.

### Notes

Changing a power plan normally works without administrator rights. Some corporate group policies restrict it; in that case the app shows a notification instead of failing silently.

Some antivirus products flag PyInstaller executables as false positives. If that happens you may need to add the file to your exclusions list.

### License

MIT

---

## Türkçe

### Ne yapıyor

TPowerPlanSwitcher saatin yanındaki bildirim alanında durur ve o anda hangi Windows güç planının etkin olduğunu gösterir. Varsayılan olarak **Balanced** ve **Power saver** arasında geçiş yapar.

- **Sol tık** — diğer plana anında geçer.
- **Sağ tık** — her iki planın bulunduğu bir menü açılır (etkin olan işaretlidir) ve *Exit* seçeneği yer alır.
- İkon ve üzerine gelince çıkan yazı her zaman gerçek etkin planı gösterir; planı Windows Ayarlar'dan veya pil simgesinden değiştirdiğinde de kendini günceller.

Uygulama tek bir Python dosyasından oluşur. Her iki tepsi ikonu da dosyanın içine base64 PNG verisi olarak gömülüdür, yanında ayrıca görsel dosyası taşımak gerekmez.

### Nasıl çalışıyor

Güç planları `powrprof.dll` içindeki `PowerGetActiveScheme` ve `PowerSetActiveScheme` fonksiyonlarıyla doğrudan okunup yazılır. Uygulama `powercfg.exe` çalıştırmaz; dolayısıyla süreç açılmaz ve ekranda konsol penceresi flaşlamaz.

Dışarıdan yapılan plan değişiklikleri, etkin planı tutan kayıt defteri anahtarı üzerinde `RegNotifyChangeKeyValue` ile yakalanır. İzleyici thread bir Windows olay nesnesinde bloklanır ve gerçekten bir değişiklik olana kadar hiç CPU harcamaz — zamanlayıcıyla yoklama yapılmaz.

Adlandırılmış bir mutex uygulamanın ikinci bir kopyasının açılmasını engeller. Ölçeklenmiş ekranlarda tepsi ikonunun net kalması için DPI farkındalığı açıktır.

### Gereksinimler

- Windows 10 veya Windows 11
- Python 3.9 veya üstü
- `pip install pystray pillow`

### Kaynaktan çalıştırma

```
pip install pystray pillow
python TPowerPlanSwitcher.py
```

İkon saatin yanında belirir. Göremezsen taşma alanını açmak için ok işaretine tıkla; ikonu oradan sürükleyerek kalıcı olarak görünür yapabilirsin.

### .exe derleme

```
pip install pyinstaller
pyinstaller --onefile --noconsole --name "TPowerPlanSwitcher" --icon "TPowerPlanSwitcher.ico" TPowerPlanSwitcher.py
```

Sonuç `dist\TPowerPlanSwitcher.exe` olur. Dosya tamamen kendi kendine yeterlidir, istediğin yere taşıyabilirsin. Derleme sonrası `build` klasörünü ve oluşan `.spec` dosyasını silebilirsin.

`--noconsole` zorunludur; olmazsa uygulamanın arkasında boş bir konsol penceresi açık kalır. `TPowerPlanSwitcher.ico`, Balanced tepsi ikonuyla aynı turuncu şimşektir ve çalıştırılabilir dosyanın kendi simgesi olur.

### Derlemeden önce planları değiştirme

`TPowerPlanSwitcher.py` dosyasını aç ve başlardaki şu satırları düzenle:

```python
BALANCED_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e"
POWER_SAVER_GUID = "a1841308-3541-4fab-bc81-f71556f20b4a"

PLAN_NAMES = {
    BALANCED_GUID: "Balanced",
    POWER_SAVER_GUID: "Power saver",
}
```

GUID'i istediğin planla değiştir, ardından `PLAN_NAMES` içindeki karşılığını da güncelle ki menü etiketi ve tooltip doğru kalsın. Sonra yeniden derle.

Standart Windows plan GUID'leri:

| Plan | GUID |
| --- | --- |
| Dengeli (Balanced) | `381b4222-f694-41f0-9685-ff5bb260df2e` |
| Güç tasarrufu (Power saver) | `a1841308-3541-4fab-bc81-f71556f20b4a` |
| Yüksek performans | `8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c` |
| Üstün performans | `e9a42b02-d5df-448d-aa00-03f14749eb61` |

Kendi bilgisayarındaki tüm planları, özel ve üretici planları dahil, görmek için:

```
powercfg /list
```

Yüksek performans ve Üstün performans planları çoğu Windows 11 kurulumunda varsayılan olarak gizlidir. Bir GUID `powercfg /list` çıktısında görünmüyorsa önce kullanılabilir hale getir:

```
powercfg -duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

Bu komutun yeni bir GUID ile bir **kopya** oluşturduğunu unutma. Komuttan sonra `powercfg /list` çalıştırıp gerçekten oluşan GUID'i kullan.

Tepsi ikonlarını değiştirmek için 128×128 PNG görseller hazırla, base64'e çevir ve `ICON_BALANCED_B64` ile `ICON_POWER_SAVER_B64` içeriklerini değiştir.

### Windows açılışında otomatik başlatma

`Win+R` tuşlarına bas, `shell:startup` yaz ve açılan klasöre `TPowerPlanSwitcher.exe` kısayolunu koy. Çalıştırılabilir dosyayı önce kalıcı bir yere taşı, yoksa dosyayı taşıdığında kısayol kırılır.

### Notlar

Güç planı değiştirmek normalde yönetici hakkı gerektirmez. Bazı kurumsal grup ilkeleri bunu kısıtlar; böyle bir durumda uygulama sessizce başarısız olmak yerine bir bildirim gösterir.

Bazı antivirüs yazılımları PyInstaller ile derlenmiş dosyaları yanlış pozitif olarak işaretleyebilir. Böyle bir durumda dosyayı istisnalara eklemen gerekebilir.

### Lisans

MIT
