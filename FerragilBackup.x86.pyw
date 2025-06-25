import os
import shutil
import threading
import time
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, IntVar, Checkbutton, ttk
from PIL import Image, ImageTk
import json
import winreg
import pystray
import sys
import ctypes
import base64
import io

CONFIG_FILE = "config.json"

DEFAULT_ICON = (
    "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"
)

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class FileCopierApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ferragil - Backup")
        self.automation_var = IntVar()
        self.systray_var = IntVar()
        self.stop_automation = threading.Event()
        self.directory_pairs = []
        self.copying = False
        self.progress_bars = {}
        self.progress_labels = {}
        self.time_labels = {}
        self.config_data = {}
        self.icon = None

        self.load_config()
        self.automation_var.set(1 if self.config_data.get("automation", False) else 0)
        self.systray_var.set(1 if self.config_data.get("systray", False) else 0)

        top_frame = tk.Frame(self.master)
        top_frame.pack(padx=10, pady=5, fill=tk.X)

        control_frame = tk.Frame(top_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        button_frame = tk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        tk.Button(button_frame, text="Adicionar Par", command=self.add_pair).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Remover Selecionado", command=self.remove_pair).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Editar Selecionado", command=self.edit_pair).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Copiar Todos", command=self.start_copy_all).pack(side=tk.LEFT, padx=5)

        check_frame = tk.Frame(control_frame)
        check_frame.pack(fill=tk.X, pady=5)
        tk.Button(check_frame, text="Horarios Backup", command=self.manage_schedules).pack(side=tk.LEFT, padx=5)
        Checkbutton(check_frame, text='Automacao', variable=self.automation_var, command=self.toggle_automation).pack(side=tk.LEFT, padx=5)
        Checkbutton(check_frame, text='Systray', variable=self.systray_var, command=self.toggle_systray).pack(side=tk.LEFT, padx=5)

        image_frame = tk.Frame(top_frame)
        image_frame.pack(side=tk.RIGHT, padx=10)
        try:
            ferragil_img = self.get_icon_image("Ferragil.png")
            self.ferragil_photo = ImageTk.PhotoImage(ferragil_img)
            tk.Label(image_frame, image=self.ferragil_photo).pack()
        except Exception:
            pass

        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(main_frame, columns=("Source", "Destination", "Progress", "Percentage", "Time"), show="headings", height=15)
        self.tree.heading("Source", text="Origem")
        self.tree.heading("Destination", text="Destino")
        self.tree.heading("Progress", text="Progresso")
        self.tree.heading("Percentage", text="%")
        self.tree.heading("Time", text="Tempo Restante")
        self.tree.column("Source", width=200)
        self.tree.column("Destination", width=200)
        self.tree.column("Progress", width=150)
        self.tree.column("Percentage", width=50)
        self.tree.column("Time", width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        for pair in self.config_data.get("directory_pairs", []):
            item = self.tree.insert("", tk.END, values=(pair["source"], pair["destination"], "", "0%", "--:--"))
            self.directory_pairs.append({"source": pair["source"], "destination": pair["destination"], "item": item})
            self.progress_bars[item] = ttk.Progressbar(self.tree, length=140, mode="determinate")
            self.progress_labels[item] = tk.Label(self.tree, text="0%")
            self.time_labels[item] = tk.Label(self.tree, text="--:--")
            self.tree.set(item, "Progress", "")
            self.tree.set(item, "Percentage", "0%")
            self.tree.set(item, "Time", "--:--")

        try:
            logoF_img = self.get_icon_image("logoF.png")
            self.logo_photo = ImageTk.PhotoImage(logoF_img)
            self.master.iconphoto(True, self.logo_photo)
        except Exception:
            pass

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.protocol("WM_SYSCOMMAND", self.on_minimize)

        if self.systray_var.get() == 1:
            self.setup_systray()
            self.hide_window()

        if self.automation_var.get() == 1:
            self.start_automation()

    def get_icon_image(self, filename):
        try:
            filepath = get_resource_path(filename)
            return Image.open(filepath)
        except Exception:
            icon_data = base64.b64decode(DEFAULT_ICON)
            return Image.open(io.BytesIO(icon_data))

    def setup_systray(self):
        try:
            icon_image = self.get_icon_image("logoF.png")
            menu = (
                pystray.MenuItem("Restaurar", self.restore_window),
                pystray.MenuItem("Sair", self.on_close)
            )
            self.icon = pystray.Icon("FileCopier", icon_image, "Ferragil - Backup", menu)
            threading.Thread(target=self.icon.run, daemon=True).start()
        except Exception:
            pass

    def hide_window(self):
        self.master.withdraw()
        if self.systray_var.get() == 1:
            hwnd = ctypes.windll.user32.GetParent(self.master.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            style |= 0x00000080 | 0x00040000  # WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
            ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE
        if not self.icon:
            self.setup_systray()

    def restore_window(self):
        if self.icon:
            self.master.deiconify()
            hwnd = ctypes.windll.user32.GetParent(self.master.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            style &= ~(0x00000080 | 0x00040000)  # Remove WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
            ctypes.windll.user32.ShowWindow(hwnd, 1)  # SW_SHOWNORMAL
            self.master.lift()

    def on_minimize(self, event, *args):
        if event == 0xF020 and self.systray_var.get() == 1:  # SC_MINIMIZE
            self.hide_window()
            return
        self.master.event_generate('<<WM_SYSCOMMAND>>', code=event)

    def toggle_systray(self):
        self.save_config()
        if self.systray_var.get() == 1:
            if not self.icon:
                self.setup_systray()
            self.hide_window()
        else:
            if self.icon:
                self.icon.stop()
                self.icon = None
            self.restore_window()

    def validate_paths(self, source, destination):
        try:
            if not os.path.exists(source) or not os.path.isdir(source):
                self.master.after(0, lambda: messagebox.showerror("Erro", "Diretorio de origem " + source + " nao existe ou nao e um diretorio."))
                return False
            try:
                os.makedirs(os.path.dirname(destination))
            except OSError:
                if not os.path.isdir(os.path.dirname(destination)):
                    self.master.after(0, lambda: messagebox.showerror("Erro", "Diretorio de destino " + os.path.dirname(destination) + " nao pode ser criado."))
                    return False
            return True
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Erro", "Erro ao validar diretorios " + source + " ou " + destination + ": " + str(e)))
            return False

    def copy_file_with_retry(self, src, dst, retries=3, delay=2):
        for attempt in range(retries):
            try:
                try:
                    os.makedirs(os.path.dirname(dst))
                except OSError:
                    if not os.path.isdir(os.path.dirname(dst)):
                        raise
                with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                    shutil.copyfileobj(fsrc, fdst, length=1024*1024)  # 1MB buffer
                shutil.copystat(src, dst)  # Preserve metadata
                return True
            except (IOError, OSError, WindowsError) as e:
                if attempt == retries - 1:
                    self.master.after(0, lambda: messagebox.showerror("Erro", "Falha ao copiar " + src + " para " + dst + " apos " + str(retries) + " tentativas: " + str(e)))
                    return False
                time.sleep(delay)
        return False

    def manage_schedules(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Gerenciar Horarios de Backup")
        dialog.transient(self.master)
        dialog.grab_set()

        main_frame = tk.Frame(dialog)
        main_frame.pack(padx=10, pady=10)

        tk.Label(main_frame, text="Horarios Configurados:").pack(anchor="w")
        schedule_listbox = tk.Listbox(main_frame, height=5, width=10)
        schedule_listbox.pack(side=tk.LEFT, padx=5, pady=5)

        for schedule in self.config_data.get("schedules", []):
            schedule_listbox.insert(tk.END, "%02d:%02d" % (schedule["hour"], schedule["minute"]))

        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.LEFT, padx=5)

        def add_schedule():
            add_dialog = tk.Toplevel(dialog)
            add_dialog.title("Adicionar Horario")
            add_dialog.transient(dialog)
            add_dialog.grab_set()

            tk.Label(add_dialog, text="Hora (00-23):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            hour_spinbox = tk.Spinbox(add_dialog, from_=0, to=23, width=5, format="%02.0f")
            hour_spinbox.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(add_dialog, text="Minuto (00-59):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            minute_spinbox = tk.Spinbox(add_dialog, from_=0, to=59, width=5, format="%02.0f")
            minute_spinbox.grid(row=1, column=1, padx=5, pady=5)

            def confirm():
                try:
                    hour = int(hour_spinbox.get())
                    minute = int(minute_spinbox.get())
                    if 0 <= hour <= 23 and 0 <= minute <= 59:
                        schedule = {"hour": hour, "minute": minute}
                        if schedule not in self.config_data.get("schedules", []):
                            schedule_listbox.insert(tk.END, "%02d:%02d" % (hour, minute))
                            self.config_data.setdefault("schedules", []).append(schedule)
                            self.save_config()
                        add_dialog.destroy()
                    else:
                        messagebox.showwarning("Entrada Invalida", "Hora deve ser 00-23 e minuto 00-59.")
                except ValueError:
                    messagebox.showwarning("Entrada Invalida", "Digite valores numericos validos.")

            tk.Button(add_dialog, text="Confirmar", command=confirm).grid(row=2, column=0, columnspan=2, pady=10)

        def edit_schedule():
            selected = schedule_listbox.curselection()
            if not selected:
                messagebox.showwarning("Nenhum Selecionado", "Selecione um horario para editar.")
                return
            index = selected[0]
            schedule = self.config_data["schedules"][index]

            edit_dialog = tk.Toplevel(dialog)
            edit_dialog.title("Editar Horario")
            edit_dialog.transient(dialog)
            edit_dialog.grab_set()

            tk.Label(edit_dialog, text="Hora (00-23):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            hour_spinbox = tk.Spinbox(edit_dialog, from_=0, to=23, width=5, format="%02.0f")
            hour_spinbox.delete(0, tk.END)
            hour_spinbox.insert(0, "%02d" % schedule["hour"])
            hour_spinbox.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(edit_dialog, text="Minuto (00-59):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            minute_spinbox = tk.Spinbox(edit_dialog, from_=0, to=59, width=5, format="%02.0f")
            minute_spinbox.delete(0, tk.END)
            minute_spinbox.insert(0, "%02d" % schedule["minute"])
            minute_spinbox.grid(row=1, column=1, padx=5, pady=5)

            def confirm():
                try:
                    hour = int(hour_spinbox.get())
                    minute = int(minute_spinbox.get())
                    if 0 <= hour <= 23 and 0 <= minute <= 59:
                        new_schedule = {"hour": hour, "minute": minute}
                        if new_schedule not in self.config_data.get("schedules", []) or new_schedule == schedule:
                            schedule_listbox.delete(index)
                            schedule_listbox.insert(index, "%02d:%02d" % (hour, minute))
                            self.config_data["schedules"][index] = new_schedule
                            self.save_config()
                            edit_dialog.destroy()
                        else:
                            messagebox.showwarning("Entrada Invalida", "Horario ja existe.")
                    else:
                        messagebox.showwarning("Entrada Invalida", "Hora deve ser 00-23 e minuto 00-59.")
                except ValueError:
                    messagebox.showwarning("Entrada Invalida", "Digite valores numericos validos.")

            tk.Button(edit_dialog, text="Confirmar", command=confirm).grid(row=2, column=0, columnspan=2, pady=10)

        def remove_schedule():
            selected = schedule_listbox.curselection()
            if not selected:
                messagebox.showwarning("Nenhum Selecionado", "Selecione um horario para remover.")
                return
            index = selected[0]
            schedule_listbox.delete(index)
            self.config_data["schedules"].pop(index)
            self.save_config()

        tk.Button(button_frame, text="Adicionar", command=add_schedule).pack(pady=2)
        tk.Button(button_frame, text="Editar", command=edit_schedule).pack(pady=2)
        tk.Button(button_frame, text="Remover", command=remove_schedule).pack(pady=2)

    def add_pair(self):
        if len(self.directory_pairs) >= 200:
            messagebox.showwarning("Limite Atingido", "Limite de 200 pares atingido.")
            return

        dialog = tk.Toplevel(self.master)
        dialog.title("Adicionar Par")
        dialog.transient(self.master)
        dialog.grab_set()

        tk.Label(dialog, text="Origem:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        source_entry = tk.Entry(dialog, width=50)
        source_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(dialog, text="Selecionar", command=lambda: self.choose_directory(source_entry)).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(dialog, text="Destino:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        dest_entry = tk.Entry(dialog, width=50)
        dest_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(dialog, text="Selecionar", command=lambda: self.choose_directory(dest_entry)).grid(row=1, column=2, padx=5, pady=5)

        def confirm():
            source = source_entry.get()
            destination = dest_entry.get()
            if source and destination and self.validate_paths(source, destination):
                item = self.tree.insert("", tk.END, values=(source, destination, "", "0%", "--:--"))
                self.directory_pairs.append({"source": source, "destination": destination, "item": item})
                self.progress_bars[item] = ttk.Progressbar(self.tree, length=140, mode="determinate")
                self.progress_labels[item] = tk.Label(self.tree, text="0%")
                self.time_labels[item] = tk.Label(self.tree, text="--:--")
                self.save_config()
                dialog.destroy()
            else:
                messagebox.showwarning("Entrada Invalida", "Selecione diretorios validos.")

        tk.Button(dialog, text="Confirmar", command=confirm).grid(row=2, column=0, columnspan=3, pady=10)

    def remove_pair(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Nenhum Selecionado", "Selecione um par para remover.")
            return

        for item in selected:
            index = self.tree.index(item)
            self.directory_pairs.pop(index)
            self.tree.delete(item)
            self.progress_bars.pop(item, None)
            self.progress_labels.pop(item, None)
            self.time_labels.pop(item, None)
        self.save_config()

    def edit_pair(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Nenhum Selecionado", "Selecione um par para editar.")
            return
        if len(selected) > 1:
            messagebox.showwarning("Selecao Invalida", "Selecione apenas um par.")
            return

        item = selected[0]
        index = self.tree.index(item)
        pair = self.directory_pairs[index]

        dialog = tk.Toplevel(self.master)
        dialog.title("Editar Par")
        dialog.transient(self.master)
        dialog.grab_set()

        tk.Label(dialog, text="Origem:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        source_entry = tk.Entry(dialog, width=50)
        source_entry.insert(0, pair["source"])
        source_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(dialog, text="Selecionar", command=lambda: self.choose_directory(source_entry)).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(dialog, text="Destino:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        dest_entry = tk.Entry(dialog, width=50)
        dest_entry.insert(0, pair["destination"])
        dest_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(dialog, text="Selecionar", command=lambda: self.choose_directory(dest_entry)).grid(row=1, column=2, padx=5, pady=5)

        def confirm():
            source = source_entry.get()
            destination = dest_entry.get()
            if source and destination and self.validate_paths(source, destination):
                self.directory_pairs[index] = {"source": source, "destination": destination, "item": item}
                self.tree.item(item, values=(source, destination, "", "0%", "--:--"))
                self.save_config()
                dialog.destroy()
            else:
                messagebox.showwarning("Entrada Invalida", "Selecione diretorios validos.")

        tk.Button(dialog, text="Confirmar", command=confirm).grid(row=2, column=0, columnspan=3, pady=10)

    def choose_directory(self, entry):
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def count_files_to_copy(self, origem, destino):
        total_files = 0
        try:
            for root, _, files in os.walk(origem):
                rel_path = os.path.relpath(root, origem)
                dest_root = os.path.join(destino, rel_path) if rel_path != '.' else destino
                for arquivo in files:
                    origem_path = os.path.join(root, arquivo)
                    destino_path = os.path.join(dest_root, arquivo)
                    try:
                        if not os.path.exists(destino_path) or os.path.getmtime(origem_path) > os.path.getmtime(destino_path):
                            total_files += 1
                    except (OSError, WindowsError):
                        continue
        except (OSError, WindowsError):
            return 0
        return total_files

    def copiar_arquivos(self, origem, destino, item, progress_callback):
        if not self.validate_paths(origem, destino):
            return 0

        try:
            try:
                os.makedirs(destino)
            except OSError:
                if not os.path.isdir(destino):
                    raise
        except (OSError, WindowsError) as e:
            self.master.after(0, lambda: messagebox.showerror("Erro", "Erro ao criar diretorio " + destino + ": " + str(e)))
            return 0

        files_copied = 0
        update_counter = 0

        try:
            for root, dirs, files in os.walk(origem):
                rel_path = os.path.relpath(root, origem)
                dest_root = os.path.join(destino, rel_path) if rel_path != '.' else destino
                try:
                    try:
                        os.makedirs(dest_root)
                    except OSError:
                        if not os.path.isdir(dest_root):
                            raise
                except (OSError, WindowsError) as e:
                    self.master.after(0, lambda: messagebox.showerror("Erro", "Erro ao criar diretorio " + dest_root + ": " + str(e)))
                    continue

                for arquivo in files:
                    if not self.copying:
                        break
                    origem_path = os.path.join(root, arquivo)
                    destino_path = os.path.join(dest_root, arquivo)
                    try:
                        if not os.path.exists(destino_path) or os.path.getmtime(origem_path) > os.path.getmtime(destino_path):
                            if self.copy_file_with_retry(origem_path, destino_path):
                                files_copied += 1
                                update_counter += 1
                                if update_counter >= 10 or os.path.getsize(origem_path) > 10*1024*1024:  # Update every 10 files or for large files
                                    progress_callback(files_copied, item)
                                    update_counter = 0
                    except (OSError, WindowsError) as e:
                        self.master.after(0, lambda: messagebox.showerror("Erro", "Erro ao acessar " + origem_path + ": " + str(e)))
                        continue
        except (OSError, WindowsError) as e:
            self.master.after(0, lambda: messagebox.showerror("Erro", "Erro ao copiar de " + origem + " para " + destino + ": " + str(e)))

        return files_copied

    def start_copy_all(self):
        if self.copying:
            messagebox.showwarning("Em Progresso", "Copia em andamento.")
            return
        if not self.directory_pairs:
            messagebox.showwarning("Sem Diretorios", "Nenhum par de diretorios configurado.")
            return
        valid_pairs = [(pair["source"], pair["destination"]) for pair in self.directory_pairs if self.validate_paths(pair["source"], pair["destination"])]
        if not valid_pairs:
            messagebox.showwarning("Diretorios Invalidos", "Nenhum par de diretorios valido.")
            return
        self.copying = True
        threading.Thread(target=self.copiar_todos, daemon=True).start()

    def copiar_todos(self, show_message=True):
        total_files = 0
        total_files_copied = 0
        start_time = time.time()

        file_counts = {}
        for pair in self.directory_pairs:
            if pair["source"] and pair["destination"] and self.validate_paths(pair["source"], pair["destination"]):
                file_counts[pair["item"]] = self.count_files_to_copy(pair["source"], pair["destination"])
                total_files += file_counts[pair["item"]]

        def update_progress(copied, item):
            pair_files = file_counts.get(item, 1)
            if pair_files > 0:
                percentage = (copied / pair_files) * 100
                def update_gui():
                    self.progress_bars[item]["value"] = percentage
                    self.tree.set(item, "Percentage", "%.1f%%" % percentage)
                    elapsed = time.time() - start_time
                    if copied > 0:
                        time_per_file = elapsed / copied
                        remaining_files = pair_files - copied
                        time_remaining = remaining_files * time_per_file
                        mins, secs = divmod(int(time_remaining), 60)
                        self.tree.set(item, "Time", "%02d:%02d" % (mins, secs))
                self.master.after(0, update_gui)

        for pair in self.directory_pairs:
            if pair["source"] and pair["destination"] and self.copying and self.validate_paths(pair["source"], pair["destination"]):
                files_copied = self.copiar_arquivos(pair["source"], pair["destination"], pair["item"], update_progress)
                total_files_copied += files_copied
                def reset_gui():
                    self.progress_bars[pair["item"]]["value"] = 0
                    self.tree.set(pair["item"], "Percentage", "0%")
                    self.tree.set(pair["item"], "Time", "--:--")
                self.master.after(0, reset_gui)

        self.copying = False
        self.save_config()
        if show_message:
            def show_completion():
                self.master.deiconify()
                self.restore_window()
                if total_files_copied > 0:
                    messagebox.showinfo("Concluido", "Um ou mais arquivos foram copiados com sucesso!")
                else:
                    messagebox.showwarning("Aviso", "Nenhum arquivo copiado.")
            self.master.after(0, show_completion)
        return total_files_copied

    def run_backup_with_retries(self, show_message=False, max_retries=3, retry_delay=300):
        retries = 0
        total_files_copied = 0
        while retries < max_retries and not self.stop_automation.is_set():
            self.copying = True
            total_files_copied = self.copiar_todos(show_message)
            self.copying = False
            if total_files_copied > 0:
                break
            retries += 1
            if retries < max_retries:
                time.sleep(retry_delay)
        return total_files_copied

    def toggle_automation(self):
        if self.automation_var.get() == 1:
            self.config_data["automation"] = True
            self.add_to_startup()
            self.start_automation()
        else:
            self.config_data["automation"] = False
            self.stop_automation.set()
            self.remove_from_startup()
        self.save_config()

    def add_to_startup(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
            exe_path = os.path.abspath(sys.argv[0])
            winreg.SetValueEx(key, "FileCopier", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Erro", "Erro ao configurar inicializacao: " + str(e)))

    def remove_from_startup(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "FileCopier")
            winreg.CloseKey(key)
        except Exception:
            pass

    def start_automation(self):
        self.stop_automation.clear()
        threading.Thread(target=self.automation_loop, daemon=True).start()
        if self.automation_var.get() == 1:
            threading.Thread(target=self.run_backup_with_retries, args=(False,), daemon=True).start()

    def automation_loop(self):
        triggered_schedules = set()
        while not self.stop_automation.is_set():
            if self.automation_var.get() == 1:
                now = datetime.datetime.now()
                current_date = now.date()
                current_hour = now.hour
                current_minute = now.minute
                for schedule in self.config_data.get("schedules", []):
                    schedule_time = (schedule["hour"], schedule["minute"], current_date)
                    if (current_hour == schedule["hour"] and
                        current_minute == schedule["minute"] and
                        schedule_time not in triggered_schedules and
                        not self.copying):
                        self.run_backup_with_retries(show_message=False)
                        triggered_schedules.add(schedule_time)
                if now.hour == 0 and now.minute == 0:  # Reset at midnight
                    triggered_schedules = set([s for s in triggered_schedules if s[2] != current_date])
            time.sleep(10)

    def on_close(self):
        self.copying = False
        self.stop_automation.set()
        self.save_config()
        if self.icon:
            self.icon.stop()
            self.icon = None
        self.master.destroy()

    def load_config(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), CONFIG_FILE)
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    self.config_data = json.load(f)
            else:
                self.config_data = {
                    "directory_pairs": [],
                    "schedules": [],
                    "automation": False,
                    "systray": False
                }
        except Exception:
            self.config_data = {
                "directory_pairs": [],
                "schedules": [],
                "automation": False,
                "systray": False
            }

    def save_config(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), CONFIG_FILE)
            self.config_data["directory_pairs"] = [{"source": pair["source"], "destination": pair["destination"]} for pair in self.directory_pairs]
            self.config_data["automation"] = bool(self.automation_var.get())
            self.config_data["systray"] = bool(self.systray_var.get())
            with open(config_path, "w") as f:
                json.dump(self.config_data, f, indent=4)
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopierApp(root)
    root.mainloop()