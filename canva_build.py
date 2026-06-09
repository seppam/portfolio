"""Full Canva portfolio creation — connect DIRECTLY to the target's own WebSocket."""
import websocket, json, time

BROWSER_WS = "ws://localhost:9333/devtools/browser/1699bf51-5c98-46ca-b2f1-057904cba506"

def send(ws, method, params=None, id_=1):
    msg = {"jsonrpc": "2.0", "id": id_, "method": method, "params": params or {}}
    ws.send(json.dumps(msg))
    return json.loads(ws.recv())

def run_js(ws, script):
    r = send(ws, "Runtime.evaluate", {"expression": script, "returnByValue": True})
    result = r.get("result", {})
    if result.get("exceptionDetails"):
        return {"error": str(result["exceptionDetails"])}
    return result.get("result", {}).get("value")

def main():
    # Step 1: Create new tab and get its websocket URL
    print("📍 Creating new tab for Canva...")
    ws = websocket.create_connection(BROWSER_WS, timeout=15)
    
    r = send(ws, "Target.createTarget", {"url": "https://www.canva.com/", "newWindow": False})
    target_id = r.get("result", {}).get("targetId")
    print(f"   Target ID: {target_id}")
    ws.close()
    
    # Step 2: Get the websocket URL for this specific target
    print("🔗 Getting target WebSocket URL...")
    ws = websocket.create_connection(BROWSER_WS, timeout=15)
    r = send(ws, "Target.getTargets")
    targets = r.get("result", {}).get("targetInfos", [])
    ws.close()
    
    target_ws_url = None
    for t in targets:
        if t.get("targetId") == target_id:
            target_ws_url = t.get("webSocketDebuggerUrl")
            print(f"   WebSocket URL: {target_ws_url}")
            break
    
    if not target_ws_url:
        print("❌ Could not find target WebSocket URL!")
        # Try to find any Canva target
        for t in targets:
            if "canva" in t.get("url", "").lower():
                target_ws_url = t.get("webSocketDebuggerUrl")
                print(f"   Using Canva target: {t.get('targetId')}")
                print(f"   WebSocket URL: {target_ws_url}")
                target_id = t.get("targetId")
                break
    
    if not target_ws_url:
        print("❌ No Canva target found!")
        return
    
    # Step 3: Connect DIRECTLY to the target's WebSocket
    print(f"\n✅ Connecting directly to target WebSocket...")
    ws = websocket.create_connection(target_ws_url, timeout=15)
    
    # Enable domains
    send(ws, "Page.enable")
    send(ws, "Runtime.enable")
    send(ws, "DOM.enable")
    
    print("⏳ Waiting for Canva to load...")
    time.sleep(6)
    
    url = run_js(ws, "window.location.href")
    title = run_js(ws, "document.title")
    print(f"   URL: {url}")
    print(f"   Title: {title}")
    
    # Check for cookie banner
    print("\n🍪 Checking for cookie banner...")
    result = run_js(ws, """
(function() {
    const btns = Array.from(document.querySelectorAll('button'));
    const accept = btns.find(b => b.textContent.includes('Accept') || b.textContent.includes('accept'));
    if(accept) { accept.click(); return 'ACCEPTED_COOKIES'; }
    return 'no_cookie_banner';
})()
""")
    print(f"   {result}")
    time.sleep(1)
    
    # Find and click Login
    print("\n🔐 Clicking Log in...")
    result = run_js(ws, """
(function() {
    const links = Array.from(document.querySelectorAll('a,button'));
    const loginLink = links.find(l => {
        const t = l.textContent.trim();
        return t === 'Log in' || t === 'Log in to Canva' || t === 'login' || t === 'Sign in';
    });
    if(loginLink) { loginLink.click(); return 'CLICKED: ' + loginLink.textContent.trim(); }
    return 'NOT_FOUND. All links/buttons: ' + links.map(l=>l.textContent.trim()).filter(t=>t.length<30).slice(0,10).join(' | ');
})()
""")
    print(f"   {result}")
    time.sleep(3)
    
    url = run_js(ws, "window.location.href")
    print(f"   URL: {url}")
    
    # Fill email
    print("\n📧 Filling email...")
    result = run_js(ws, """
(function() {
    const inputs = Array.from(document.querySelectorAll('input'));
    const emailInput = inputs.find(i => {
        if(i.type === 'email') return true;
        const ph = (i.placeholder || '').toLowerCase();
        const name = (i.name || '').toLowerCase();
        return ph.includes('email') || name === 'email' || i.autocomplete === 'username';
    });
    if(emailInput) {
        emailInput.focus();
        emailInput.value = '';
        const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
        setter.call(emailInput, 'seppam@hotmail.com');
        emailInput.dispatchEvent(new Event('input', {bubbles: true}));
        emailInput.dispatchEvent(new Event('change', {bubbles: true}));
        return 'FILLED: ' + emailInput.value;
    }
    return 'NOT_FOUND. Inputs: ' + inputs.map(i=>i.type+'|'+i.placeholder).join(' || ');
})()
""")
    print(f"   {result}")
    time.sleep(1)
    
    # Click Continue
    print("▶ Clicking Continue...")
    result = run_js(ws, """
(function() {
    const btns = Array.from(document.querySelectorAll('button'));
    const cont = btns.find(b => {
        const t = b.textContent.trim();
        return t === 'Continue' || t === 'Lanjut' || t === 'Next';
    });
    if(cont) { cont.click(); return 'CLICKED: ' + cont.textContent.trim(); }
    return 'NOT_FOUND. Buttons: ' + btns.map(b=>b.textContent.trim()).filter(t=>t.length<20).join(' | ');
})()
""")
    print(f"   {result}")
    time.sleep(3)
    
    url = run_js(ws, "window.location.href")
    print(f"   URL: {url}")
    
    # Fill password
    print("\n🔑 Filling password...")
    result = run_js(ws, """
(function() {
    const inputs = Array.from(document.querySelectorAll('input'));
    const pwdInput = inputs.find(i => i.type === 'password');
    if(pwdInput) {
        pwdInput.focus();
        pwdInput.value = '';
        const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
        setter.call(pwdInput, 'Seppam@canva11');
        pwdInput.dispatchEvent(new Event('input', {bubbles: true}));
        pwdInput.dispatchEvent(new Event('change', {bubbles: true}));
        return 'FILLED: ' + pwdInput.value;
    }
    return 'NOT_FOUND. Inputs types: ' + inputs.map(i=>i.type).join(' ');
})()
""")
    print(f"   {result}")
    time.sleep(1)
    
    # Click Sign in / Log in
    print("▶ Clicking Sign in...")
    result = run_js(ws, """
(function() {
    const btns = Array.from(document.querySelectorAll('button,input'));
    const signin = btns.find(b => {
        const t = (b.textContent || '').trim().toLowerCase();
        return (t.includes('sign in') && t.length < 20) || (t.includes('log in') && t.length < 20) || t === 'masuk';
    });
    if(signin) { signin.click(); return 'CLICKED: ' + signin.textContent.trim(); }
    return 'NOT_FOUND. Buttons: ' + Array.from(document.querySelectorAll('button')).map(b=>b.textContent.trim()).filter(t=>t.length<25).join(' | ');
})()
""")
    print(f"   {result}")
    time.sleep(6)
    
    # Check login status
    url = run_js(ws, "window.location.href")
    title = run_js(ws, "document.title")
    logged_in = run_js(ws, """
(function() {
    const t = document.title + document.body.textContent;
    return t.includes('Create a design') || t.includes('What will you design') || 
           t.includes('Dashboard') || t.includes('Profile') || t.includes('seppam') ||
           t.includes('My designs') || t.includes('Templates');
})()
""")
    print(f"\n📊 Final URL: {url}")
    print(f"   Title: {title}")
    print(f"   Logged in: {logged_in}")
    
    if logged_in:
        print("\n🎉 Logged in! Navigating to create resume...")
        
        # Navigate to resume templates
        send(ws, "Page.navigate", {"url": "https://www.canva.com/create/resumes/"})
        time.sleep(5)
        
        url = run_js(ws, "window.location.href")
        print(f"   Template page URL: {url}")
        
        # Click first template
        result = run_js(ws, """
(function() {
    // Try various template selectors
    const selectors = [
        'a[href*="/templates/resume"]', 'a[href*="/templates/cv"]',
        '[data-testid="template-card"] a', '.template-card a',
        'a[href*="template"]'
    ];
    for(const sel of selectors) {
        const el = document.querySelector(sel);
        if(el) { el.click(); return 'CLICKED: ' + sel; }
    }
    // Fallback: click any link with template in href
    const links = Array.from(document.querySelectorAll('a[href]'));
    const tpl = links.find(l => l.href.includes('template') || l.href.includes('resume'));
    if(tpl) { tpl.click(); return 'CLICKED_LINK: ' + tpl.href; }
    return 'NOT_FOUND';
})()
""")
        print(f"   Template click: {result}")
        time.sleep(5)
        
        final_url = run_js(ws, "window.location.href")
        final_title = run_js(ws, "document.title")
        print(f"\n✅ Editor URL: {final_url}")
        print(f"   Editor Title: {final_title}")
        print("\n✨ Canva editor should now be open in Chrome!")
        print("   The portfolio design will open in the Canva editor for you to customize.")
    else:
        body_snippet = run_js(ws, "document.body.textContent.substring(0, 300)")
        print(f"\n⚠️  Login may have failed. Body snippet:\n{body_snippet}")
        print("\n   Please check the Chrome window — you may need to complete a CAPTCHA.")
    
    ws.close()
    print("\nDone!")

if __name__ == "__main__":
    main()
