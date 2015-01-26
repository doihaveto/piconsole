from . import settings, utils
from flask import jsonify, render_template
from piconsole import app
from piconsole.utils import api_response

@app.route('/pcpower/<pc>/status/')
def status(pc):
    if pc not in settings.PCS:
        return jsonify(**api_response('error', 'Unknown PC'))
    try:
        network_status = utils.network_status(settings.PCS[pc]['ip'])
        power, mains_power, power_led = utils.gpio_status(pc)
        return jsonify(**api_response(data={
            'power': power,
            'power_led': power_led,
            'network': network_status,
            'mains_power': mains_power
        }))
    except StandardError as e:
        return jsonify(**api_response('error', str(e)))

@app.route('/pcpower/<pc>/power/<status>')
def power(pc, status):
    if pc not in settings.PCS:
        return jsonify(**api_response('error', 'Unknown PC'))
    if status == 'on' or status == 'soft':
        secs = 1
    elif status == 'off':
        secs = 8
    else:
        return jsonify(**api_response('error', 'Unknown status. Valid statuses are on and off'))
    try:
        utils.power_click(pc, secs)
    except StandardError as e:
        return jsonify(**api_response('error', str(e)))
    return jsonify(**api_response())

@app.route('/pcpower/<pc>/mains-power/<status>')
def mains_power(pc, status):
    if pc not in settings.PCS:
        return jsonify(**api_response('error', 'Unknown PC'))
    if status == 'on':
        status = 0
    elif status == 'off':
        status = 1
    else:
        return jsonify(**api_response('error', 'Unknown status. Valid statuses are on and off'))
    try:
        utils.mains_power_toggle(pc, status)
    except StandardError as e:
        return jsonify(**api_response('error', str(e)))
    return jsonify(**api_response())

@app.route('/pcpower/')
def pcpower():
    context = {
        'pcs': settings.PCS
    }
    return render_template('pcpower/main.html', **context)
