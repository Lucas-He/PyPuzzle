# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 10:49:33 2018

@author: Lucas
"""

import tkinter as tk  # use a capital T for python 2.
import copy
import os
import numpy as np

class Puzzle(tk.Frame):
    def __init__(self, parent):
        with open(os.path.join(os.getcwd(), "levels_info_puzzle.txt"),"r") as f:
            self.level_info = f.readlines()
        self.level_cap = int(self.level_info[-1].split("\t")[-1].split("\n")[0])
        tk.Frame.__init__(self, parent, width=680, height=690)
        parent.bind('<Left>', self.leftkey)
        parent.bind('<Right>', self.rightkey)
        parent.bind('<Up>', self.upkey)
        parent.bind('<Down>', self.downkey)
        # Start
        self.play_button = tk.Button(self, text="Play", command=self.play_free_mode)
        self.play_button.pack(side="right")
        self.play_button.place(y=5, x=5, height=30, width=50)
        # Reset
        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack(side="right")
        self.reset_button.place(y=5, x=55, height=30, width=50)
        # Edit
        self.edit_button = tk.Button(self, text="Start", command=self.edit_field)
        self.edit_button.pack(side="right")
        self.edit_button.place(y=5, x=325, height=30, width=50)
        # Repeat_Last_Moves
        self.last_moves_button = tk.Button(self, text="Repeat", command=self.last_moves)
        self.last_moves_button.pack(side="right")
        self.last_moves_button.place(y=5, x=480, height=30, width=50)
        # Save_Last_Moves
        self.last_moves_button = tk.Button(self, text="Save moves", command=self.save_last_moves)
        self.last_moves_button.pack(side="right")
        self.last_moves_button.place(y=5, x=530, height=30, width=80)
        # Timer
        self.timer_label = tk.Label(self, text="", anchor="w")
        self.timer_label.pack(side="left")
        self.timer_label.place(y=5, x=380, height=30, width=40)
        # Keys
        self.keys_label = tk.Label(self, text="", anchor="w")
        self.keys_label.pack(side="left")
        self.keys_label.place(y=5, x=420, height=30, width=60)
        # Load
        self.load_button = tk.Button(self, text="Load", command=self.load_field)
        self.load_button.pack(side="right")
        self.load_button.place(y=5, x=275, height=30, width=50)
        # Save
        self.save_button = tk.Button(self, text="Save", command=self.save_field)
        self.save_button.pack(side="right")
        self.save_button.place(y=5, x=225, height=30, width=50)
        # Level Selection
        var = tk.DoubleVar(value=0)
        self.level_select = tk.Spinbox(self, from_=0, to=self.level_cap, textvariable=var)
        self.level_select.pack(side="right")
        self.level_select.place(y=5, x=175, height=30, width=50)
        self.level_select['state'] = 'readonly'
        # Text output
        self.text_output = tk.Label(self, text="", anchor="w")
        self.text_output.pack(side="left")
        self.text_output.place(y=5, x=105, height=30, width=60)
        #--------------------#
        self.pic_empty = tk.PhotoImage(file="Puzzle_pics/Empty.GIF")
        self.pic_wall = tk.PhotoImage(file="Puzzle_pics/Wall.GIF")
        self.pic_player = tk.PhotoImage(file="Puzzle_pics/Player.GIF")
        self.pic_home = tk.PhotoImage(file="Puzzle_pics/Home.GIF")
        self.pic_brownbox = tk.PhotoImage(file="Puzzle_pics/BrownBox.GIF")
        self.pic_boxreq = tk.PhotoImage(file="Puzzle_pics/BoxRequired.GIF")
        self.pic_button = tk.PhotoImage(file="Puzzle_pics/Button.GIF")
        self.pic_buttonwall = tk.PhotoImage(file="Puzzle_pics/PassableWall.GIF")
        self.pic_bluebox = tk.PhotoImage(file="Puzzle_pics/BlueBox.GIF")
        self.pic_reverse = tk.PhotoImage(file="Puzzle_pics/Reverse.GIF")
        self.pic_reverse_lr = tk.PhotoImage(file="Puzzle_pics/Reverse_lr.GIF")
        self.pic_reverse_ud = tk.PhotoImage(file="Puzzle_pics/Reverse_ud.GIF")
        self.pic_invisible = tk.PhotoImage(file="Puzzle_pics/Invisible.GIF")
        self.pic_invisible_rev = tk.PhotoImage(file="Puzzle_pics/Invisible_rev.GIF")
        self.pic_timer = tk.PhotoImage(file="Puzzle_pics/Timer.GIF")
        self.pic_kill = tk.PhotoImage(file="Puzzle_pics/Kill.GIF")
        self.pic_key = tk.PhotoImage(file="Puzzle_pics/Key.GIF")
        self.pic_keyhole = tk.PhotoImage(file="Puzzle_pics/Keyhole.GIF")
        self.pic_hkey = tk.PhotoImage(file="Puzzle_pics/HKey.GIF")
        self.pic_hkeyhole = tk.PhotoImage(file="Puzzle_pics/HKeyhole.GIF")
        self.pic_ikey = tk.PhotoImage(file="Puzzle_pics/IKey.GIF")
        self.pic_ikeyhole = tk.PhotoImage(file="Puzzle_pics/IKeyhole.GIF")
        self.parent = parent
        self.current_level = 0
        self.field = []
        self.current_field = []
        self.started = False
        self.won = False
        self.possesed_keys = 0
        self.lost = False
        self.good_to_go = True
        self.timer_started = False
        self.reverse_lr = False
        self.reverse_ud = False
        self.invisible = False
        self.button_active = False
        self.current_object = 0
        self.player_pos = 0
        self.stopped = True
        self.field_len = 20
        self.time_left = 60
        self.button_count = 0
        self.object_button_count = 0
        self.field_buttons = []
        self.object_buttons = []
        self.object_dict = {0: {"Name": "Empty", "pic": self.pic_empty, "count": 322, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            1: {"Name": "Wall", "pic": self.pic_wall, "count": 78, "min_count": 0, "max_count": 400, "passable": False, "movable": False},
                            2: {"Name": "Player", "pic": self.pic_player, "count": 0, "min_count": 1, "max_count": 1},
                            3: {"Name": "Home", "pic": self.pic_home, "count": 0, "min_count": 1, "max_count": 1, "passable": True, "movable": False},
                            4: {"Name": "Brownbox", "pic": self.pic_brownbox, "count": 0, "min_count": 0, "max_count": 400, "passable": False, "movable": True},
                            5: {"Name": "Chesreq", "pic": self.pic_boxreq, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            6: {"Name": "Button", "pic": self.pic_button, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            7: {"Name": "Button_wall", "pic": self.pic_buttonwall, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            8: {"Name": "Invis_chest", "pic": self.pic_bluebox, "count": 0, "min_count": 0, "max_count": 400, "passable": False, "movable": True},
                            9: {"Name": "Reverse", "pic": self.pic_reverse, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            10: {"Name": "Invis", "pic": self.pic_invisible, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            11: {"Name": "Timer", "pic": self.pic_timer, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            12: {"Name": "Kill", "pic": self.pic_kill, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            13: {"Name": "Key", "pic":self.pic_key, "count":0, "min_count":0, "max_count": 400, "passable": True, "movable":False},
                            14: {"Name": "Keyhole", "pic":self.pic_keyhole, "count":0, "min_count":0, "max_count": 400, "passable": False, "movable":False},
                            15: {"Name": "HKey", "pic":self.pic_hkey, "count":0, "min_count":0, "max_count": 400, "passable": False, "movable":True},
                            16: {"Name": "HKeyhole", "pic":self.pic_hkeyhole, "count":0, "min_count":0, "max_count": 400, "passable": False, "movable":False},
                            17: {"Name": "IKey", "pic":self.pic_ikey, "count":0, "min_count":0, "max_count": 400, "passable": False, "movable":True},
                            18: {"Name": "IKeyhole", "pic":self.pic_ikeyhole, "count":0, "min_count":0, "max_count": 400, "passable": False, "movable":False},
                            19: {"Name": "Invisrev", "pic": self.pic_invisible_rev, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            20: {"Name": "Reverse_lr", "pic": self.pic_reverse_lr, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False},
                            21: {"Name": "Reverse_ud", "pic": self.pic_reverse_ud, "count": 0, "min_count": 0, "max_count": 400, "passable": True, "movable": False}}
        self.move_list = []
        self.save_move_list = [3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 3, 3, 0, 1, 2, 1, 0, 0, 0, 0, 0, 3, 0, 0, 1, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1, 3, 0, 2, 3, 3, 3, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 2, 2, 2, 2, 1, 0, 0, 0, 3, 0, 1, 1, 1, 3, 3, 3, 2, 2, 2, 2, 1, 1, 0, 0, 3, 0, 1, 1, 1, 3, 3, 2, 2, 2, 1, 1, 1, 0, 3, 3, 2, 3, 0, 0, 3, 0, 1, 1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 0, 2, 3, 3, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 2, 3, 3, 0, 0, 0, 0, 1, 1, 1, 1, 3, 3, 3, 3, 2, 1, 3, 2, 2, 2, 1, 1, 0, 0, 0, 3, 0, 1, 1, 3, 3, 2, 3, 2, 2, 1, 2, 1, 0, 0, 0, 0, 3, 0, 1, 1, 2, 1, 1, 1, 2, 1, 1, 0, 0, 1, 2, 0, 1, 1, 1, 2, 2, 2, 0, 0, 1, 2, 2, 0, 0, 0, 3, 3, 3, 3, 2, 1, 1, 1, 1, 0, 1, 2, 2, 2, 0, 0, 3, 3, 3, 3, 3, 2, 2, 2, 1, 0, 3, 0, 1, 1, 1, 0, 1, 2, 2, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 0, 1, 0, 1, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 2, 2, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 0, 3, 3, 2, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 3, 0, 0, 1, 0, 1, 1, 2, 3, 0, 3, 2, 2, 2, 2, 1, 1, 0, 1, 2, 3, 2, 1, 1, 0, 1, 2, 2, 2, 2, 3, 2, 1, 1, 3, 3, 3, 0, 0, 0, 0, 1, 0, 3, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 0, 1, 2, 3, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 1, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 0, 1, 2, 3, 2, 1, 1, 0, 1, 2, 2, 2, 2, 2, 3, 2, 1, 1, 3, 3, 3, 0, 0, 0, 0, 1, 0, 3, 2, 2, 2, 2, 2, 1, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 3, 2, 3, 3, 0, 3, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 3, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 1, 1, 1, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 0, 1, 2, 3, 2, 1, 1, 0, 1, 2, 2, 2, 2, 3, 2, 1, 3, 3, 3, 0, 0, 0, 0, 1, 0, 3, 2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 0, 3, 3, 3, 2, 2, 3, 0, 3, 0, 1, 1, 1, 1, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 3, 2, 3, 0, 0, 3, 0, 1, 1, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 1, 1, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 1, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 3, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 0, 0, 0, 0, 1, 1, 0, 3, 2, 3, 3, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 1, 1, 1, 0, 3, 2, 3, 3, 0, 0, 1, 2, 2, 2, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 0, 3, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 0, 0, 0, 3, 0, 1, 1, 1, 1, 1, 1, 2, 1, 0, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 3, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 0, 1, 2, 3, 2, 1, 1, 0, 1, 2, 2, 2, 3, 2, 1, 1, 3, 2, 3, 3, 0, 0, 0, 0, 1, 0, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 3, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 3, 0, 0, 1, 2, 2, 2, 1, 1, 0, 1, 2, 3, 2, 1, 1, 0, 1, 2, 2, 2, 3, 2, 1, 2, 3, 3, 0, 0, 0, 0, 1, 0, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 2, 3, 0, 3, 3, 3, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 1, 0, 1, 2, 3, 2, 1, 1, 0, 1, 2, 3, 2, 2, 2, 2, 3, 3, 0, 0, 0, 0, 1, 0, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 2, 3, 0, 3, 3, 3, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 0, 1, 2, 3, 2, 1, 1, 3, 2, 1, 2, 2, 2, 2, 3, 3, 0, 0, 0, 0, 1, 0, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 0, 3, 2, 3, 0, 0, 0, 3, 0, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 0, 1, 2, 1, 2, 2, 2, 2, 2, 3, 3, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 3, 3, 1, 1, 2, 2, 1, 3, 3, 3, 0, 3, 2, 2, 2, 1, 2, 3, 3, 3, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 3, 0, 1, 0, 3, 3, 3, 0, 3, 2, 2, 1, 2, 3, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 3, 2, 2, 1, 2, 3, 3, 3, 3, 0, 3, 2, 2, 1, 0, 1, 1, 1, 1, 0, 0, 0, 3, 3, 3, 2, 2, 1, 2, 3, 3, 3, 2, 3, 0, 0, 0, 0, 1, 0, 3, 3, 1, 2, 2, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0, 3, 3, 3, 3, 2, 3, 0, 1, 0, 3, 3, 3, 2, 3, 0, 0, 0, 0, 1, 0, 3, 1, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 3, 3, 2, 1, 2, 2, 1, 2, 2, 3, 2, 2, 2, 3, 3, 2, 3, 0, 1, 0, 3, 3, 3, 3, 2, 3, 0, 1, 0, 3, 3, 3, 2, 3, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        self.len_move_list=len(self.save_move_list)
        self.move_count = 0
        self.start_position = True

    def leftkey(self, event):
        self.move_player(direction=2)

    def rightkey(self, event):
        self.move_player(direction=0)

    def upkey(self, event):
        self.move_player(direction=3)

    def downkey(self, event):
        self.move_player(direction=1)

    def last_moves(self):
        if not self.stopped and self.start_position:
            self.good_to_go = True
            self.auto_move()

    def auto_move(self):
        if not self.stopped and self.good_to_go:
            self.move_player(direction=self.save_move_list[self.move_count])
            self.move_count += 1
            if self.move_count < self.len_move_list:
                self.parent.after(50,self.auto_move)
                
    def save_last_moves(self):
        self.save_move_list = copy.deepcopy(self.move_list)
        self.len_move_list = len(self.save_move_list)
        self.move_count = 0
        print(self.save_move_list)
    
    def save_field(self):
        if self.stopped and self.started:
            self.level_cap += 1
            new_level = [p for sublist in self.field for p in sublist]
            new_level_info = self.level_info[:-1]
            new_level_info.append("Level: %d\t" % self.level_cap + ','.join(['%d' % pos for pos in new_level]) + "\n")
            new_level_info.append("Max Level:\t%d" % self.level_cap)
            self.level_info = copy.deepcopy(new_level_info)
            self.level_select.config(to=self.level_cap)
            with open(os.path.join(os.getcwd(), "levels_info_puzzle.txt"), "w") as f:
                f.writelines(new_level_info)

    def load_field(self):
        if self.stopped and self.started:
            self.current_level = int(self.level_select.get())
            if self.current_level > 0:
                level_info = self.level_info[self.current_level - 1].split("\t")[-1].split("\n")[0].split(',')
                self.field = np.zeros((self.field_len, self.field_len))
                for i, info in enumerate(level_info):
                    self.field[i//self.field_len, i%self.field_len] = int(info)
                self.current_field = copy.deepcopy(self.field)
                self.update_field(self.field)
                for key in self.object_dict:
                    self.object_dict[key]["count"] = np.sum(self.field == key)
            else:
                self.create_field()
                self.current_field = copy.deepcopy(self.field)
                self.update_field(self.field)
                for key in self.object_dict:
                    self.object_dict[key]["count"] = np.sum(self.field == key)

    def wall_button_press(self):
        new_walls = np.where(self.current_field == 7)
        self.current_field[new_walls[0], new_walls[1]] = 701
        for j, i in enumerate(new_walls[0]):
            self.field_buttons[i*self.field_len + new_walls[1][j]].configure(image=self.object_dict[1]["pic"])

    def wall_button_release(self):
        new_passable_walls = np.where(self.current_field == 701)
        self.current_field[new_passable_walls[0], new_passable_walls[1]] = 7
        for j, i in enumerate(new_passable_walls[0]):
            self.field_buttons[i*self.field_len + new_passable_walls[1][j]].configure(image=self.object_dict[7]["pic"])

    def edit_field(self):
        if not self.started:
            self.create_field()
            self.create_visual_field()
            self.edit_button.configure(text="Edit")
            self.started = True
            self.button_active = True
        else:
            self.reset()
            if not self.stopped:
                self.time_left = 60
                self.timer_label.configure(text="")
                self.won = False
                self.lost = False
                self.stopped = True
                self.button_active = True
        self.text_output.configure(text="Edit Mode")

    def reset(self):
        if not self.stopped or self.won or self.lost:
            self.good_to_go = False
            self.start_position = True
            self.time_left = 60
            self.timer_label.configure(text="")
            self.keys_label.configure(text="")
            self.timer_started = False
            self.reverse_lr = False
            self.reverse_ud = False
            self.invisible = False
            self.possesed_keys = 0
            if self.won or self.lost:
                self.text_output.configure(text="Play Mode")
            self.won = False
            self.lost = False
            self.stopped = False
            self.update_field(self.field)
            self.current_field = copy.deepcopy(self.field)
            player_pos = np.where(self.field == 2)
            self.player_pos = player_pos[0][0] * self.field_len + player_pos[1][0]
            self.move_list = []
            self.move_count = 0

    def create_field(self):
        self.field = np.zeros((self.field_len, self.field_len))
        self.field[:, 0] = 1
        self.field[0, :] = 1
        self.field[self.field_len - 1, :] = 1
        self.field[:, self.field_len - 1] = 1

    def create_visual_field(self):
        self.field = np.array(self.field)
        self.field_buttons = []
        self.button_count = 0
        self.object_buttons = []
        self.object_button_count = 0
        for key, value in self.object_dict.items():
            self.object_buttons.append(tk.Button(self, disabledforeground=None, command=lambda k=key: self.change_current_object(obj=k)))
            self.object_buttons[self.object_button_count].pack(side="left", padx=20)
            self.object_buttons[self.object_button_count].place(y=35, x=5 + key * 30, height=30, width=30)
            self.object_buttons[self.object_button_count].configure(bg="white", image=value["pic"])
            self.object_button_count += 1
        for i in range(self.field_len):
            for j in range(self.field_len):
                self.field_buttons.append(tk.Button(self, command=lambda k=self.field_len * i + j: self.change_field(pos=k)))
                self.field_buttons[self.button_count].pack(side="left", padx=20)
                self.field_buttons[self.button_count].place(y=80 + i * 30, x=40 + j * 30, height=30, width=30)
                self.field_buttons[self.button_count].configure(bg="white", image=self.object_dict[self.field[i, j]]["pic"])
                self.button_count += 1

    def change_field(self, pos=0):
        if self.button_active:
            cur_obs = self.field[int(pos//self.field_len), int(pos % self.field_len)]
            if cur_obs != self.current_object and self.object_dict[self.current_object]["count"] < self.object_dict[self.current_object]["max_count"]:
                self.field[int(pos // self.field_len), int(pos % self.field_len)] = self.current_object
                self.field_buttons[pos].configure(bg="white", image=self.object_dict[self.current_object]["pic"])
                self.object_dict[self.current_object]["count"] += 1
                self.object_dict[cur_obs]["count"] -= 1

    def update_field(self, new_field):
        if self.started:
            for i, button in enumerate(self.field_buttons):
                pic = self.object_dict[new_field[i//self.field_len, i % self.field_len]]["pic"]
                button.configure(bg="white", image=pic)

    def change_current_object(self, obj):
        self.current_object = obj

    def play_free_mode(self):
        if self.won or self.lost:
            self.reset()
            self.button_active = False
            self.text_output.configure(text="Play Mode")
        if self.stopped:
            if np.sum(self.field == 2) == 1 and np.sum(self.field == 3) == 1 and (np.sum(self.field == 4) + np.sum(self.field == 8)) >= np.sum(self.field == 5):
                self.current_field = copy.deepcopy(self.field)
                self.button_active = False
                self.stopped = False
                self.start_position = True
                self.good_to_go = True
                self.text_output.configure(text="Play Mode")
                player_pos = np.where(self.field == 2)
                self.player_pos = player_pos[0][0] * self.field_len + player_pos[1][0]
            else:
                self.text_output.configure(text="Check field !")

    def move_player(self, direction):
        if not self.stopped:
            if self.start_position:
                self.start_position = False
            self.move_list.append(direction)
            if self.reverse_lr and (direction==0 or direction==2):
                if direction==0:
                    plus_minus = -1
                elif direction==2:
                    plus_minus = 1
            elif self.reverse_ud and (direction==1 or direction==3):
                if direction==1:
                    plus_minus = -1
                elif direction==3:
                    plus_minus = 1
            else:
                plus_minus = 1 if direction < 2 else -1
            old_player_pos = self.player_pos
            if old_player_pos//self.field_len == 0 and direction % 2 == 1 and plus_minus == -1:
                new_player_pos = old_player_pos + self.field_len * (self.field_len - 1)
            elif old_player_pos // self.field_len == self.field_len - 1 and direction % 2 == 1 and plus_minus == 1:
                new_player_pos = old_player_pos - self.field_len * (self.field_len - 1)
            elif old_player_pos % self.field_len == 0 and direction % 2 == 0 and plus_minus == -1:
                new_player_pos = old_player_pos + self.field_len - 1
            elif old_player_pos % self.field_len == self.field_len - 1 and direction % 2 == 0 and plus_minus == 1:
                new_player_pos = old_player_pos - self.field_len + 1
            else:
                new_player_pos = (self.player_pos + plus_minus * (((direction + 1) % 2) + (direction % 2 * self.field_len))) % (self.field_len**2)
            old_space_obs = self.current_field[old_player_pos // self.field_len, old_player_pos % self.field_len]
            next_space_obs = self.current_field[new_player_pos//self.field_len, new_player_pos % self.field_len]
            if self.object_dict[next_space_obs % 100]["passable"]:
                self.player_pos = new_player_pos
                if next_space_obs == 9:
                    self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = 2
                    if self.reverse_lr:
                        self.reverse_lr = False
                    else:
                        self.reverse_lr = True
                    if self.reverse_ud:
                        self.reverse_ud = False
                    else:
                        self.reverse_ud = True
                elif next_space_obs == 10:
                    self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = 2
                    self.invisible = True
                elif next_space_obs == 11:
                    self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = 2
                    if self.timer_started:
                        self.time_left = 60
                    else:
                        self.timer_started = True
                        self.start_timer()
                elif next_space_obs == 12:
                    self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = 2
                    self.loose()
                elif next_space_obs == 13:
                    self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = 2
                    self.possesed_keys += 1
                    self.keys_label.configure(text="Keys: %02d" % self.possesed_keys)
                elif next_space_obs == 19:
                    self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = 2
                    self.invisible = False
                elif next_space_obs == 20:
                    if self.reverse_lr:
                        self.reverse_lr = False
                    else:
                        self.reverse_lr = True
                elif next_space_obs == 21:
                    if self.reverse_ud:
                        self.reverse_ud = False
                    else:
                        self.reverse_ud = True
                else:
                    self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = next_space_obs * 100 + 2
                self.current_field[old_player_pos // self.field_len, old_player_pos % self.field_len] = old_space_obs//100
                if self.invisible:
                    self.field_buttons[new_player_pos].configure(image=self.object_dict[0]["pic"])
                else:
                    self.field_buttons[new_player_pos].configure(image=self.object_dict[2]["pic"])
                self.field_buttons[old_player_pos].configure(image=self.object_dict[old_space_obs//100]["pic"])
                if next_space_obs == 6:
                    self.wall_button_press()
            else:
                if self.object_dict[next_space_obs % 100]["movable"]:
                    if new_player_pos // self.field_len == 0 and direction % 2 == 1 and plus_minus == -1:
                        new_obs_pos = new_player_pos + self.field_len * (self.field_len - 1)
                    elif new_player_pos // self.field_len == self.field_len - 1 and direction % 2 == 1 and plus_minus == 1:
                        new_obs_pos = new_player_pos - self.field_len * (self.field_len - 1)
                    elif new_player_pos % self.field_len == 0 and direction % 2 == 0 and plus_minus == -1:
                        new_obs_pos = new_player_pos + self.field_len - 1
                    elif new_player_pos % self.field_len == self.field_len - 1 and direction % 2 == 0 and plus_minus == 1:
                        new_obs_pos = new_player_pos - self.field_len + 1
                    else:
                        new_obs_pos = (new_player_pos + plus_minus * (((direction + 1) % 2) + (direction % 2 * self.field_len))) % (self.field_len**2)
                    next_next_space_obs = self.current_field[new_obs_pos//self.field_len, new_obs_pos % self.field_len]
                    if self.object_dict[next_next_space_obs % 100]["passable"]:
                        self.player_pos = new_player_pos
                        self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = (next_space_obs // 100) * 100 + 2
                        self.current_field[old_player_pos // self.field_len, old_player_pos % self.field_len] = old_space_obs // 100
                        if next_next_space_obs == 9:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_space_obs % 100
                            if self.reverse_lr:
                                self.reverse_lr = False
                            else:
                                self.reverse_lr = True
                            if self.reverse_ud:
                                self.reverse_ud = False
                            else:
                                self.reverse_ud = True
                        elif next_next_space_obs == 10:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_space_obs % 100
                            self.invisible = True
                        elif next_next_space_obs == 11:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_space_obs % 100
                            if self.timer_started:
                                self.time_left = 60
                            else:
                                self.timer_started = True
                                self.start_timer()
                        elif next_next_space_obs == 12:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_space_obs % 100
                            self.loose()
                        elif next_next_space_obs == 13:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_space_obs % 100
                            self.possesed_keys += 1
                            self.keys_label.configure(text="Keys: %02d" % self.possesed_keys)
                        elif next_next_space_obs == 19:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_space_obs % 100
                            self.invisible = False
                        elif next_next_space_obs == 20:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_space_obs % 100
                            if self.reverse_lr:
                                self.reverse_lr = False
                            else:
                                self.reverse_lr = True
                        elif next_next_space_obs == 21:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_space_obs % 100
                            if self.reverse_ud:
                                self.reverse_ud = False
                            else:
                                self.reverse_ud = True
                        else:
                            self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = next_next_space_obs * 100 + (next_space_obs % 100)
                        if self.invisible:
                            self.field_buttons[new_player_pos].configure(image=self.object_dict[0]["pic"])
                        else:
                            self.field_buttons[new_player_pos].configure(image=self.object_dict[2]["pic"])
                        self.field_buttons[old_player_pos].configure(image=self.object_dict[old_space_obs // 100]["pic"])
                        if next_next_space_obs * 100 + (next_space_obs % 100) == 8 or next_next_space_obs * 100 + (next_space_obs % 100) == 17:
                            self.field_buttons[new_obs_pos].configure(image=self.object_dict[0]["pic"])
                        else:
                            self.field_buttons[new_obs_pos].configure(image=self.object_dict[next_space_obs % 100]["pic"])
                        if next_next_space_obs == 6:
                            self.wall_button_press()
                    elif (next_next_space_obs == 16 and next_space_obs % 100 == 15) or (next_next_space_obs == 18 and next_space_obs % 100 == 17):
                        self.player_pos = new_player_pos
                        self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = (next_space_obs // 100) * 100 + 2
                        self.current_field[old_player_pos // self.field_len, old_player_pos % self.field_len] = old_space_obs // 100
                        self.current_field[new_obs_pos // self.field_len, new_obs_pos % self.field_len] = 0
                        if self.invisible:
                            self.field_buttons[new_player_pos].configure(image=self.object_dict[0]["pic"])
                        else:
                            self.field_buttons[new_player_pos].configure(image=self.object_dict[2]["pic"])
                        self.field_buttons[old_player_pos].configure(image=self.object_dict[old_space_obs // 100]["pic"])
                        self.field_buttons[new_obs_pos].configure(image=self.object_dict[0]["pic"])
                elif next_space_obs == 14 and self.possesed_keys > 0:
                     self.possesed_keys -= 1
                     self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len] = 0
                     self.field_buttons[new_player_pos].configure(image=self.object_dict[0]["pic"])
                     self.keys_label.configure(text="Keys: %02d" % self.possesed_keys)
            if old_space_obs // 100 == 6 and old_player_pos != self.player_pos:
                self.wall_button_release()
            if self.current_field[new_player_pos // self.field_len, new_player_pos % self.field_len]//100 == 3:
                self.check_for_win()

    def start_timer(self):
        if self.timer_started:
            self.time_left -= 1
            self.timer_label.configure(text="%d:%02d"%(int(self.time_left//60),int(self.time_left%60)))
            if self.time_left <= 0:
                self.loose()
            else:
                self.parent.after(1000,self.start_timer)

    def loose(self):
        self.time_left = 0
        self.text_output.configure(text="Lost :(")
        self.stopped = True
        self.lost = True

    def check_for_win(self):
        if (np.sum(self.current_field == 504) + np.sum(self.current_field == 508)) == self.object_dict[5]["count"]:
            self.text_output.configure(text="Win !!")
            self.stopped = True
            self.timer_started = False
            self.time_left = 60
            self.won = True

if __name__ == "__main__":
    root = tk.Tk()
    app = Puzzle(parent=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
