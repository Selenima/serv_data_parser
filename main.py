import paramiko
import json


# Настройки подключения
  # Ваш пароль

with open('data.json', 'r') as d:
    data = json.load(d)

for d in data:
    hostname = d['ip']  # IP-адрес или доменное имя сервера
    port = d['port']  # Порт SSH, обычно 22
    username = d['username']
    password = d['password']


    try:
        # Создаем SSH клиент
        ssh_client = paramiko.SSHClient()

        # Добавляем сервер в список "доверенных", если он отсутствует
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Подключение к {hostname}")
        # Подключаемся к серверу
        ssh_client.connect(hostname, port, username, password)
        print(f"Подключение к {hostname} установлено.")
        with open('valid_ssh.txt', 'a+', encoding='utf8') as f:
            f.write(f'{hostname}:{port}:{username}:{password}\n')

        stdin, stdout, stderr = ssh_client.exec_command('ls -l')
        print("Результат выполнения команды:")
        print(stdout.read().decode())

    except paramiko.ssh_exception.SSHException as e:
        print(f'SSH ERROR: {e}')
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрываем соединение
        ssh_client.close()
        print("Соединение закрыто.")
