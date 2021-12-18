from transitions import Machine

signal = {
    "fl_light_1": 0,
    "fl_light_2": 0,
    "fl_light_3": 0,
    "fl_light_4": 0,

    "el_light_1": 0,
    "el_light_2": 0,
    "el_light_3": 0,
    "el_light_4": 0,

    "go_up_fast": 0,
    "go_up_slow": 0,

    "go_down_fast": 0,
    "go_down_slow": 0,

    "open_doors": 0,
    "close_doors": 0
}


class Elevator(object):

    states = ['initial_search',
              'idle',
              'go_to_first_floor',
              'go_up_fast',
              'go_up_slow',
              'go_down_fast',
              'go_down_slow',
              'stopping',
              'door_opening',
              'door_opened',
              'door_closing',
              'door_closed',
              'boarding_end']

    transitions = [
        {
            'trigger': 'fl_btn',
            'source': ['idle', 'door_closed'],
            'dest': 'go_up_fast',
            'conditions': ['is_dest_fl_upper'],
            'prepare': 'set_dest',
            'after': ['set_go_up_fast']
        },
        {
            'trigger': 'fl_btn',
            'source': 'idle',
            'dest': 'door_opening',
            'conditions': ['is_dest_floor'],
            'prepare': 'set_dest',
            'after': ['set_door_opening']
        },
        {
            'trigger': 'el_btn',
            'source': ['idle', 'door_closed'],
            'dest': 'go_up_fast',
            'conditions': ['is_dest_fl_upper'],
            'prepare': 'set_dest',
            'after': ['set_go_up_fast']
        },
        {
            'trigger': 'el_btn',
            'source': 'idle',
            'dest': 'door_opening',
            'conditions': ['is_dest_floor'],
            'prepare': 'set_dest',
            'after': ['set_door_opening']
        },

        {
            'trigger': 'fl_btn',
            'source': ['idle', 'door_closed'],
            'dest': 'go_down_fast',
            'conditions': ['is_dest_fl_less'],
            'prepare': 'set_dest',
            'after': ['set_go_down_fast']
        },
        {
            'trigger': 'el_btn',
            'source': ['idle', 'door_closed'],
            'dest': 'go_down_fast',
            'conditions': ['is_dest_fl_less'],
            'prepare': 'set_dest',
            'after': ['set_go_down_fast']
        },
        {
            'trigger': 'stopping_sensor',
            'source': 'go_up_fast',
            'dest': 'go_up_slow',
            'conditions': ['is_dest_floor'],
            'prepare': 'inc_current_floor',
            'after': 'set_go_up_slow'
        },
        {
            'trigger': 'stopping_sensor',
            'source': 'go_down_fast',
            'dest': 'go_down_slow',
            'conditions': ['is_dest_floor'],
            'prepare': 'dec_current_floor',
            'after': 'set_go_down_slow'
        },
        {
            'trigger': 'stopping_sensor',
            'source': 'go_up_fast',
            'dest': 'go_up_fast',
            'conditions': ['not_dest_floor'],

        },
        {
            'trigger': 'stopping_sensor',
            'source': 'go_down_fast',
            'dest': 'go_down_fast',
            'conditions': ['not_dest_floor'],
        },

        {
            'trigger': 'stop_btn',
            'source': 'go_up_fast',
            'dest': 'go_up_slow',
            'after': 'set_go_up_slow'
        },
        {
            'trigger': 'stop_btn',
            'source': 'go_down_fast',
            'dest': 'go_down_slow',
            'after': 'set_go_down_slow'
        },

        {
            'trigger': 'floor_sensor',
            'source': ['idle', 'go_up_slow', 'go_down_slow'],
            'dest': 'door_opening',
            'conditions': ['is_dest_floor'],
            'after': 'set_door_opening'
        },

        {
            'trigger': 'door_opened_sensor',
            'source': 'door_opening',
            'dest': 'door_opened',
            'after': 'set_door_opened'
        },

        {
            'trigger': 'pass_sensor',
            'source': 'door_opened',
            'dest': 'door_closing',
            'after': 'set_door_closing'
        },

        {
            'trigger': 'door_closed_sensor',
            'source': 'door_closing',
            'dest': 'door_closed',
            'after': 'set_door_closed'
        },

        {
            'trigger': 'pass_sensor',
            'source': 'door_closed',
            'dest': 'idle',
            'after': 'set_idle'
        },

        {
            'trigger': 'start_simulation',
            'source': 'initial_search',
            'dest': 'go_down_slow',
            'after': 'set_go_down_slow'
        },
        {
            'trigger': 'zero_floor_sensor',
            'source': 'go_down_slow',
            'dest': 'go_to_first_floor',
            'before': 'set_floor',
            'after': 'set_go_up_slow'
        },
        {
            'trigger': 'floor_sensor',
            'source': 'go_to_first_floor',
            'dest': 'idle',
            'before': 'set_first_floor',
            'after': 'set_idle'
        },

        {
            'trigger': 'open_doors_btn',
            'source': ['door_closing', 'door_closed'],
            'dest': 'door_opening',
            'after': 'set_door_opening'
        },

    ]

    def __init__(self):
        self.current_floor = None
        self.dest_floor = None
        self.signal = {
            "fl_light_1": 0,
            "fl_light_2": 0,
            "fl_light_3": 0,
            "fl_light_4": 0,

            "el_light_1": 0,
            "el_light_2": 0,
            "el_light_3": 0,
            "el_light_4": 0,

            "go_up_fast": 0,
            "go_up_slow": 0,

            "go_down_fast": 0,
            "go_down_slow": 0,

            "open_doors": 0,
            "close_doors": 0
        }

        self.machine = Machine(model=self,
                               states=Elevator.states,
                               transitions=Elevator.transitions,
                               initial='initial_search')


    def get_floor_number(self, floor_code):
        floor_code_map = {
            'fl_btn_1': 1,
            'fl_btn_2': 2,
            'fl_btn_3': 3,
            'fl_btn_4': 4,
            'el_btn_1': 1,
            'el_btn_2': 2,
            'el_btn_3': 3,
            'el_btn_4': 4,
        }
        return floor_code_map[floor_code]

    def set_dest(self, btn_code):
        self.dest_floor = self.get_floor_number(btn_code)
        self.signal[btn_code] = 1

    def set_go_up_fast(self, btn):
        self.signal['go_up_fast'] = 1

    def set_go_up_slow(self, btn):
        self.signal['go_up_fast'] = 0
        self.signal['go_up_slow'] = 1

    def set_go_down_fast(self, btn):
        self.signal['go_down_fast'] = 1

    def set_go_down_slow(self, btn):
        self.signal['go_down_fast'] = 0
        self.signal['go_down_slow'] = 1

    def inc_current_floor(self, btn):
        self.current_floor += 1

    def dec_current_floor(self, btn):
        self.current_floor -= 1

    def set_door_opening(self, btn):
        self.signal['go_down_slow'] = 0
        self.signal['go_up_slow'] = 0
        self.signal['close_doors'] = 0
        self.signal['open_doors'] = 1

    def set_door_opened(self, btn):
        self.signal['open_doors'] = 0
        self.signal[f"fl_light_{self.dest_floor}"] = 0
        self.signal[f"el_light_{self.dest_floor}"] = 0

    def set_door_closing(self, btn):
        self.signal['close_doors'] = 1

    def set_door_closed(self, btn):
        self.signal['close_doors'] = 0

    def set_floor(self, btn):
        self.signal['go_down_slow'] = 0
        self.current_floor = 0
        self.dest_floor = 1

    def set_first_floor(self, btn):
        self.current_floor = 1

    def set_idle(self, btn):
        for key in self.signal:
            self.signal[key] = 0

    @property
    def is_dest_floor(self):
        return self.current_floor == self.dest_floor

    @property
    def not_dest_floor(self):
        return self.current_floor != self.dest_floor

    @property
    def is_dest_fl_upper(self):
        return self.dest_floor > self.current_floor

    @property
    def is_dest_fl_less(self):
        return self.dest_floor < self.current_floor


from flask import Flask, request

app = Flask(__name__)

elevator = Elevator()
prev_sensors = None

@app.route('/echo', methods=['GET'])
def get_tasks():
    return '', 418

@app.route('/calc', methods=['POST'])
def calc():
    sensors = request.json
    signal = get_signals(sensors)
    return signal, 200

def get_signals(sensors):
    global prev_sensors
    global elevator

    if not prev_sensors:
        elevator.trigger('start_simulation', 'start')
        prev_sensors = sensors
        return elevator.signal

    difference = {}

    for key in sensors:
        if sensors[key] != prev_sensors[key]:
            difference[key] = sensors[key]

    try:
        for key in difference:
            if key.find('fl_btn') != -1:
                elevator.trigger('fl_btn', key)
            elif key.find('el_btn') != -1:
                elevator.trigger('el_btn', key)
            else:
                elevator.trigger(key, key)
    except Exception:
        return elevator.signal

    return elevator.signal


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=5565)