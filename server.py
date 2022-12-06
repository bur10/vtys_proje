import random
from flask import Flask, request, render_template, redirect, url_for, flash
from takso import Drivers, Customers, Taxis, ActiveVoyages, PastVoyages
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

selected_customer = 4


# --- ADMIN ROUTES ---

@app.route("/admin")
def admin_home():
    return render_template("admin/index_admin.html")

# --- TAXI ROUTES ---


@app.route('/admin/taksi_ekle', methods=['GET', 'POST'])
def admin_add_taxi():
    if request.method == "POST":
        print(request.form['plate_number'])
        Taxis.add_taxi(
            plate_number=request.form['plate_number'],
            car_model=request.form['car_model'],
            car_year=request.form['car_year']
        )
        return redirect(url_for('admin_add_taxi'))
    else:
        return render_template("admin/taxi/taksi_ekle.html")


@app.route("/admin/taksi_sil", methods=['GET', 'POST'])
def admin_delete_taxi():
    if request.method == "POST":
        print(request.form['plate_number'])
        if Taxis.delete_taxi(plate_number=request.form['plate_number']) == -1:
            flash("Yolculukta olan taksiyi silemezsiniz!", "danger")
        else:
            flash("Taksiyi başarıyla sildiniz!", "success")
        return redirect(url_for('admin_delete_taxi'))
    else:
        return render_template("admin/taxi/taksi_sil.html")


@app.route("/admin/taksi_sil/<int:id>", methods=['GET'])
def admin_delete_taxi_by_id(id):
    Taxis.delete_taxi(id=id)
    return redirect(url_for('admin_show_taxis'))


@app.route("/admin/taksi_goster", methods=['GET'])
def admin_show_taxis():
    return render_template("admin/taxi/taksi_goster.html", taxis=Taxis.get_all_taxis())

# --- CUSTOMER ROUTES ---


@app.route('/admin/musteri_ekle', methods=['GET', 'POST'])
def admin_add_customer():
    if request.method == "POST":
        print(request.form['name'])
        Customers.add_customer(
            name=request.form['name'],
            last_name=request.form['last_name'],
            phone_number=request.form['phone_number'],
            address=request.form['address']
        )
        return redirect(url_for('admin_add_customer'))
    else:
        return render_template("admin/customer/musteri_ekle.html")


@app.route('/admin/musteri_duzenle/<int:id>', methods=['GET', 'POST'])
def admin_update_customer(id):
    if request.method == 'POST':
        print(id)
        Customers.update_customer(
            id=id,
            name=request.form['name'],
            last_name=request.form['last_name'],
            phone_number=request.form['phone_number'],
            address=request.form['address']
        )
        return redirect(url_for('admin_update_customer', id=id))
    else:
        return render_template("admin/customer/musteri_duzenle.html", customer=Customers.get_customer_by_id(id))


@app.route("/admin/musteri_sil/<int:id>", methods=['GET'])
def admin_delete_customer(id):
    if Customers.delete_customer(id) == -1:
        flash("Yolculukta olan yolcuyu silemezsiniz!", "danger")
    else:
        flash("Yolcuyu başarılı bir şekilde sildiniz!", "success")
    return redirect(url_for('admin_customer_results'))


@app.route("/admin/musteri_ara", methods=['GET', 'POST'])
def admin_customer_results():
    if request.method == "POST":
        return render_template("admin/customer/musteri_ara.html", customers=Customers.get_customer_by_name(request.form['name'], request.form['last_name']))
    else:
        return render_template("admin/customer/musteri_ara.html")

# --- END CUSTOMER ROUTES ---

# --- DRIVER ROUTES ---


@app.route("/admin/surucu_ekle", methods=['GET', 'POST'])
def admin_add_driver():
    if request.method == "POST":
        print(request.form['name'])
        Drivers.add_driver(
            name=request.form['name'],
            last_name=request.form['last_name'],
            photo_link=request.form['photo_link'],
            biography=request.form['biography']
        )
        return redirect(url_for('admin_add_driver'))
    else:
        return render_template("admin/driver/surucu_ekle.html")


@app.route("/admin/surucu_duzenle/<int:id>", methods=['GET', 'POST'])
def admin_update_driver(id):
    if request.method == 'POST':
        print(id)
        Drivers.update_driver(
            id=id,
            name=request.form['name'],
            last_name=request.form['last_name'],
            photo_link=request.form['photo_link'],
            biography=request.form['biography']
        )
        return redirect(url_for('admin_update_driver', id=id))
    else:
        return render_template("admin/driver/surucu_duzenle.html", driver=Drivers.get_driver_by_id(id))


@app.route("/admin/surucu_sil/<int:id>", methods=['GET'])
def admin_delete_driver(id):
    if Drivers.delete_driver(id) == -1:
        flash("Yolculukta olan bir sürücüyü silemezsiniz", "danger")
    else:
        flash("Sürücü başarıyla silindi!", "success")
    return redirect(url_for('admin_driver_results'))


@app.route("/admin/surucu_ara", methods=['GET', 'POST'])
def admin_driver_results():
    if request.method == "POST":
        return render_template("admin/driver/surucu_ara.html", drivers=Drivers.get_driver_by_name(request.form['name'], request.form['last_name']))
    else:
        return render_template("admin/driver/surucu_ara.html")

# --- END DRIVER ROUTES ---

# --- END ADMIN ROUTES ---

# --- USER ROUTES ---


@app.route("/")
def home():
    active_voyage = ActiveVoyages.get_customer_active_voyage(selected_customer)
    voyage_info = {}
    if active_voyage != None:
        voyage_info = {
            'driver_info': Drivers.get_driver_by_id(active_voyage['driver_id']),
            'taxi_info': Taxis.get_taxi_by_id(active_voyage['taxi_id']),
            'where_to': active_voyage['where_to'],
            'where_from': active_voyage['where_from'],
        }
    return render_template("user/index.html", available_drivers=Drivers.get_available_drivers(), voyage_info=voyage_info)

@app.route("/user/profil")
def user_profile():
    return render_template("user/profil.html", user=Customers.get_customer_by_id(selected_customer))


@app.route("/user/surucu_cagir/<int:driver_id>")
def call_driver(driver_id):
    res = ActiveVoyages.add_active_voyage(
        customer_id=selected_customer,
        driver_id=driver_id,
        taxi_id=random.choice([taxi['id'] for taxi in Taxis.get_all_taxis()]),
        where_to="Teknoloji Fakültesi",
        where_from=Customers.get_customer_by_id(selected_customer)['address']
    )
    if res == -1:
        flash("Sürücü çağırma başarısız! Zaten aktif bir yolculuğunuz var!", 'danger')
    else:
        flash("Yolculuğunuz başladı!", "success")
    return redirect(url_for('home'))

@app.route("/user/surusu_bitir", methods=['POST'])
def end_voyage():
    voyage = ActiveVoyages.get_customer_active_voyage(selected_customer)
    time_passed = (datetime.now() - voyage['call_date']).seconds
    total_try = round((time_passed/60) * 7, 2)
    if voyage != None:
        PastVoyages.add_past_voyage(
            active_voyage_id=voyage['id'],
            customer_id=voyage['customer_id'],
            driver_id=voyage['driver_id'],
            taxi_id=voyage['taxi_id'],
            where_to=voyage['where_to'],
            where_from=voyage['where_from'],
            call_date=voyage['call_date'],
            end_date=datetime.now(),
            rating=int(request.form['rating']),
            total=total_try,
        )
    else:
        print("aktif voyage yok!")
    return redirect(url_for('home'))


@app.route("/user/tum_surusler")
def all_voyages():
    voyages = [{"driver_info": Drivers.get_driver_by_id(voyage['driver_id']),
                "taxi_info": Taxis.get_taxi_by_id(voyage['taxi_id']),
                "where_to": voyage['where_to'],
                "where_from": voyage['where_from'],
                "total": voyage['total'],
                "rating": voyage['rating'],
                "total_minutes": round(((voyage["end_date"] - voyage['call_date']).seconds)/60, 2),
                "call_date": voyage['call_date']} for voyage in PastVoyages.get_all_voyages(selected_customer)]
    return render_template("user/gecmis_surusler.html", voyages=reversed(voyages))


# --- END USER ROUTES ---


if __name__ == "__main__":
    app.run()
