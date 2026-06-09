"""Connect to Canva tab via Chrome CDP and build portfolio."""
import json, time, sys
import websocket

CANVA_WS = "ws://localhost:9222/devtools/page/937A63BD2BBB6144ABF8A9E753FA6010"

def cdp_send(ws, method, params=None, id_=1):
    msg = {"id": id_, "method": method}
    if params:
        msg["params"] = params
    ws.send(json.dumps(msg))

def cdp_recv(ws):
    raw = ws.recv()
    return json.loads(raw)

def cdp_call(ws, method, params=None, id_=1):
    cdp_send(ws, method, params, id_)
    return cdp_recv(ws)

def main():
    ws = websocket.create_connection(CANVA_WS, timeout=20)
    print("✅ Connected to Canva tab")
    
    # Check current URL
    r = cdp_call(ws, "Runtime.evaluate", {"expression": "window.location.href"})
    print(f"Current URL: {r.get('result',{}).get('result',{}).get('value', '?')}")
    
    # Step 1: Accept cookies if shown
    print("\n--- Step 1: Cookie banner ---")
    r = cdp_call(ws, "Runtime.evaluate", {
        "expression": "(function(){ const btns=document.querySelectorAll('button'); for(const b of btns){ if(b.textContent.includes('Accept')){ b.click(); return 'clicked accept'; } } return 'no accept btn'; })()"
    })
    print(f"Accept cookies: {r}")
    time.sleep(1)
    
    # Step 2: Click Log in link in header
    print("\n--- Step 2: Click Log in ---")
    r = cdp_call(ws, "Runtime.evaluate", {
        "expression": "(function(){ const links=document.querySelectorAll('a,button'); for(const l of links){ if(l.textContent.trim()==='Log in'||l.textContent.trim()==='Log in to Canva'){ l.click(); return 'clicked log in'; } } return 'not found'; })()"
    })
    print(f"Click Log in: {r}")
    time.sleep(3)
    
    # Step 3: Check URL after clicking log in
    r = cdp_call(ws, "Runtime.evaluate", {"expression": "window.location.href"})
    print(f"URL after log in click: {r.get('result',{}).get('result',{}).get('value','?')}")
    
    # Step 4: Try to find email input in modal/page
    print("\n--- Step 3: Fill email ---")
    r = cdp_call(ws, "Runtime.evaluate", {
        "expression": """
(function(){
    const selectors = [
        'input[type="email"]', 'input[name="email"]', 'input[placeholder*="email"]',
        'input[placeholder*="Email"]', 'input[autocomplete="email"]', '#email',
        'input[aria-label*="email"]', 'input[aria-label*="Email"]'
    ];
    for(const sel of selectors){
        const el = document.querySelector(sel);
        if(el){ el.focus(); el.value=''; document.execCommand('insertText', false, 'seppam@hotmail.com'); return 'found: '+sel; }
    }
    return 'not found';
})()
"""
    })
    print(f"Fill email result: {r}")
    time.sleep(1)
    
    # Step 5: Click Continue
    print("\n--- Step 4: Click Continue ---")
    r = cdp_call(ws, "Runtime.evaluate", {
        "expression": "(function(){ const btns=document.querySelectorAll('button'); for(const b of btns){ const t=b.textContent.trim(); if(t==='Continue'||t==='Lanjut'||t.includes('Continue')){ b.click(); return 'clicked: '+t; } } return 'not found'; })()"
    })
    print(f"Click Continue: {r}")
    time.sleep(3)
    
    # Step 6: Check if password field appeared
    print("\n--- Step 5: Fill password ---")
    r = cdp_call(ws, "Runtime.evaluate", {
        "expression": """
(function(){
    const selectors = ['input[type="password"]', 'input[name="password"]', 'input[placeholder*="password"]', 'input[placeholder*="Password"]'];
    for(const sel of selectors){
        const el = document.querySelector(sel);
        if(el){ el.focus(); el.value=''; document.execCommand('insertText', false, 'Seppam@canva11'); return 'found: '+sel; }
    }
    return 'not found';
})()
"""
    })
    print(f"Fill password result: {r}")
    time.sleep(1)
    
    # Step 7: Click Sign in
    print("\n--- Step 6: Click Sign in ---")
    r = cdp_call(ws, "Runtime.evaluate", {
        "expression": "(function(){ const btns=document.querySelectorAll('button,input[type=submit]'); for(const b of btns){ const t=b.textContent.trim(); if(t.includes('Sign in')||t.includes('Log in')||t.includes('Masuk')){ b.click(); return 'clicked: '+t; } } return 'not found'; })()"
    })
    print(f"Sign in result: {r}")
    time.sleep(5)
    
    # Check final URL
    r = cdp_call(ws, "Runtime.evaluate", {"expression": "window.location.href"})
    print(f"\nFinal URL: {r.get('result',{}).get('result',{}).get('value','?')}")
    
    # Check page title
    r = cdp_call(ws, "Runtime.evaluate", {"expression": "document.title"})
    print(f"Page title: {r.get('result',{}).get('result',{}).get('value','?')}")
    
    ws.close()
    print("\nDone!")

if __name__ == "__main__":
    main()
