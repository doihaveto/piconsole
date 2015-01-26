import wiringpi2 as wiringpi
import subprocess
from . import settings
from time import sleep
from lockfile import LockFile, NotLocked, LockTimeout

lock = LockFile('.pcpower.lock')

def _gpio_export(pin, mode='in', unexport=False):
    if unexport:
        p = subprocess.Popen(['gpio', 'unexport', str(pin)])    
    else:
        p = subprocess.Popen(['gpio', 'export', str(pin), str(mode)])
    return p.communicate()

def _gpio_cleanup(pc):
    _gpio_export(settings.PCS[pc]['gpio']['power'], unexport=True)
    _gpio_export(settings.PCS[pc]['gpio']['mains_power'], unexport=True)
    _gpio_export(settings.PCS[pc]['gpio']['power_led'], unexport=True)

def gpio_setup(pc):
    _gpio_cleanup(pc)
    _gpio_export(settings.PCS[pc]['gpio']['power'], 'out')
    _gpio_export(settings.PCS[pc]['gpio']['mains_power'], 'out')
    _gpio_export(settings.PCS[pc]['gpio']['power_led'], 'in')
    wiringpi.wiringPiSetupSys()
    wiringpi.pinMode(settings.PCS[pc]['gpio']['power'], 1)
    wiringpi.pinMode(settings.PCS[pc]['gpio']['mains_power'], 1)
    wiringpi.pinMode(settings.PCS[pc]['gpio']['power_led'], 0)

def gpio_status(pc):
    power_status = wiringpi.digitalRead(settings.PCS[pc]['gpio']['power'])
    mains_power = wiringpi.digitalRead(settings.PCS[pc]['gpio']['mains_power'])
    power_led = wiringpi.digitalRead(settings.PCS[pc]['gpio']['power_led'])
    if settings.PCS[pc]['mains_normally_closed']:
        mains_power = mains_power^1
    return bool(power_status), bool(mains_power), bool(power_led)

def power_click(pc, secs):
    try:
        lock.acquire(timeout=0.5)
        wiringpi.digitalWrite(settings.PCS[pc]['gpio']['power'], 1)
        sleep(secs)
        wiringpi.digitalWrite(settings.PCS[pc]['gpio']['power'], 0)
    except LockTimeout:
        raise StandardError('Already operating on this pin. Try again later.')
    finally:
        try:
            lock.release()
        except NotLocked:
            pass

def mains_power_toggle(pc, status):
    try:
        lock.acquire(timeout=0.5)
        wiringpi.digitalWrite(settings.PCS[pc]['gpio']['mains_power'], status)
    except LockTimeout:
        raise StandardError('Already operating on this pin. Try again later.')
    finally:
        try:
            lock.release()
        except NotLocked:
            pass

def network_status(host):
    ping = subprocess.Popen(['ping', '-c', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    out, error = ping.communicate()
    try:
        status = out.split('1 packets transmitted, ')[1].split(' ', 1)[0]
        if status == '1':
            return True
    except IndexError:
        return False
    return False
