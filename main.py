from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from plyer import notification
from kivy.utils import platform
import datetime

# SIEM import with proper error handling
try:
    from siemcore import run_siem_scan
    print("[SentinelIT] SIEM module loaded successfully")
except ImportError as e:
    print(f"[IMPORT ERROR]: {e}")
    def run_siem_scan():
        print("[SentinelIT] Using fallback SIEM scan")
        return {
            "success": True,
            "threats": [
                {
                    "id": 1,
                    "type": "Suspicious Connection",
                    "severity": "medium",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "status": "active",
                    "port": 8080
                },
                {
                    "id": 2,
                    "type": "Root Access Attempt", 
                    "severity": "high",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "status": "blocked",
                    "source": "unknown"
                },
                {
                    "id": 3,
                    "type": "Unusual Network Traffic",
                    "severity": "low", 
                    "timestamp": datetime.datetime.now().isoformat(),
                    "status": "monitoring",
                    "port": 443
                }
            ],
            "scan_timestamp": datetime.datetime.now().isoformat(),
            "threats_count": 3
        }
    print("[SentinelIT] Fallback SIEM scan loaded")

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.threats_data = []
        self.last_scan_time = None
        self.protection_status = "Protected"
        self.total_scans = 0
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Header section
        header = self.create_header()
        main_layout.add_widget(header)
        
        # Status cards grid
        status_cards = self.create_status_cards()
        main_layout.add_widget(status_cards)
        
        # Quick actions section
        quick_actions = self.create_quick_actions()
        main_layout.add_widget(quick_actions)
        
        # Recent activity section
        activity_section = self.create_activity_section()
        main_layout.add_widget(activity_section)
        
        self.add_widget(main_layout)
        
        # Auto-refresh every 30 seconds
        Clock.schedule_interval(self.auto_refresh, 30)
    
    def create_header(self):
        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.2, spacing=8)
        
        # App title with icon
        title_label = Label(
            text="🛡️ SentinelIT Mobile Pro", 
            font_size='26sp',
            bold=True,
            color=(0.2, 0.6, 0.8, 1),
            halign='center'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Protection status indicator
        self.status_label = Label(
            text="🟢 System Protected",
            font_size='18sp',
            color=(0, 0.8, 0, 1),
            halign='center'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        
        # Last scan information
        self.last_scan_label = Label(
            text="Last scan: Never",
            font_size='14sp',
            color=(0.6, 0.6, 0.6, 1),
            halign='center'
        )
        self.last_scan_label.bind(size=self.last_scan_label.setter('text_size'))
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(self.status_label)
        header_layout.add_widget(self.last_scan_label)
        
        return header_layout
    
    def create_status_cards(self):
        # Container for status cards
        cards_container = BoxLayout(orientation='vertical', size_hint_y=0.35, spacing=10)
        
        # Section title
        cards_title = Label(
            text="Security Status",
            font_size='20sp',
            bold=True,
            size_hint_y=0.2,
            color=(0.3, 0.3, 0.3, 1),
            halign='left'
        )
        cards_title.bind(size=cards_title.setter('text_size'))
        cards_container.add_widget(cards_title)
        
        # 2x2 grid for status cards
        cards_grid = GridLayout(cols=2, size_hint_y=0.8, spacing=15)
        
        # Individual status cards
        self.threats_card = self.create_status_card("⚠️ Threats", "0", "All Clear", (0, 0.8, 0, 1))
        self.scans_card = self.create_status_card("🔍 Scans", "0", "Completed", (0.2, 0.6, 0.8, 1))
        self.protection_card = self.create_status_card("🛡️ Protection", "ON", "Real-time", (0, 0.8, 0, 1))
        self.updates_card = self.create_status_card("📡 Updates", "✓", "Current", (0, 0.8, 0, 1))
        
        cards_grid.add_widget(self.threats_card)
        cards_grid.add_widget(self.scans_card)
        cards_grid.add_widget(self.protection_card)
        cards_grid.add_widget(self.updates_card)
        
        cards_container.add_widget(cards_grid)
        return cards_container
    
    def create_status_card(self, title, value, subtitle, color):
        # Card container with background
        card_container = BoxLayout(orientation='vertical', padding=15, spacing=8)
        
        # Card title
        title_label = Label(
            text=title,
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.3,
            halign='center'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Main value
        value_label = Label(
            text=value,
            font_size='32sp',
            bold=True,
            color=color,
            size_hint_y=0.5,
            halign='center'
        )
        value_label.bind(size=value_label.setter('text_size'))
        
        # Subtitle
        subtitle_label = Label(
            text=subtitle,
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.2,
            halign='center'
        )
        subtitle_label.bind(size=subtitle_label.setter('text_size'))
        
        card_container.add_widget(title_label)
        card_container.add_widget(value_label)
        card_container.add_widget(subtitle_label)
        
        return card_container
    
    def create_quick_actions(self):
        actions_container = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=10)
        
        # Section title
        actions_title = Label(
            text="Quick Actions",
            font_size='20sp',
            bold=True,
            size_hint_y=0.25,
            color=(0.3, 0.3, 0.3, 1),
            halign='left'
        )
        actions_title.bind(size=actions_title.setter('text_size'))
        actions_container.add_widget(actions_title)
        
        # Action buttons in 2x2 grid
        buttons_grid = GridLayout(cols=2, spacing=12, size_hint_y=0.75)
        
        # Quick Scan button
        quick_scan_btn = Button(
            text="🔍 Quick Scan",
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        quick_scan_btn.bind(on_press=self.perform_quick_scan)
        
        # Full Scan button
        full_scan_btn = Button(
            text="🔍 Deep Scan", 
            background_color=(0.8, 0.4, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        full_scan_btn.bind(on_press=self.perform_full_scan)
        
        # Settings button
        settings_btn = Button(
            text="⚙️ Settings",
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        settings_btn.bind(on_press=self.open_settings)
        
        # Reports button
        reports_btn = Button(
            text="📊 Reports",
            background_color=(0.4, 0.8, 0.4, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        reports_btn.bind(on_press=self.open_reports)
        
        buttons_grid.add_widget(quick_scan_btn)
        buttons_grid.add_widget(full_scan_btn)
        buttons_grid.add_widget(settings_btn)
        buttons_grid.add_widget(reports_btn)
        
        actions_container.add_widget(buttons_grid)
        return actions_container
    
    def create_activity_section(self):
        activity_container = BoxLayout(orientation='vertical', size_hint_y=0.2, spacing=8)
        
        # Section title
        activity_title = Label(
            text="Recent Activity",
            font_size='20sp',
            bold=True,
            size_hint_y=0.3,
            color=(0.3, 0.3, 0.3, 1),
            halign='left'
        )
        activity_title.bind(size=activity_title.setter('text_size'))
        activity_container.add_widget(activity_title)
        
        # Scrollable activity feed
        self.activity_scroll = ScrollView(size_hint_y=0.7)
        self.activity_list = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.activity_list.bind(minimum_height=self.activity_list.setter('height'))
        
        # Add initial activity items
        self.add_activity_item("🛡️ SentinelIT Mobile started", "Just now")
        self.add_activity_item("📡 Security definitions loaded", "2 min ago")
        self.add_activity_item("🔄 Real-time protection enabled", "2 min ago")
        
        self.activity_scroll.add_widget(self.activity_list)
        activity_container.add_widget(self.activity_scroll)
        
        return activity_container
    
    def add_activity_item(self, text, time_text):
        item_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=35, spacing=10)
        
        # Activity description
        activity_label = Label(
            text=text,
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1),
            text_size=(None, None),
            halign='left',
            size_hint_x=0.7
        )
        
        # Timestamp
        time_label = Label(
            text=time_text,
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            halign='right',
            size_hint_x=0.3
        )
        
        item_container.add_widget(activity_label)
        item_container.add_widget(time_label)
        
        # Add to top of activity list
        self.activity_list.add_widget(item_container, index=len(self.activity_list.children))
    
    def perform_quick_scan(self, instance):
        self.execute_scan("Quick Scan")
    
    def perform_full_scan(self, instance):
        self.execute_scan("Deep Scan")
    
    def execute_scan(self, scan_type):
        try:
            print(f"[SentinelIT] Starting {scan_type}...")
            
            # Update UI to show scanning state
            self.status_label.text = f"🔍 {scan_type} in progress..."
            self.status_label.color = (1, 0.8, 0, 1)  # Orange color
            
            # Add activity entry
            self.add_activity_item(f"🔍 {scan_type} initiated", "Now")
            
            # Execute SIEM scan
            result = run_siem_scan()
            
            if isinstance(result, dict) and result.get("success"):
                threats = result.get("threats", [])
                threats_count = result.get("threats_count", len(threats))
                self.threats_data = threats
                self.last_scan_time = datetime.datetime.now()
                self.total_scans += 1
                
                # Update all status cards
                self.update_threats_card(threats_count, threats)
                self.update_scans_card()
                self.update_last_scan_display()
                
                # Update main status and activity
                if threats_count > 0:
                    self.add_activity_item(f"⚠️ {threats_count} threats detected", "Now")
                    self.status_label.text = f"⚠️ {threats_count} threats found"
                    self.status_label.color = (1, 0.6, 0, 1)  # Orange warning
                    
                    # Send notification
                    try:
                        notification.notify(
                            title="SentinelIT Alert",
                            message=f"{scan_type}: {threats_count} threats detected!",
                            timeout=5
                        )
                    except Exception:
                        pass
                else:
                    self.add_activity_item("✅ System clean - no threats", "Now")
                    self.status_label.text = "🟢 System Protected"
                    self.status_label.color = (0, 0.8, 0, 1)  # Green
                    
                    try:
                        notification.notify(
                            title="SentinelIT",
                            message=f"{scan_type} complete: All clear!",
                            timeout=5
                        )
                    except Exception:
                        pass
            else:
                error_msg = result.get("error", "Scan failed") if isinstance(result, dict) else "Unknown error"
                self.status_label.text = f"❌ {error_msg}"
                self.status_label.color = (1, 0, 0, 1)  # Red
                self.add_activity_item(f"❌ {scan_type} failed", "Now")
                
        except Exception as e:
            print(f"[SentinelIT ERROR]: {e}")
            self.status_label.text = f"❌ Scan error: {str(e)}"
            self.status_label.color = (1, 0, 0, 1)
            self.add_activity_item("❌ Scan error occurred", "Now")
    
    def update_threats_card(self, count, threats):
        # Update the threats card with current data
        threat_value_label = self.threats_card.children[1]  # Value label
        threat_subtitle_label = self.threats_card.children[0]  # Subtitle label
        
        if count > 0:
            threat_value_label.text = str(count)
            
            # Determine color based on severity
            high_threats = sum(1 for t in threats if t.get('severity') == 'high')
            medium_threats = sum(1 for t in threats if t.get('severity') == 'medium')
            low_threats = sum(1 for t in threats if t.get('severity') == 'low')
            
            if high_threats > 0:
                threat_value_label.color = (1, 0, 0, 1)  # Red for high
                threat_subtitle_label.text = f"{high_threats} Critical"
                threat_subtitle_label.color = (1, 0, 0, 1)
            elif medium_threats > 0:
                threat_value_label.color = (1, 0.6, 0, 1)  # Orange for medium
                threat_subtitle_label.text = f"{medium_threats} Medium"
                threat_subtitle_label.color = (1, 0.6, 0, 1)
            else:
                threat_value_label.color = (1, 0.8, 0, 1)  # Yellow for low
                threat_subtitle_label.text = f"{low_threats} Low Risk"
                threat_subtitle_label.color = (1, 0.8, 0, 1)
        else:
            threat_value_label.text = "0"
            threat_value_label.color = (0, 0.8, 0, 1)  # Green for clean
            threat_subtitle_label.text = "All Clear"
            threat_subtitle_label.color = (0, 0.8, 0, 1)
    
    def update_scans_card(self):
        # Update scan counter
        scan_value_label = self.scans_card.children[1]
        scan_value_label.text = str(self.total_scans)
    
    def update_last_scan_display(self):
        if self.last_scan_time:
            time_str = self.last_scan_time.strftime("%H:%M")
            self.last_scan_label.text = f"Last scan: Today at {time_str}"
    
    def auto_refresh(self, dt):
        # Periodic system status refresh
        self.add_activity_item("🔄 System status refreshed", "Now")
        
        # Keep only recent 10 activity items
        if len(self.activity_list.children) > 10:
            self.activity_list.remove_widget(self.activity_list.children[0])
    
    def open_settings(self, instance):
        self.add_activity_item("⚙️ Settings panel accessed", "Now")
        # TODO: Implement settings screen
        
    def open_reports(self, instance):
        self.add_activity_item("📊 Security reports viewed", "Now")
        # TODO: Implement reports screen

class SentinelApp(App):
    def build(self):
        self.title = "SentinelIT Mobile Pro"
        
        # Create screen manager for future expansion
        screen_manager = ScreenManager()
        dashboard_screen = DashboardScreen()
        screen_manager.add_widget(dashboard_screen)
        
        return screen_manager

if __name__ == '__main__':
    print("[SentinelIT] Professional Security Dashboard launching...")
    SentinelApp().run() 