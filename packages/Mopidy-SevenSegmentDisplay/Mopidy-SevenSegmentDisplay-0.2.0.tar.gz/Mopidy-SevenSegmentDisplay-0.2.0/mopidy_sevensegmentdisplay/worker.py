from __future__ import unicode_literals

import logging
from time import sleep
import json
from threader import Threader
from music import Music
from display import Display
from ir import IrSender, IrReceiver
from gpio import Gpio
from timer import TimerOn, TimerOff, TimerAlert
from clock import Time, Date
from menu import Menu
from max7219 import Symbols
from alert import Alert


class Worker(Threader):
    core = None
    music = None
    display = None
    ir_sender = None
    ir_receiver = None
    gpio = None
    timer_on = None
    timer_off = None
    timer_alert = None
    time = None
    date = None
    menu = None

    response_code = None

    def start(self, config, core):
        self.config = config
        self.core = core
        super(Worker, self).start()

    def run(self):
        try:
            self.music = Music(self.core, self.config['default_song'])
            self.display = Display()
            self.ir_sender = IrSender()
            self.ir_receiver = IrReceiver(self.play_stop_music,
                                          self.on_menu_click,
                                          self.on_menu_click_left,
                                          self.on_menu_click_right,
                                          self.music.decrease_volume,
                                          self.music.increase_volume,
                                          self.music.mute,
                                          self.on_preset)
            self.gpio = Gpio(self.play_stop_music, self.on_menu_click, self.on_menu_click_left, self.on_menu_click_right, self.ir_sender)
            self.timer_on = TimerOn(self.play_music)
            self.timer_off = TimerOff(self.stop_music)
            self.timer_alert = TimerAlert(Alert(self.display, self.gpio, json.loads(self.config['alert_files'])).run)
            self.time = Time()
            self.date = Date([self.timer_on, self.timer_off, self.timer_alert])
            self.menu = Menu(self.display,
                             self.get_menu(),
                             [self.time, self.date, self.timer_on, self.timer_off, self.timer_alert],
                             self.config['display_min_brightness'],
                             self.config['display_max_brightness'],
                             self.config['display_off_time_from'],
                             self.config['display_off_time_to'])

            self.ir_receiver.start()

            while True:
                self.menu.run()

                if (self.stopped()):
                    break
                else:
                    sleep(1)

        except Exception as inst:
            logging.error(inst)
        finally:
            self.ir_receiver.stop()
            self.display.shutdown()
            self.gpio.cleanup()

    def get_menu(self):
        return [
            {
                "click_left": self.decrease_timer,
                "click_right": self.increase_timer,
                "sub_menu": [
                    {
                        "get_buffer": lambda: [0, Symbols.T1, Symbols.T2, Symbols.I, Symbols.M1, Symbols.M2, Symbols.E, Symbols.R],
                        "sub_menu": [
                            {
                                "get_buffer": lambda: [0, Symbols.A, Symbols.L, Symbols.E, Symbols.R, Symbols.T1, Symbols.T2, 0],
                                "sub_menu": [
                                    {
                                        "get_buffer": lambda: [0, 0, 0, Symbols.A, Symbols.D, Symbols.D, 0, 0],
                                        "sub_menu": [
                                            {
                                                "get_buffer": self.timer_alert.get_draw_menu_buffer,
                                                "click": lambda: (self.timer_alert.add_timer(),
                                                                  self.display.draw(self.timer_alert.get_draw_menu_buffer())),
                                                "click_left": self.timer_alert.decrease,
                                                "click_right": self.timer_alert.increase
                                            }
                                        ]
                                    },
                                    {
                                        "get_buffer": lambda: [0, 0, Symbols.C, Symbols.L, Symbols.E, Symbols.A, Symbols.R, 0],
                                        "click": self.timer_alert.reset,
                                        "click_animation": True
                                    },
                                ]
                            },
                            {
                                "get_buffer": lambda: [0, 0, 0, Symbols.O, Symbols.F, Symbols.F, 0, 0],
                                "sub_menu": [
                                    {
                                        "get_buffer": self.timer_off.get_draw_buffer,
                                        "click_left": self.timer_off.decrease,
                                        "click_right": self.timer_off.increase
                                    }
                                ]
                            },
                            {
                                "get_buffer": lambda: [0, 0, 0, Symbols.O, Symbols.N, 0, 0, 0],
                                "sub_menu": [
                                    {
                                        "get_buffer": self.timer_on.get_draw_buffer,
                                        "click_left": self.timer_on.decrease,
                                        "click_right": self.timer_on.increase
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "get_buffer": lambda: [0, Symbols.P, Symbols.L, Symbols.A, Symbols.Y, 0, Symbols.NUMBER[1], 0],
                        "click": lambda: self.play_music([self.music.get_default_song()])
                    },
                    {
                        "get_buffer": lambda: [0, Symbols.U, Symbols.O, Symbols.L, Symbols.U, Symbols.M1, Symbols.M2, Symbols.E],
                        "sub_menu": [
                            {
                                "get_buffer": self.music.get_draw_volume,
                                "click_left": self.music.decrease_volume,
                                "click_right": self.music.increase_volume
                            }
                        ]
                    },
                    {
                        "get_buffer": lambda: [0, Symbols.S, Symbols.T1, Symbols.T2, Symbols.Y, Symbols.L, Symbols.E, 0],
                        "sub_menu": list(map(lambda x: {
                            "get_buffer": lambda: x["buffer"],
                            "click": lambda: self.music.set_preset(x["name"]),
                            "click_animation": True
                        }, Music.PRESETS))
                    },
                    {
                        "get_buffer": lambda: [0, 0, Symbols.D, Symbols.E, Symbols.M1, Symbols.M2, Symbols.O, 0],
                        "click": lambda: self.menu.draw_sub_menu_animation(self.music.get_draw_equalizer_animation())
                    }
                ]
            }
        ]

    def on_menu_click(self):
        self.menu.click()

    def on_menu_click_left(self):
        self.menu.click_left()

    def on_menu_click_right(self):
        self.menu.click_right()

    def increase_timer(self):
        if (self.music.is_playing()):
            self.timer_off.increase()
            self.menu.draw_sub_menu(self.timer_off.get_draw_buffer())
        else:
            self.timer_on.increase()
            self.menu.draw_sub_menu(self.timer_on.get_draw_buffer())

    def decrease_timer(self):
        if (self.music.is_playing()):
            self.timer_off.decrease()
            self.menu.draw_sub_menu(self.timer_off.get_draw_buffer())
        else:
            self.timer_on.decrease()
            self.menu.draw_sub_menu(self.timer_on.get_draw_buffer())

    def get_volume(self):
        return self.music.get_volume()

    def set_volume(self, volume):
        self.music.set_volume(volume)

    def get_state(self):
        return self.music.get_state()

    def play_stop_music(self):
        if (self.music.is_playing()):
            self.stop_music()
        else:
            self.play_music()

    def play_music(self, tracks=None):
        self.music.play(tracks)
        self.on_started()

    def pause_music(self):
        self.music.pause()
        self.on_paused()

    def stop_music(self):
        self.music.stop()
        self.on_stopped()

    def on_preset(self, preset):
        self.menu.draw_sub_menu(self.music.set_preset(preset))

    def on_started(self):
        self.menu.draw_sub_menu_animation(self.music.get_draw_start_animation())

    def on_stopped(self):
        self.menu.draw_sub_menu_animation(self.music.get_draw_stop_animation())
        self.timer_off.reset()
        self.gpio.switch_relay_off()

    def on_playing(self):
        self.menu.draw_sub_menu_animation(self.music.get_draw_play_animation())
        self.timer_on.reset()
        if (self.music.is_playing()):
            self.gpio.switch_relay_on()

    def on_paused(self):
        self.menu.draw_sub_menu_animation(self.music.get_draw_pause_animation())

    def on_seeked(self):
        self.menu.draw_sub_menu_animation(self.music.get_draw_seek_animation())

    def on_mute(self, mute):
        if mute:
            self.on_volume_changed(0)
        else:
            self.on_volume_changed()

    def on_volume_changed(self, volume=None):
        if (self.menu is not None and self.music is not None and self.music.is_volume_changed(volume)):
            self.menu.draw_sub_menu(self.music.get_draw_volume(volume))

    def on_playback_state_changed(self, old_state, new_state):
        if (old_state != new_state):
            if (self.music.is_playing(new_state)):
                self.on_playing()
            elif (self.music.is_paused(new_state)):
                self.on_paused()
