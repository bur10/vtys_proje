from flask import Flask, request, render_template, redirect, url_for, flash
from takso import add_driver, delete_driver, get_drivers, get_driver

app = Flask(__name__)


@app.route("/admin")
def admin_home():
    return render_template("admin/index_admin.html")


@app.route("/admin/surucu_ekle", methods=['GET', 'POST'])
def admin_add_driver():
    if request.method == "POST":
        print(request.form['name'])
        add_driver(
            name=request.form['name'],
            last_name=request.form['last_name'],
            photo_link=request.form['photo_link'],
            biography=request.form['biography']
        )
        return redirect(url_for('admin_add_driver'))
    else:
        return render_template("admin/surucu_ekle.html")


@app.route("/admin/surucu_sil/<int:id>", methods=['GET'])
def admin_delete_driver(id):
    delete_driver(id)
    return redirect(url_for('admin_delete_driver_results'))


@app.route("/admin/surucu_sil_ara", methods=['GET', 'POST'])
def admin_delete_driver_results():
    if request.method == "POST":
        return render_template("admin/surucu_sil.html", drivers=get_driver(request.form['name'], request.form['last_name']))
    else:
        return render_template("admin/surucu_sil.html")


@app.route("/")
def home():
    return render_template("user/index.html", drivers=get_drivers())


if __name__ == "__main__":
    app.run()
