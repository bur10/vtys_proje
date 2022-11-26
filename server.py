from flask import Flask, request, render_template, redirect, url_for, flash
from takso import add_driver, delete_driver, get_drivers, get_driver_by_name, get_driver_by_id, update_driver

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


@app.route("/admin/surucu_duzenle/<int:id>", methods=['GET', 'POST'])
def admin_update_driver(id):
    if request.method == 'POST':
        print(request.form['id'])
        update_driver(
            id=request.form['id'],
            name=request.form['name'],
            last_name=request.form['last_name'],
            photo_link=request.form['photo_link'],
            biography=request.form['biography']
        )
        return redirect(url_for('admin_update_driver', id=request.form['id']))
    else:
        return render_template("admin/surucu_duzenle.html", driver=get_driver_by_id(id))

@app.route("/admin/surucu_sil/<int:id>", methods=['GET'])
def admin_delete_driver(id):
    delete_driver(id)
    return redirect(url_for('admin_driver_results'))


@app.route("/admin/surucu_ara", methods=['GET', 'POST'])
def admin_driver_results():
    if request.method == "POST":
        return render_template("admin/surucu_ara.html", drivers=get_driver_by_name(request.form['name'], request.form['last_name']))
    else:
        return render_template("admin/surucu_ara.html")


@app.route("/")
def home():
    return render_template("user/index.html", drivers=get_drivers())


if __name__ == "__main__":
    app.run()
