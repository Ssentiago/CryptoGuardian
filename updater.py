import subprocess
import time

GIT_REPO = r'https://github.com/Ssentiago/CryptoGuardian'

print

while True:
    remote_hash = subprocess.check_output(['git', 'ls-remote', GIT_REPO, 'HEAD']).decode('utf-8').split()[0]
    local_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8')

    if local_hash != remote_hash:
        print('Обнаружены изменения в удалённом репозитории...')
        subprocess.call(['sudo', 'git', 'pull'])
        print('Изменения из удалённого репозитория успешно объединены с локальным репозиторием')


        time.sleep(1200)
