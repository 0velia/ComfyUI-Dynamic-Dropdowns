import os
import sys
import webview

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, working correctly both 
        during local development and after compilation inside PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # Locate the embedded HTML generator file
    html_path = get_resource_path("generator.html")
    
    # Create the standalone window environment
    window = webview.create_window(
        title="Universal Dropdown Node Generator",
        url=html_path,
        width=900,
        height=850,
        resizable=True
    )
    
    # Force the local OS renderer (WebView2 Edge Chromium on Windows) 
    # so the interface looks identical and functions smoothly offline on all PCs
    webview.start(gui="cef" if os.name != "nt" else "mshtml" if not html_path else None)