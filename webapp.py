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
    if "Sign-in" in soup.find("title").text:
      raise Exception("Provide public link")
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
      print('QR code generated!')
    return qr_links

  def get_image_link(image):
    return f"https://drive.google.com/file/d/{image}/view"
  
  def get_image_path(image):
    outpath = Path("static/images")
    outpath.mkdir(parents=True, exist_ok=True)
    return outpath / image

  if request.method == "POST":
    try:
      url = request.form.get("files") 
      titles, links = get_links_from_drive(url)
      qr_links = generate_qr_codes(links)
      return render_template("links.html", links=zip(titles, qr_links))
    except Exception as e:
      if str(e) == "Provide public link":
        return render_template("form.html", message=e)
      else:
        return render_template("form.html", message="Invalid URL")
  return render_template("form.html")

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = Path.absolute(Path.cwd()) / "static" / "images"
    return send_from_directory(uploads, filename)

if __name__=='__main__':
  app.run(debug=True, port=5001)
