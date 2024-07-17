from tkinter import *
from tkinter import messagebox, ttk
import datetime
import random


class LibraryApp:
  def __init__(self):
      self.users_file = 'profile.txt'
      self.audit_file = 'jurnal.txt'
      self.counter_try = 0


      with open(self.users_file, 'w') as file:
          file.write('admin,admin\n')


      with open(self.audit_file, 'w'):
          pass


      self.root = Tk()
      self.root.geometry('500x300')
      self.root.title('Главное меню')
      self.root.resizable(width=False, height=False)
      self.root['bg'] = 'orange'


      self.reg_btn = ttk.Button(self.root, text='Регистрация', command=self.registration)
      self.reg_btn.pack()


      self.log_btn = ttk.Button(self.root, text='Авторизация', command=self.authorization)
      self.log_btn.pack()


      self.root.mainloop()


  def kabinet(self, username):
      window_kabinet = Toplevel(self.root)
      window_kabinet.geometry('500x300')
      window_kabinet.title('Личный кабинет')
      window_kabinet.resizable(width=False, height=False)
      window_kabinet['bg'] = 'orange'


      main_menu = Menu(window_kabinet)
      if username == 'admin':
          main_menu.add_cascade(label="Список пользователей", command=self.list_user)
          main_menu.add_cascade(label="Журнал аудита", command=self.jurnal)
          window_kabinet.config(menu=main_menu)
  def load_jurnal(self, data):
      with open(f'log.txt', 'w') as file:
          for i in data:
              file.write(f'{i}\n')

  def sort_jurnal(self, do_list,tree):
      # Сортировка по времени с миллисекундами в порядке убывания
      do_list.sort(key=lambda x: datetime.datetime.strptime(x[2].strip(), '%Y-%m-%d %H:%M:%S.%f'), reverse=True)

      # Очистка дерева перед обновлением
      for item in tree.get_children():
          tree.delete(item)

      # Вставка отсортированных данных
      for person in do_list:
          tree.insert("", END, values=person)

  def jurnal(self):
      window_jurnal = Toplevel(self.root)
      window_jurnal.geometry('700x300')
      window_jurnal.title('Список пользователей')
      window_jurnal.resizable(width=False, height=False)
      window_jurnal['bg'] = 'orange'


      with open('jurnal.txt', 'r') as file:
          data = file.read().split('\n')


      load_btn = ttk.Button(window_jurnal, text='Выгрузить журнал', command=lambda: self.load_jurnal(data))
      load_btn.pack()


      do_list = [item.split(',') for item in data[:-1]]
      columns = ['действие', 'пользователь', 'время']


      tree = ttk.Treeview(window_jurnal, columns=columns, show="headings")
      tree.pack(fill=BOTH, expand=1)
      tree.heading("действие", text="действие")
      tree.heading("пользователь", text="пользователь")
      tree.heading("время", text="время")


      for person in do_list:
          tree.insert("", END, values=person)

      sort_btn = ttk.Button(window_jurnal, text='Отсортировать по времени',
                            command=lambda: self.sort_jurnal(do_list, tree))
      sort_btn.pack()

  def list_user(self):
      window_list_user = Toplevel()
      window_list_user.geometry('500x300')
      window_list_user.title('Список пользователей')
      window_list_user.resizable(width=False, height=False)
      window_list_user['bg'] = 'orange'


      with open('profile.txt', 'r') as file:
          user = file.read().split('\n')


      do_list = [item.split(',') for item in user[:-1]]
      columns = ['пользователь', 'пароль']


      tree = ttk.Treeview(window_list_user, columns=columns, show="headings")
      tree.pack(fill=BOTH, expand=1)
      tree.heading("пользователь", text="пользователь")
      tree.heading("пароль", text="пароль")


      for person in do_list:
          tree.insert("", END, values=person)


      delete_button = ttk.Button(window_list_user, text='Delete Selected', command=lambda: self.delete_selected(tree))
      delete_button.pack(pady=10)


  def delete_selected(self, tree):
      # Получаем выделенный элемент
      selected_item = tree.selection()
      # Удаляем выделенный элемент, если есть
      if selected_item:
          values = tree.item(selected_item, 'values')


          # Удаляем выделенный элемент из дерева
          tree.delete(selected_item)


          # Удаляем пользователя из файла
          with open('profile.txt', 'r') as file:
              data = file.readlines()


          with open('profile.txt', 'w') as file:
              for line in data:
                  if not all(value in line for value in values):
                      file.write(line)


  def registration(self):
      registration_window = Toplevel(self.root)
      registration_window.geometry('500x300')
      registration_window.title('Регистрация')
      registration_window.resizable(width=False, height=False)
      registration_window['bg'] = 'orange'


      main_label = ttk.Label(registration_window, text='Регистрация', font='Arial 15', foreground='brown')
      main_label.pack()


      username_label = ttk.Label(registration_window, text='Имя пользователя', font='Arial 15', foreground='brown')
      username_label.pack()


      username_entry = ttk.Entry(registration_window, font='Arial 15', background='white', foreground='black')
      username_entry.pack()


      password_label = ttk.Label(registration_window, text='Пароль', font='Arial 15', foreground='brown')
      password_label.pack()


      password_entry = ttk.Entry(registration_window, font='Arial 15', background='white', foreground='black')
      password_entry.pack()


      send_btn = ttk.Button(registration_window, text='Сгенерировать пароль', command=lambda: self.gen_password(password_entry))
      send_btn.pack()


      registr_btn = ttk.Button(registration_window, text='Зарегистрироваться', command=lambda: self.click_reg(username_entry, password_entry, registration_window))
      registr_btn.pack()


  def authorization(self):
      auth_window = Toplevel(self.root)
      auth_window.geometry('500x300')
      auth_window.title('Авторизация')
      auth_window.resizable(width=False, height=False)
      auth_window['bg'] = 'orange'


      main_label = ttk.Label(auth_window, text='Авторизация', font='Arial 15', foreground='brown')
      main_label.pack()


      username_label = ttk.Label(auth_window, text='Имя пользователя', font='Arial 15', foreground='brown')
      username_label.pack()


      username_entry = ttk.Entry(auth_window, font='Arial 15', background='white', foreground='black')
      username_entry.pack()


      password_label = ttk.Label(auth_window, text='Пароль', font='Arial 15', foreground='brown')
      password_label.pack()


      password_entry = ttk.Entry(auth_window, font='Arial 15', background='white', foreground='black')
      password_entry.pack()


      send_btn = ttk.Button(auth_window, text='Авторизироваться', command=lambda: self.click_auth(username_entry, password_entry, auth_window, send_btn))
      send_btn.pack()


  def click_reg(self, username_entry, password_entry, registration_window):
      username = username_entry.get()
      password = password_entry.get()


      with open(self.users_file, 'r') as file_1:
          users = file_1.read().split('\n')


      for user in users:
          if user.split(',')[0] == username:
              messagebox.showinfo(message='Такой пользователь уже существует')
              with open(self.audit_file, 'a') as file_2:
                  file_2.write(f'Попытка зарегистрировать уже существующего пользователя, {username}, {datetime.datetime.now()}\n')
              return


      messagebox.showinfo('Регистрация успешно прошла', f'{username}, {password}')
      with open(self.users_file, 'a') as file:
          file.write(f'{username},{password}\n')


      with open(self.audit_file, 'a') as file_2:
          file_2.write(f'Зарегистрирован пользователь, {username}, {datetime.datetime.now()}\n')


      registration_window.destroy()


  def click_auth(self, username_entry, password_entry, auth_window, send_btn):
      username = username_entry.get()
      password = password_entry.get()
      with open(self.users_file, 'r') as file:
          users = file.read().split('\n')


      for user in users:
          if user.split(',')[0] == username and user.split(',')[1] == password:
              messagebox.showinfo(message='Вы успешно авторизировались')
              with open(self.audit_file, 'a') as file_2:
                  file_2.write(f'Пользователь вошел в личный кабинет, {username}, {datetime.datetime.now()}\n')
              auth_window.destroy()
              self.kabinet(username)
              return
      self.counter_try += 1
      messagebox.showinfo(message='Неправильно введен логин или пароль')
      if self.counter_try == 3:
          if auth_window.winfo_exists():  # Проверяем, существует ли окно
              send_btn.config(state="disabled")
              auth_window.after(5000, lambda: send_btn.config(state="normal"))
      with open(self.audit_file, 'a') as file_2:
          file_2.write(f'Попытка авторизации пользователя, {username}, {datetime.datetime.now()}\n')


  def gen_password(self, password_entry):
      size = 9
      q = size % 5 + 1
      alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
      symbols = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*']
      password = ''
      number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]


      for i in range(q):
          password += symbols[random.randint(0, 9)]


      for i in range(size - q):
          if len(password) == 8:
              password += str(number[random.randint(0, 9)])
          else:
              password += alpha[random.randint(0, 25)]


      password_entry.delete(0, END)
      password_entry.insert(0, password)




if __name__ == "__main__":
  app = LibraryApp()


