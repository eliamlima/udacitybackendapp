from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#"This page will show all my restaurants"
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

#"This page will be for making a new restaurant"
@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

#"This page will be for editing restaurant %s" % restaurant_id
@app.route('/restaurants/<int:id>/edit', methods=['GET', 'POST'])
def editRestaurant(id):
    edited = session.query(Restaurant).filter_by(id = id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited.name = request.form['name']
            session.add(edited)
            session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', e = edited)

#"This page will be for deleting restaurant %s" % restaurant_id
@app.route('/restaurants/<int:id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(id):
    toDelete = session.query(Restaurant).filter_by(id = id).one()
    if request.method == 'POST':
        session.delete(toDelete)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', d = toDelete)

#"This page is the menu for restaurant %s" % restaurant_id
@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', r = restaurant, items = items)

#"This page is for making a new menu item for restaurant %s" % restaurant_id
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id =
            restaurant_id, description = request.form['description'], price =
            request.form['price'], course = request.form['course'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', )

#"This page is for editing menu item %s" % menu_id
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            session.add(editedItem)
            session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', e = editedItem)

#"This page is for deleting menu item %s" % menu_id
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    toDeleteItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(toDeleteItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', d = toDeleteItem)

#JSON All Restaurants
@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[r.serialize for r in restaurants])

#JSON All Menu from a restaurant_id
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(Menu=[m.serialize for m in menu])

#JSON All Menu from a restaurant_id
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem=[item.serialize])

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
