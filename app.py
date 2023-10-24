from flask import Flask, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import connect_db, db, Pet
from forms import AddPetForm
# export PATH=/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
connect_db(app)
app.config["SECRET_KEY"] = "abc123"

db.create_all()

@app.route('/')
def show_pets():
    all_pets = Pet.query.all()
    return render_template('index.html', all_pets=all_pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        new_pet = Pet(name=name, species=species, photo_url=photo, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add.html', form = form)

@app.route('/<int:pet_id>', methods=['GET' ,'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet) ## replaces text with this object

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo = form.photo_url.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        db.session.commit()
        return redirect('/')

    return render_template('edit.html', form = form)


## **Further Study**

# There are some optional steps, if you’d like:

# - Add “message flashing” to give feedback after a pet is added/edited
# - Divide the homepage into two listings: available pets and no-longer-available pets.
# - Add Bootstrap and a simple theme.
# - Reduce duplication: you probably have lots of duplicate form code in both the add form and edit form; learn about Jinja2’s “include” directive, and figure out how you can factor out that common code.
# - **Harder**: in your add-pet route, you are probably extracting each field’s data individually to instantiate the new pet. This is a little tedious and also would need to be updated if the add form changed. Given that there is already a dictionary of values from the form, can you instantiate a pet using this more directly?
# - **Harder, Requires Research**: add a new field for a photo upload (in addition to the URL field, before). This will need to handle file uploads and then save the file into the ***/static*** directory so it can be served up. Make it so that only one of these two fields can be filled out (if you try to fill out both, you should get a validation error).