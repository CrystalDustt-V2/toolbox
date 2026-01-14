from toolbox import __version__

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
except ModuleNotFoundError:
    FastAPI = None
    HTMLResponse = None

app = FastAPI(title="ToolBox Dashboard") if FastAPI is not None else None


def _ensure_plugins_loaded() -> None:
    from toolbox.core.plugin import plugin_manager

    if plugin_manager.plugins:
        return
    plugin_manager.load_plugins()


def api_status():
    from toolbox.core.engine import engine_registry
    from toolbox.core.plugin import plugin_manager

    _ensure_plugins_loaded()

    engines = []
    for name, available, hint in engine_registry.check_all():
        engine = engine_registry.get(name)
        engines.append(
            {
                "name": name,
                "available": bool(available),
                "path": engine.path if available else None,
                "hint": None if available else hint,
            }
        )

    plugins = []
    for name, plugin in plugin_manager.plugins.items():
        md = plugin.get_metadata()
        plugins.append(
            {
                "name": name,
                "engine": md.engine,
                "commands": md.commands,
                "version": md.version,
            }
        )

    plugins.sort(key=lambda p: p["name"])
    engines.sort(key=lambda e: e["name"].lower())

    return {"version": __version__, "engines": engines, "plugins": plugins}


def read_root():
    html = f"""<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>ToolBox Dashboard</title>
    <style>
      :root {{
        --bg: #0b1220;
        --panel: #0f1a2b;
        --border: #1f2a3a;
        --text: #e5e7eb;
        --muted: #94a3b8;
        --good: #22c55e;
        --bad: #ef4444;
        --accent: #60a5fa;
      }}

      body {{
        margin: 0;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, Noto Sans,
          \"Apple Color Emoji\", \"Segoe UI Emoji\";
        background: var(--bg);
        color: var(--text);
      }}

      .wrap {{
        max-width: 1100px;
        margin: 0 auto;
        padding: 28px 18px 48px;
      }}

      header {{
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 16px;
        padding-bottom: 18px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 18px;
      }}

      h1 {{
        margin: 0;
        letter-spacing: -0.02em;
        font-size: 28px;
      }}

      .muted {{
        color: var(--muted);
        font-size: 13px;
      }}

      .grid {{
        display: grid;
        grid-template-columns: 1.15fr 0.85fr;
        gap: 16px;
      }}

      @media (max-width: 980px) {{
        .grid {{
          grid-template-columns: 1fr;
        }}
      }}

      .card {{
        border: 1px solid var(--border);
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0.0));
        background-color: var(--panel);
        border-radius: 14px;
        padding: 16px;
      }}

      .card h2 {{
        margin: 0 0 10px;
        font-size: 16px;
      }}

      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th,
      td {{
        padding: 10px 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        text-align: left;
        vertical-align: top;
        font-size: 13px;
      }}
      th {{
        color: var(--muted);
        font-weight: 600;
      }}

      .pill {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.12);
      }}
      .good {{
        color: var(--good);
      }}
      .bad {{
        color: var(--bad);
      }}

      code {{
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1px 6px;
        border-radius: 6px;
        font-size: 12px;
      }}

      .kvs {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
      }}
      .kv {{
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(0, 0, 0, 0.18);
        border-radius: 12px;
        padding: 12px;
      }}
      .kv .k {{
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }}
      .kv .v {{
        margin-top: 6px;
        font-size: 16px;
        font-weight: 700;
      }}
      .link {{
        color: var(--accent);
        text-decoration: none;
      }}
      .link:hover {{
        text-decoration: underline;
      }}
    </style>
  </head>
  <body>
    <div class=\"wrap\">
      <header>
        <div>
          <h1>ToolBox Dashboard</h1>
          <div class=\"muted\">Version: <code>{__version__}</code></div>
        </div>
        <div class=\"muted\">
          Use <code>toolbox status</code> and <code>toolbox check</code> for CLI output.
        </div>
      </header>

      <div class=\"grid\">
        <div class=\"card\">
          <h2>Engines</h2>
          <table>
            <thead>
              <tr>
                <th style=\"width: 160px\">Engine</th>
                <th style=\"width: 120px\">Status</th>
                <th>Path / Hint</th>
              </tr>
            </thead>
            <tbody id=\"engines\">
              <tr><td colspan=\"3\" class=\"muted\">Loading…</td></tr>
            </tbody>
          </table>
        </div>

        <div class=\"card\">
          <h2>Plugins</h2>
          <div class=\"kvs\">
            <div class=\"kv\"><div class=\"k\">Installed Plugins</div><div class=\"v\" id=\"pluginCount\">—</div></div>
            <div class=\"kv\"><div class=\"k\">Total Commands</div><div class=\"v\" id=\"commandCount\">—</div></div>
          </div>
          <div style=\"margin-top: 12px\" class=\"muted\">
            Tip: <code>toolbox plugin list</code> prints a full list.
          </div>
          <div style=\"margin-top: 12px\">
            <a class=\"link\" href=\"/api/status\">/api/status</a>
          </div>
        </div>
      </div>

      <footer style=\"margin-top: 22px\" class=\"muted\">
        ToolBox is offline-first; this dashboard renders local state.
      </footer>
    </div>

    <script>
      function escapeHtml(s) {{
        return String(s)
          .replaceAll('&', '&amp;')
          .replaceAll('<', '&lt;')
          .replaceAll('>', '&gt;')
          .replaceAll('"', '&quot;')
          .replaceAll("'", '&#039;');
      }}

      fetch('/api/status')
        .then((r) => r.json())
        .then((data) => {{
          const engines = data.engines || [];
          const plugins = data.plugins || [];

          document.getElementById('pluginCount').textContent = String(plugins.length);
          const totalCommands = plugins.reduce((acc, p) => acc + (p.commands ? p.commands.length : 0), 0);
          document.getElementById('commandCount').textContent = String(totalCommands);

          const rows = engines
            .map((e) => {{
              const ok = !!e.available;
              const status = ok
                ? '<span class="pill good">AVAILABLE</span>'
                : '<span class="pill bad">MISSING</span>';
              const detail = ok ? e.path : e.hint;
              return `<tr><td>${{escapeHtml(e.name)}}</td><td>${{status}}</td><td class="muted">${{escapeHtml(detail || '')}}</td></tr>`;
            }})
            .join('');

          document.getElementById('engines').innerHTML = rows || '<tr><td colspan="3" class="muted">No engines registered.</td></tr>';
        }})
        .catch((err) => {{
          document.getElementById('engines').innerHTML = `<tr><td colspan="3" class="bad">Failed to load status: ${{escapeHtml(err)}}</td></tr>`;
        }});
    </script>
  </body>
</html>"""
    return HTMLResponse(content=html)


if app is not None:
    app.get("/api/status")(api_status)
    app.get("/", response_class=HTMLResponse)(read_root)

def start_dashboard(host: str = "127.0.0.1", port: int = 8000):
    if app is None:
        raise ModuleNotFoundError(
            "fastapi is required for the dashboard. Install with: pip install 'toolbox-universal[dev]' or pip install fastapi uvicorn"
        )

    import uvicorn

    uvicorn.run(app, host=host, port=port)
