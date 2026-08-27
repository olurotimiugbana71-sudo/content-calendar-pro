"""
Visualization Module - Content Calendar Pro
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class Visualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = ['#667EEA', '#764BA2', '#4ECDC4', '#FFD700', '#FF6B6B']
    
    def _to_b64(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        return img
    
    def platform_chart(self, data):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', colors=self.colors)
        ax.set_title('Content by Platform')
        plt.tight_layout()
        return self._to_b64(fig)
    
    def calendar_heatmap(self, week_data):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        html = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:8px;">'
        for i, (date, posts) in enumerate(week_data.items()):
            count = len(posts)
            color = f"hsl(240,{min(80,count*20)}%,{max(40,80-count*10)}%)"
            html += f'<div style="background:{color};padding:12px;border-radius:8px;text-align:center;color:white;"><strong>{days[i]}</strong><br><small>{date[-5:]}</small><br><span style="font-size:20px;">{count}</span></div>'
        html += '</div>'
        return html
    
    def summary_cards(self, analytics):
        return f"""
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div style="background:linear-gradient(135deg,#667EEA,#764BA2);color:white;padding:18px;border-radius:10px;flex:1;min-width:140px;text-align:center;">
                <h4 style="margin:0;">Total Posts</h4>
                <p style="font-size:32px;margin:8px 0;">{analytics['total_posts']}</p>
            </div>
            <div style="background:linear-gradient(135deg,#4ECDC4,#44BD9E);color:white;padding:18px;border-radius:10px;flex:1;min-width:140px;text-align:center;">
                <h4 style="margin:0;">Hashtags</h4>
                <p style="font-size:32px;margin:8px 0;">{analytics['total_hashtags']}</p>
            </div>
        </div>
        """