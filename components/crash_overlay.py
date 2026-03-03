# components/crash_overlay.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.animation import Animation
from logic.crash_logic import calculate_total_points
from kivy.uix.gridlayout import GridLayout

class CrashOverlay(BoxLayout):
    def __init__(self, attacker, defender, start_pos, end_pos, a_faction, d_faction, get_img_path_func, on_finish, on_cancel, **kwargs):
        super().__init__(orientation='vertical', size_hint=(None, None), size=(340, 400), 
                         pos_hint={'right': 0.96, 'center_y': 0.5}, padding=15, spacing=10, **kwargs)
        
        self.attacker = attacker
        self.defender = defender
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.a_faction = a_faction
        self.d_faction = d_faction
        self.get_img_path_func = get_img_path_func
        self.on_finish = on_finish
        self.on_cancel = on_cancel
        self.crash_stagger_count = 0
        
        with self.canvas.before:
            Color(0.08, 0.08, 0.12, 0.98) 
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        self.x += 30
        self.opacity = 0
        anim = Animation(x=self.x - 30, opacity=1, duration=0.2, t='out_quad')
        anim.start(self)
        
        self._setup_ui()

    def _update_bg(self, instance, value):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size

    def _setup_ui(self):
        title_lbl = Label(text="CRASH!", bold=True, font_size='28sp', color=(1, 0.2, 0.2, 1), size_hint_y=0.15)
        self.add_widget(title_lbl)
        
        combatants_layout = BoxLayout(orientation='horizontal', size_hint_y=0.55)
        
        # ฝ่ายโจมตี
        atk_box = BoxLayout(orientation='vertical', spacing=5)
        atk_img = Image(source=self.get_img_path_func(self.attacker), size_hint_y=0.4)
        atk_pts = getattr(self.attacker, 'base_points', 5)
        atk_box.add_widget(atk_img)
        atk_box.add_widget(Label(text=f"point : {atk_pts}", font_size='14sp', color=(1, 0.8, 0.2, 1), size_hint_y=0.15))
        
        self.a_coins_layout = GridLayout(cols=3, spacing=2, size_hint_y=0.25)
        atk_box.add_widget(self.a_coins_layout)
        
        self.a_val_lbl = Label(text=f"crash : {atk_pts}", font_size='16sp', color=(1, 0.4, 0.4, 1), bold=True, size_hint_y=0.2)
        atk_box.add_widget(self.a_val_lbl)
        
        self.vs_lbl = Label(text="VS", bold=True, font_size='24sp', color=(0.8, 0.8, 0.8, 1), size_hint_x=0.4, halign="center")
        
        # ฝ่ายป้องกัน
        def_box = BoxLayout(orientation='vertical', spacing=5)
        def_img = Image(source=self.get_img_path_func(self.defender), size_hint_y=0.4)
        def_pts = getattr(self.defender, 'base_points', 5)
        def_box.add_widget(def_img)
        def_box.add_widget(Label(text=f"point : {def_pts}", font_size='14sp', color=(1, 0.8, 0.2, 1), size_hint_y=0.15))
        
        self.d_coins_layout = GridLayout(cols=3, spacing=2, size_hint_y=0.25)
        def_box.add_widget(self.d_coins_layout)
        
        self.d_val_lbl = Label(text=f"crash : {def_pts}", font_size='16sp', color=(0.4, 0.4, 1, 1), bold=True, size_hint_y=0.2)
        def_box.add_widget(self.d_val_lbl)
        
        combatants_layout.add_widget(atk_box)
        combatants_layout.add_widget(self.vs_lbl)
        combatants_layout.add_widget(def_box)
        self.add_widget(combatants_layout)
        
        btn_layout = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=10, padding=[0, 10, 0, 0])
        self.crash_btn = Button(text="CRASH!", bold=True, font_size='18sp', background_color=(0.8, 0.2, 0.2, 1))
        self.crash_btn.bind(on_release=self.start_crash_animation)
        self.cancel_btn = Button(text="CANCEL", font_size='14sp', background_color=(0.3, 0.3, 0.3, 1))
        self.cancel_btn.bind(on_release=lambda x: self.on_cancel())
        
        btn_layout.add_widget(self.crash_btn)
        btn_layout.add_widget(self.cancel_btn)
        self.add_widget(btn_layout)

    def start_crash_animation(self, *args):
        self.crash_btn.disabled = True
        self.cancel_btn.disabled = True

        if getattr(self.defender, 'item', None) and self.defender.item.id == 4:
            self.on_finish(self.start_pos, self.end_pos, "blocked")
            return 

        a_base = getattr(self.attacker, 'base_points', 5)
        a_coins = getattr(self.attacker, 'coins', 3)
        d_base = getattr(self.defender, 'base_points', 5)
        d_coins = getattr(self.defender, 'coins', 3)

        if getattr(self.defender, 'item', None) and self.defender.item.id == 8: a_coins = max(0, a_coins - 1)
        if getattr(self.attacker, 'item', None) and self.attacker.item.id == 8: d_coins = max(0, d_coins - 1)
        if getattr(self.defender, 'item', None) and self.defender.item.id == 2: a_coins = 0

        self.a_final_total, self.a_results = calculate_total_points(a_base, a_coins, self.a_faction)
        self.d_final_total, self.d_results = calculate_total_points(d_base, d_coins, self.d_faction)

        self.a_val_lbl.text = f"crash : {a_base}"
        self.d_val_lbl.text = f"crash : {d_base}"

        self.a_coins_layout.clear_widgets()
        self.d_coins_layout.clear_widgets()
        self.a_coin_widgets = []
        self.d_coin_widgets = []

        for _ in range(a_coins):
            img = Image(source='assets/coin/coin10.png', size_hint=(None, None), size=(32, 32))
            self.a_coin_widgets.append(img)
            self.a_coins_layout.add_widget(img)

        for _ in range(d_coins):
            img = Image(source='assets/coin/coin10.png', size_hint=(None, None), size=(32, 32))
            self.d_coin_widgets.append(img)
            self.d_coins_layout.add_widget(img)

        def get_pt(res_str, faction):
            if "Green" in res_str: return 100
            if "Cyan" in res_str: return 10
            if "Purple" in res_str: return 6
            if "Orange" in res_str: return 4
            if "Blue" in res_str: return 3
            if "Red" in res_str: return 2
            if "Yellow" in res_str: return 1
            if "Tails" in res_str and faction == "demon": return -3
            return 0

        self.a_pts_array = [get_pt(r, self.a_faction) for r in self.a_results]
        self.d_pts_array = [get_pt(r, self.d_faction) for r in self.d_results]

        self.anim_state = {
            'side': 'atk', 'coin_idx': 0, 'ticks': 0, 'max_ticks': 20,
            'a_current_total': a_base, 'd_current_total': d_base
        }
        self.spin_event = Clock.schedule_interval(self.animate_coin_step, 0.10)

    def _get_coin_img(self, res_str, faction):
        if "Green" in res_str: return "assets/coin/coin9.png"
        if "Cyan" in res_str: return "assets/coin/coin8.png"
        if "Purple" in res_str: return "assets/coin/coin7.png"
        if "Orange" in res_str: return "assets/coin/coin6.png"
        if "Blue" in res_str: return "assets/coin/coin5.png"
        if "Red" in res_str: return "assets/coin/coin4.png"
        if "Yellow" in res_str: return "assets/coin/coin3.png"
        if "Tails" in res_str: return "assets/coin/coin1.png" if faction == "demon" else "assets/coin/coin2.png"
        return "assets/coin/coin10.png"

    def animate_coin_step(self, dt):
        state = self.anim_state
        side = state['side']
        idx = state['coin_idx']
        
        if side == 'atk':
            pts_array, results, faction = self.a_pts_array, self.a_results, self.a_faction
            coin_widgets, lbl_total, current_total_key = self.a_coin_widgets, self.a_val_lbl, 'a_current_total'
        else:
            pts_array, results, faction = self.d_pts_array, self.d_results, self.d_faction
            coin_widgets, lbl_total, current_total_key = self.d_coin_widgets, self.d_val_lbl, 'd_current_total'

        if idx >= len(pts_array):
            if side == 'atk':
                state['side'], state['coin_idx'], state['ticks'] = 'def', 0, 0
                return
            else:
                self.spin_event.cancel()
                self.finish_crash_animation()
                return

        state['ticks'] += 1
        
        if idx < len(coin_widgets):
            img_widget = coin_widgets[idx]
            img_widget.opacity = 1.0 if (state['ticks'] % 4) < 2 else 0.3
            
            if state['ticks'] >= state['max_ticks']:
                img_widget.opacity = 1.0
                img_widget.source = self._get_coin_img(results[idx], faction)
                state[current_total_key] += pts_array[idx]
                lbl_total.text = f"crash : {state[current_total_key]}"
                state['coin_idx'] += 1
                state['ticks'] = 0
        else:
            state['coin_idx'] += 1
            state['ticks'] = 0

    def finish_crash_animation(self):
        a_tot = self.anim_state['a_current_total']
        d_tot = self.anim_state['d_current_total']

        if a_tot > d_tot:
            self.vs_lbl.text = "[color=00ff00]BREAKING[/color]"
            self.vs_lbl.font_size = '20sp'
            self.vs_lbl.markup = True
            Clock.schedule_once(lambda dt: self.on_finish(self.start_pos, self.end_pos, "won"), 1.5)
            
        elif a_tot == d_tot:
            self.vs_lbl.text = "[color=ffff00]DRAW[/color]"
            self.vs_lbl.font_size = '20sp'
            self.vs_lbl.markup = True
            Clock.schedule_once(lambda dt: self.start_crash_animation(), 1.5)
            
        else:
            self.crash_stagger_count += 1
            if self.crash_stagger_count < 2:
                self.vs_lbl.text = "[color=ff8800]STAGGER[/color]" 
                self.vs_lbl.font_size = '20sp'
                self.vs_lbl.markup = True
                Clock.schedule_once(lambda dt: self.start_crash_animation(), 1.5)
            else:
                self.vs_lbl.text = "[color=ff0000]DISTORTION[/color]" 
                self.vs_lbl.font_size = '20sp'
                self.vs_lbl.markup = True
                Clock.schedule_once(lambda dt: self.on_finish(self.start_pos, self.end_pos, "died"), 1.5)

    def force_cancel(self):
        if hasattr(self, 'spin_event') and self.spin_event:
            self.spin_event.cancel()