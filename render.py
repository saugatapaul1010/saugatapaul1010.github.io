import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright

src_dir = '/home/neo/Desktop/Claude_Total_Replication/Blog/source'
out_dir = '/home/neo/Desktop/Claude_Total_Replication/Blog/diagrams'

html_files = [
    '01-iceberg.html',
    '02-hook-fire-order.html',
    '03-statusline-anatomy.html',
    '04-memory-ladder.html',
    '05-skill-invocation-flow.html',
    '06-agent-decision-tree.html',
    '07-mcp-fleet-topology.html',
    '08-mission-lifecycle.html',
    '09-weekly-composition.html',
    '10-setup-architecture.html',
    '11-overall-architecture.html',
    '12-memory-tier-flow.html',
    '13-mcp-topology.html',
    '14-five-year-retrieval.html',
    '15-agent-dispatch.html'
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for f in html_files:
        src_path = os.path.join(src_dir, f)
        out_name = f.replace('.html', '.png')
        out_path = os.path.join(out_dir, out_name)
        if os.path.exists(src_path):
            print(f"Rendering {src_path} ...")
            page.goto(f"file://{src_path}")
            page.wait_for_timeout(500) 
            
            # Since some pages like 01-iceberg have body { width: 1400px; height: auto }
            # We want to clip to the body size.
            clip_box = page.evaluate('''() => {
                const body = document.body;
                return {
                    x: 0,
                    y: 0,
                    width: body.scrollWidth,
                    height: body.scrollHeight
                };
            }''')
            
            # Use viewport size to avoid capturing large blank areas
            page.set_viewport_size({"width": clip_box["width"], "height": clip_box["height"]})
            page.screenshot(path=out_path, clip=clip_box)
            print(f"Saved {out_path}")
    browser.close()
