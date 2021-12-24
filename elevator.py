from transitions import Machine, EventData

inputs_state = {
    'fl_btn_1': 0,
    'fl_btn_2': 0,
    'fl_btn_3': 0,
    'fl_btn_4': 0,

    'el_btn_1': 0,
    'el_btn_2': 0,
    'el_btn_3': 0,
    'el_btn_4': 0,

    'open_doors_btn': 0,
    'stop_btn': 0,

    'pass_sensor': 0,
    'obstacle_sensor': 0,
    'doors_opened_sensor': 0,
    'doors_closed_sensor': 0,

    'stopping_sensor_1': 0,
    'stopping_sensor_2': 0,
    'stopping_sensor_3': 0,
    'stopping_sensor_4': 0,

    'floor_sensor_1': 0,
    'floor_sensor_2': 0,
    'floor_sensor_3': 0,
    'floor_sensor_4': 0,

    'zero_floor_sensor': 0,
    'last_floor_sensor': 0,
}

outputs_state = {
    'fl_light_1': 0,
    'fl_light_2': 0,
    'fl_light_3': 0,
    'fl_light_4': 0,

    'el_light_1': 0,
    'el_light_2': 0,
    'el_light_3': 0,
    'el_light_4': 0,

    'go_up_fast': 0,
    'go_up_slow': 0,

    'go_down_fast': 0,
    'go_down_slow': 0,

    'open_doors': 0,
    'close_doors': 0
}

machine_state = {
    'current_floor': None,
    'dest_floor': None,
    'stop': False
}


class Elevator(object):
    states = [{'name': 'init'},
              {'name': 'initial_search', 'on_enter': 'set_initial_search', 'on_exit': 'reset_initial_search'},
              {'name': 'idle', 'on_enter': 'set_idle'},

              {'name': 'go_up_fast', 'on_enter': 'set_go_up_fast', 'on_exit': 'reset_go_up_fast'},
              {'name': 'go_up_slow', 'on_enter': 'set_go_up_slow', 'on_exit': 'reset_go_up_slow'},

              {'name': 'go_down_fast', 'on_enter': 'set_go_down_fast', 'on_exit': 'reset_go_down_fast'},
              {'name': 'go_down_slow', 'on_enter': 'set_go_down_slow', 'on_exit': 'reset_go_down_slow'},

              {'name': 'doors_opening', 'on_enter': 'set_doors_opening'},
              {'name': 'doors_opened', 'on_enter': 'set_doors_opened', 'on_exit': 'reset_doors_opened'},
              {'name': 'doors_closing', 'on_enter': 'set_doors_closing'},
              {'name': 'doors_closed', 'on_enter': 'set_doors_closed'}
              ]

    transitions = [
        # init
        {
            'trigger': 'start_simulation',
            'source': 'init',
            'dest': 'initial_search',
        },

        # initial_search
        {
            'trigger': 'floor_sensor',
            'source': 'initial_search',
            'dest': 'idle',
            'after': 'set_current_floor'
        },
        {
            'trigger': 'zero_floor_sensor',
            'source': 'initial_search',
            'dest': 'idle',
            'after': 'set_current_floor'
        },

        # idle
        {
            'trigger': 'fl_btn',
            'source': 'idle',
            'dest': 'go_up_fast',
            'prepare': 'set_dest_floor',
            'after': 'turn_on_fl_btn',
            'conditions': ['is_dest_floor_upper']
        },
        {
            'trigger': 'fl_btn',
            'source': 'idle',
            'dest': 'go_down_fast',
            'after': 'turn_on_fl_btn',
            'prepare': 'set_dest_floor',
            'conditions': ['is_dest_floor_less']
        },
        {
            'trigger': 'fl_btn',
            'source': 'idle',
            'dest': 'doors_opening',
            'prepare': 'set_dest_floor',
            'conditions': ['is_dest_floor']
        },

        # go_up_fast
        {
            'trigger': 'stopping_sensor',
            'source': 'go_up_fast',
            'dest': 'go_up_fast',
            'prepare': 'inc_current_floor',
            'conditions': ['not_is_dest_floor']
        },
        {
            'trigger': 'stopping_sensor',
            'source': 'go_up_fast',
            'dest': 'go_up_slow',
            'conditions': ['is_dest_floor']
        },
        {
            'trigger': 'stop_btn',
            'source': 'go_up_fast',
            'dest': 'go_up_slow',
            'before': 'set_nearest_dest_floor'
        },

        # go_down_fast
        {
            'trigger': 'stopping_sensor',
            'source': 'go_down_fast',
            'dest': 'go_down_fast',
            'prepare': 'dec_current_floor',
            'conditions': ['not_is_dest_floor']
        },
        {
            'trigger': 'stopping_sensor',
            'source': 'go_down_fast',
            'dest': 'go_down_slow',
            'conditions': ['is_dest_floor']
        },
        {
            'trigger': 'stop_btn',
            'source': 'go_down_fast',
            'dest': 'go_down_slow',
            'before': 'set_nearest_dest_floor'
        },

        # go_common
        {
            'trigger': 'floor_sensor',
            'source': ['go_up_slow', 'go_down_slow'],
            'dest': 'doors_opening',
            'conditions': ['is_dest_floor']
        },

        # doors_opening
        {
            'trigger': 'doors_opened_sensor',
            'source': 'doors_opening',
            'dest': 'doors_opened',
        },

        # doors_opened
        {
            'trigger': 'pass_sensor',
            'source': 'doors_opened',
            'dest': 'doors_closing',
        },

        # doors_closing
        {
            'trigger': 'doors_closed_sensor',
            'source': 'doors_closing',
            'dest': 'doors_closed',
        },
        {
            'trigger': 'obstacle_sensor',
            'source': 'doors_closing',
            'dest': 'doors_opening',
        },
        {
            'trigger': 'doors_open_btn',
            'source': 'doors_closing',
            'dest': 'doors_opening',
        },

        # doors_closed
        {
            'trigger': 'doors_open_btn',
            'source': 'doors_closed',
            'dest': 'doors_opening',
        },
        {
            'trigger': 'el_btn',
            'source': 'doors_closed',
            'dest': 'go_up_fast',
            'prepare': 'set_dest_floor',
            'after': 'turn_on_el_btn',
            'conditions': ['is_dest_floor_upper']
        },
        {
            'trigger': 'el_btn',
            'source': 'doors_closed',
            'dest': 'go_down_fast',
            'prepare': 'set_dest_floor',
            'after': 'turn_on_el_btn',
            'conditions': ['is_dest_floor_less']
        },
        {
            'trigger': 'el_btn',
            'source': 'doors_closed',
            'dest': 'doors_opening',
            'prepare': 'set_dest_floor',
            'conditions': ['is_dest_floor']
        },
        {
            'trigger': 'pass_sensor',
            'source': 'doors_closed',
            'dest': 'idle',
        },
    ]

    def __init__(self):
        self.inputs_state = {
            'fl_btn_1': 0,
            'fl_btn_2': 0,
            'fl_btn_3': 0,
            'fl_btn_4': 0,

            'el_btn_1': 0,
            'el_btn_2': 0,
            'el_btn_3': 0,
            'el_btn_4': 0,

            'open_doors_btn': 0,
            'stop_btn': 0,

            'pass_sensor': 0,
            'obstacle_sensor': 0,
            'doors_opened_sensor': 0,
            'doors_closed_sensor': 0,

            'stopping_sensor_1': 0,
            'stopping_sensor_2': 0,
            'stopping_sensor_3': 0,
            'stopping_sensor_4': 0,

            'floor_sensor_1': 0,
            'floor_sensor_2': 0,
            'floor_sensor_3': 0,
            'floor_sensor_4': 0,

            'zero_floor_sensor': 0,
            'last_floor_sensor': 0,
        }

        self.outputs_state = {
            'fl_light_1': 0,
            'fl_light_2': 0,
            'fl_light_3': 0,
            'fl_light_4': 0,

            'el_light_1': 0,
            'el_light_2': 0,
            'el_light_3': 0,
            'el_light_4': 0,

            'go_up_fast': 0,
            'go_up_slow': 0,

            'go_down_fast': 0,
            'go_down_slow': 0,

            'open_doors': 0,
            'close_doors': 0
        }

        self.machine_state = {
            'current_floor': None,
            'dest_floor': None,
            'stop': False
        }

        self.machine = Machine(model=self,
                               states=Elevator.states,
                               transitions=Elevator.transitions,
                               initial='init',
                               send_event=True)

    def set_initial_search(self, event: EventData):
        self.outputs_state['go_down_slow'] = 1

    def reset_initial_search(self, event: EventData):
        self.outputs_state['go_down_slow'] = 0

    def set_idle(self, event: EventData):
        for key in self.outputs_state:
            self.outputs_state[key] = 0

    def set_go_up_fast(self, event: EventData):
        self.outputs_state['go_up_fast'] = 1

    def reset_go_up_fast(self, event: EventData):
        self.outputs_state['go_up_fast'] = 0

    def set_go_up_slow(self, event: EventData):
        self.outputs_state['go_up_slow'] = 1

    def reset_go_up_slow(self, event: EventData):
        self.outputs_state['go_up_slow'] = 0

    def set_go_down_fast(self, event: EventData):
        self.outputs_state['go_down_fast'] = 1

    def reset_go_down_fast(self, event: EventData):
        self.outputs_state['go_down_fast'] = 0

    def set_go_down_slow(self, event: EventData):
        self.outputs_state['go_down_slow'] = 1

    def reset_go_down_slow(self, event: EventData):
        self.outputs_state['go_down_slow'] = 0

    def set_doors_opening(self, event: EventData):
        self.outputs_state['open_doors'] = 1

    def set_doors_opened(self, event: EventData):
        self.outputs_state['open_doors'] = 0

        self.outputs_state['fl_light_1'] = 0
        self.outputs_state['fl_light_2'] = 0
        self.outputs_state['fl_light_3'] = 0
        self.outputs_state['fl_light_4'] = 0

        self.outputs_state['el_light_1'] = 0
        self.outputs_state['el_light_2'] = 0
        self.outputs_state['el_light_3'] = 0
        self.outputs_state['el_light_4'] = 0

    def set_doors_closing(self, event: EventData):
        self.outputs_state['close_doors'] = 1

    def set_doors_closed(self, event: EventData):
        self.outputs_state['close_doors'] = 0

    def set_current_floor(self, event: EventData):
        floor_sensor_code = event.kwargs.get('floor_sensor_code')
        self.machine_state['current_floor'] = int(floor_sensor_code[-1])

    def set_dest_floor(self, event: EventData):
        btn_code = event.kwargs.get('btn_code')
        self.machine_state['dest_floor'] = int(btn_code[-1])

    def inc_current_floor(self, event: EventData):
        self.machine_state['current_floor'] += 1

    def dec_current_floor(self, event: EventData):
        self.machine_state['current_floor'] -= 1

    def turn_on_el_btn(self, event: EventData):
        self.outputs_state[f"el_light_{self.machine_state['dest_floor']}"] = 1

    def turn_on_fl_btn(self, event: EventData):
        self.outputs_state[f"fl_light_{self.machine_state['dest_floor']}"] = 1

    def is_dest_floor(self, event: EventData):
        return self.machine_state['current_floor'] == self.machine_state['dest_floor']

    def not_is_dest_floor(self, event: EventData):
        return self.machine_state['current_floor'] != self.machine_state['dest_floor']

    def is_dest_floor_upper(self, event: EventData):
        return self.machine_state['current_floor'] < self.machine_state['dest_floor']

    def is_dest_floor_less(self, event: EventData):
        return self.machine_state['current_floor'] > self.machine_state['dest_floor']


# def print_elevator_state(trigger, signal, current_floor, dest_floor, new_state):
#     print("--------------------------------------------")
#     print(f"Триггрер: {trigger}")
#     print("Сигнал: ", signal)
#     print(f"Новое состояние: {new_state}")
#     print(f"Текущий этаж: {current_floor}")
#     print(f"Нужный этаж: {dest_floor}")
#     print("---------------------------------------------")
#
# def menu(triggers):
#     for indx, value in enumerate(triggers):
#         print(f"{indx} -- {value}")
#     print("-1 -- exit")
#
# elevator = Elevator()
#
# triggers = [
#     "start_simulation",
#     "fl_btn_1",
#     "fl_btn_2",
#     "fl_btn_3",
#     "fl_btn_4",
#     "el_btn_1",
#     "el_btn_2",
#     "el_btn_3",
#     "el_btn_4",
#     "open_doors_btn",
#     "pass_sensor",
#     "obstacle_sensor",
#     "doors_opened_sensor",
#     "doors_closed_sensor",
#     "stopping_sensor_1",
#     "stopping_sensor_2",
#  "stopping_sensor_3",
# "stopping_sensor_4",
#     "floor_sensor_1",
# "floor_sensor_2",
# "floor_sensor_3",
# "floor_sensor_4",
#     "zero_floor_sensor"
# ]
#
# while(True):
#     menu(triggers)
#     i = int(input("Триггер: "))
#
#     if i == -1:
#         break
#
#     try:
#         if triggers[i].find('fl_btn') != -1:
#             elevator.trigger('fl_btn', btn_code=triggers[i])
#         elif triggers[i].find('el_btn') != -1:
#             elevator.trigger('el_btn', btn_code=triggers[i])
#         elif triggers[i].find('stopping_sensor') != -1:
#             elevator.trigger('stopping_sensor', stopping_sensor_code=triggers[i])
#         elif triggers[i].find('floor_sensor') != -1:
#             elevator.trigger('floor_sensor', floor_sensor_code=triggers[i])
#         else:
#             elevator.trigger(triggers[i])
#
#         print_elevator_state(triggers[i], elevator.outputs_state, elevator.machine_state['current_floor'], elevator.machine_state['dest_floor'], elevator.state)
#     except Exception as e:
#         print(e)
from transitions.extensions import GraphMachine

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

elevator = Elevator()
graph = GraphMachine(model=elevator, states=elevator.states, transitions=elevator.transitions, show_conditions=True)
elevator.get_graph().draw('new_state_diagram.png', prog='dot')

prev_sensors = None


@app.route('/echo', methods=['GET'])
def get_tasks():
    return '', 418


@app.route('/calc', methods=['POST'])
def calc():
    global elevator
    sensors = request.json
    signal = get_signals(sensors)
    signal['machine_state'] = elevator.machine_state
    return signal, 200


@app.route('/refresh', methods=['PATCH'])
def refresh():
    global elevator
    global prev_sensors
    prev_sensors = None
    elevator = Elevator()
    return '', 200


def get_signals(sensors):
    global prev_sensors
    global elevator

    if not prev_sensors:
        elevator.trigger('start_simulation', 'start')
        prev_sensors = sensors
        return elevator.outputs_state

    difference = {}

    for key in sensors:
        if (sensors[key] == 1 and prev_sensors[key] == 0) or \
                (sensors[key] != prev_sensors[key] == 0 and key == 'pass_sensor'):
            difference[key] = sensors[key]

    try:
        for key in difference:
            if key.find('fl_btn') != -1:
                elevator.trigger('fl_btn', btn_code=key)
            elif key.find('el_btn') != -1:
                elevator.trigger('el_btn', btn_code=key)
            elif key.find('stopping_sensor') != -1:
                elevator.trigger('stopping_sensor', stopping_sensor_code=key)
            elif key.find('floor_sensor') != -1:
                elevator.trigger('floor_sensor', floor_sensor_code=key)
            else:
                elevator.trigger(key)
    except Exception:
        return elevator.outputs_state

    return elevator.outputs_state


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=5565)
