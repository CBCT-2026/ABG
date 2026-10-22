"""Build the ABG recruitment flyer PDFs (English and Japanese, one-sided A4).

Usage (from this folder):
  python3 build_flyer.py --form-en https://forms.office.com/r/XXXX --form-ja https://forms.office.com/r/YYYY

Leave out a --form-* link and that flyer gets a placeholder QR code marked "PLACEHOLDER".
Needs: python3 -m pip install "qrcode[pil]"  and Chromium/Chrome (set CHROME=/path/to/chrome if not found).
Text is edited in src/flyer-en.html and src/flyer-ja.html; layout and colours in src/flyer.css.
"""
import argparse, glob, os, shutil, subprocess, sys
import qrcode, qrcode.image.svg

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "src"), HERE
PLACEHOLDER_URL = "https://forms.office.com/PLACEHOLDER-replace-with-real-link"

def qr_svg(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage,
                      error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    svg = img.to_string(encoding="unicode")
    return svg[svg.index("<svg"):]

def find_chrome():
    for c in [os.environ.get("CHROME"), *sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")), shutil.which("chromium"),
              shutil.which("chromium-browser"), shutil.which("google-chrome"),
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"]:
        if c and os.path.exists(c):
            return c
    sys.exit("Chrome/Chromium not found: set CHROME=/path/to/chrome")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--form-en"); ap.add_argument("--form-ja")
    a = ap.parse_args()
    chrome = find_chrome()
    for lang, url in (("en", a.form_en), ("ja", a.form_ja)):
        html = open(os.path.join(SRC, f"flyer-{lang}.html"), encoding="utf-8").read()
        qr = qr_svg(url or PLACEHOLDER_URL)
        if not url:
            qr += '<div class="ph"><span>PLACEHOLDER<br>QR CODE</span></div>'
        html = html.replace("{{QR}}", qr)
        built = os.path.join(SRC, f"_built-{lang}.html")
        open(built, "w", encoding="utf-8").write(html)
        pdf = os.path.join(OUT, f"recruitment-flyer-{lang.upper()}.pdf")
        subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--allow-file-access-from-files", "--virtual-time-budget=15000", "--run-all-compositor-stages-before-draw",
                        f"--print-to-pdf={pdf}", "file://" + built], check=True, stderr=subprocess.DEVNULL)
        os.remove(built)
        print("wrote", pdf, "(placeholder QR)" if not url else "")

main()
