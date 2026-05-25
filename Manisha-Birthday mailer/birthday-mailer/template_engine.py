"""
template_engine.py — Minimal Jinja2-powered template renderer.
Templates live in the templates/ folder.
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_template(template_name: str, context: dict) -> str:
    """Render a template file with the given context dict."""
    template = _env.get_template(template_name)
    return template.render(**context)
