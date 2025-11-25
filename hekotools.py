import customtkinter as ctk
import requests
import subprocess
import winreg
import shutil
import zipfile
from pathlib import Path

ctk.set_appearance_mode('dark')
app = ctk.CTk()


def instalar():
    def install(url, nome_arquivo):
        downloadsFolder = Path.home() / "Downloads"
        finalPath = downloadsFolder / nome_arquivo

        print(f"Downloading to: {finalPath}")
        content = requests.get(url).content
        with open(finalPath, "wb") as f:
            f.write(content)
        print("File downloaded with success! ✅")

        # Fechar Steam
        subprocess.run(["taskkill", "/F", "/IM", "steam.exe"])

        # Instalar SteamTools
        print('Installing...')
        subprocess.run([finalPath], shell=True)
        print('Alright! ✅')

        # SteamBrew
        print("Downloading and installing SteamBrew")
        subprocess.run([
            "powershell",
            "-Command",
            'iwr -useb "https://steambrew.app/install.ps1" | iex'
        ], shell=True)
        print("Installation completed! First Steam launch will take longer...")

        # Abrir Steam
        try:
            chave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Valve\\Steam")
            caminho, _ = winreg.QueryValueEx(chave, "SteamExe")
            subprocess.Popen(caminho)
            print("Steam launched with success!")
        except Exception as e:
            print("I can't find Steam ❌", e)

        # Download LuaTools
        lua_zip_path = downloadsFolder / "luatools.zip"
        print(f"Downloading to: {lua_zip_path}")
        content = requests.get(
            "https://github.com/madoiscool/ltsteamplugin/releases/download/6.3/ltsteamplugin.zip"
        ).content
        with open(lua_zip_path, "wb") as f:
            f.write(content)

        # Unzip
        def unzip(zip_path, extract_to):
            print(f"Unzipping: {zip_path}")
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(extract_to)
            print("Unzipped!")

        unzip(lua_zip_path, downloadsFolder)

        # Encontrar pasta .millennium
        def find_millennium_dir():
            possible_drives = ["C:\\", "D:\\", "E:\\", "F:\\", "G:\\"]
            for drive in possible_drives:
                path = Path(drive) / "Program Files (x86)" / "Steam" / "plugins" / ".millennium"
                if path.exists():
                    return path
            return None

        # Move files e pastas para .millennium
        def move_from_downloads_to_millennium():
            downloads = Path.home() / "Downloads"
            millennium = find_millennium_dir()

            if millennium is None:
                print("❌ .millennium folder not found")
                return

            print(f"✔ millennium found in: {millennium}")

            items_to_move = [
                "backend",
                "public",
                "requirements.txt",
                "readme",
                "plugin.json",
                ".gitignore"
            ]

            for item in items_to_move:
                src_item = downloads / item
                dst_item = millennium / item

                if src_item.exists():
                    try:
                        if src_item.is_dir():
                            shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                            shutil.rmtree(src_item)
                            print(f"✂️  Moved folder: {item}")
                        else:
                            shutil.move(str(src_item), str(dst_item))
                            print(f"✂️  Moved file: {item}")
                    except Exception as e:
                        print(f"❌ Error moving {item}: {e}")
                else:
                    print(f"⚠ Not found in Downloads: {item}")

            print("\n✅ Everything moved to .millennium!")

        # Function call
        move_from_downloads_to_millennium()

    # MAIN CALL
    install("https://github.com/Arthuttut/Heko-Tools/releases/download/Release/st-setup-1.8.17r2.exe", "steamtools.exe")


def comprar():
    # WIP
    pass


# ------------------- GUI -------------------
app.title('Heko Tools')
app.geometry('300x300')

label = ctk.CTkLabel(app, text='Heko Tools')
installBtn = ctk.CTkButton(
    app,
    text='Install\n(Steam tools, Millenium and Lua Tools)\n [!!!NECESSÁRIO PARA COMPRAR OS JOGOS!!!]',
    command=instalar
)
comprarBtn = ctk.CTkButton(app, text='Comprar jogo', command=comprar)
jogoCampo = ctk.CTkEntry(app, placeholder_text='Digite o nome de um jogo')

label.pack(pady=10)
installBtn.pack(pady=5)
jogoCampo.pack(pady=5)
comprarBtn.pack(pady=5)

app.mainloop()

#made by heko
#code maybe will have changes.
