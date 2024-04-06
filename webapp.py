from flask import Flask, request, render_template, send_from_directory
from bs4 import BeautifulSoup as bs4
from pathlib import Path
import requests
import qrcode
 
# Flask constructor
app = Flask(__name__)   
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():

  def get_links_from_drive(url):
    req = requests.get(url)
    soup = bs4(req.content, features="html.parser")
    script = [x for x in soup.find_all("script") if "https:\\/\\/drive.google.com\\/file\\/d\\/" in str(x)][0]
    links = [x.split("/")[5].strip("\\") for x in str(script).split(",") if "view" in x]
    titles = [x.text for x in soup.find_all('div', class_="tyTrke")]
    return titles, links

  def generate_qr_codes(filelist):
    qr_links = []
    for link in filelist:
      img = qrcode.make(get_image_link(link))
      filename = f"{link}-qr.png" 
      filepath = str(get_image_path(filename))
      img.save(filepath)
      qr_links.append(filename)
      # download_file(filename)
      print('QR code generated!')
    return qr_links

  def get_image_link(image):
    return f"https://drive.google.com/file/d/{image}/view"
  
  def get_image_path(image):
    outpath = Path("static/images")
    outpath.mkdir(parents=True, exist_ok=True)
    return outpath / image

  def clean_output_dir():
    for file in Path("static").glob("*"):
      file.unlink()
 
  if request.method == "POST":
    url = request.form.get("files") 
    titles, links = get_links_from_drive(url)
    qr_links = generate_qr_codes(links)
    return render_template("links.html", links=zip(titles, qr_links))
  return render_template("form.html")

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = Path.absolute(Path.cwd()) / "static" / "images"
    return send_from_directory(uploads, filename)

if __name__=='__main__':
  # https://drive.google.com/drive/folders/1izOR_sbmrINr59FZSks9zNB-PiKq6kr_?usp=drive_link
  # https://drive.usercontent.google.com/u/0/uc?id=1Q06zKmk164LWnDyNmk2E9SadMzyrMaV5&export=download
  # https://drive.google.com/file/d/1fIHMIOBtAP3Qe5WuARiZZ4IikeAZnoK4/view
  app.run(debug=True, port=5001)