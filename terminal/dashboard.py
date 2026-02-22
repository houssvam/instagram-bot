import asyncio
import psutil
import time
from datetime import datetime
import os

# Simple console dashboard for Windows
class TerminalDashboard:
    """Terminal dashboard for monitoring"""
    
    def __init__(self):
        self.start_time = time.time()
        self.stats = {
            'downloads': 0,
            'users': 0,
            'errors': 0,
            'bytes_sent': 0
        }
        
    async def start(self):
        """Start live dashboard"""
        while True:
            self.clear_screen()
            self.render_header()
            self.render_stats()
            self.render_logs()
            self.render_footer()
            await asyncio.sleep(1)
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render_header(self):
        """Render header"""
        print("="*60)
        print("🤖 INSTAGRAM ULTIMATE BOT DASHBOARD")
        print(f"Uptime: {self.get_uptime()}")
        print("="*60)
    
    def render_stats(self):
        """Render statistics"""
        print("\n📊 STATISTICS:")
        print(f"  Downloads: {self.stats['downloads']}")
        print(f"  Active Users: {self.stats['users']}")
        print(f"  Errors: {self.stats['errors']}")
        print(f"  Data Sent: {self.format_bytes(self.stats['bytes_sent'])}")
        
        # System stats
        print(f"  CPU Usage: {psutil.cpu_percent()}%")
        print(f"  Memory: {psutil.virtual_memory().percent}%")
    
    def render_logs(self):
        """Render recent logs"""
        print("\n📝 RECENT LOGS:")
        print("-"*60)
        try:
            if os.path.exists('logs/bot.log'):
                with open('logs/bot.log', 'r') as f:
                    lines = f.readlines()[-5:]  # Last 5 lines
                    for line in lines:
                        print(line.strip())
            else:
                print("No logs available")
        except:
            print("Error reading logs")
    
    def render_footer(self):
        """Render footer"""
        print("-"*60)
        print("Press Ctrl+C to exit | Active Node: mesh-001")
        print("="*60)
    
    def get_uptime(self):
        """Get formatted uptime"""
        uptime = time.time() - self.start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def format_bytes(bytes_num):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_num < 1024.0:
                return f"{bytes_num:.1f} {unit}"
            bytes_num /= 1024.0
        return f"{bytes_num:.1f} TB"

if __name__ == "__main__":
    import asyncio
    dashboard = TerminalDashboard()
    asyncio.run(dashboard.start())
