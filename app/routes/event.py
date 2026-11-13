from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from extension import db
from app.decorator import permission_required
from app.models import Category, Event, Location, EventType
from datetime import datetime
import cloudinary.uploader

event = Blueprint('event', __name__)


@event.route('/view')
@login_required
def view_event():
    
    return render_template('views/events.html')



@event.route('/manage')
@login_required
@permission_required(['manage_event'])
def manage_event():
    
    return render_template('views/manage_event.html')



@event.route('/my-manage')
@login_required
@permission_required(['manage_event'])
def host_event():
    my_events = (
        Event.query
        .filter_by(author_id=current_user.id)
        .order_by(Event.created_at.desc())
        .all()
    )
    return render_template('views/host_event.html', events=my_events)




@event.route('/manage-vendor')
@login_required
@permission_required(['manage_service'])
def manage_vendor():
    return render_template('views/manage_vendor.html')

@event.route('/new', methods=["GET", 'POST'])
@login_required
@permission_required(['manage_event'])
def create_event():
    if request.method == "POST":
        # 1. Extract form fields
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category_val = request.form.get("category")
        venue_name = request.form.get("venue_name", "").strip()

        start_date_str = request.form.get("start_date")  # e.g., "2026-11-20"
        start_time_str = request.form.get("start_time")  # e.g., "09:00"
        end_date_str = request.form.get("end_date")      # e.g., "2026-11-20"
        end_time_str = request.form.get("end_time")      # e.g., "17:00"

        # 2. Validate & parse dates and times into Python datetime objects
        try:
            start_date_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date_dt = datetime.strptime(end_date_str, "%Y-%m-%d")

            # Combine date + time so start_time & end_time are valid DateTime objects
            start_time_dt = datetime.strptime(
                f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M"
            )
            end_time_dt = datetime.strptime(
                f"{end_date_str} {end_time_str}", "%Y-%m-%d %H:%M"
            )

            if end_time_dt < start_time_dt:
                flash("End date/time cannot be before start date/time.", "error")
                return redirect(url_for("event.create_event"))

        except (ValueError, TypeError):
            flash("Please provide valid start and end dates and times.", "error")
            return redirect(url_for("event.create_event"))

        # 3. Upload cover image to Cloudinary
        img_url = None
        cover_file = request.files.get("cover_image")
        if cover_file and cover_file.filename != "":
            try:
                upload_result = cloudinary.uploader.upload(
                    cover_file,
                    folder="events/covers",
                    resource_type="image",
                    transformation=[
                        {"width": 1920, "height": 1080, "crop": "limit"},
                        {"quality": "auto", "fetch_format": "auto"},
                    ],
                )
                img_url = upload_result.get("secure_url")
            except Exception as e:
                flash(f"Image upload failed: {str(e)}", "error")
                return redirect(url_for("event.create_event"))

        # 4. Handle Location (Find existing or create new Location record)
        location_id = None
        if venue_name:
            location = Location.query.filter_by(name=venue_name).first()
            if not location:
                location = Location(name=venue_name)
                db.session.add(location)
                db.session.flush()  # Generates location.id before commit
            location_id = location.id

        # 5. Create Event instance
        new_event = Event(
            title=title,
            description=description,
            img_url=img_url,
            start_date=start_date_dt,
            end_date=end_date_dt,
            start_time=start_time_dt,
            end_time=end_time_dt,
            location_id=location_id,
            author_id=current_user.id,
            event_type=EventType.MEETUP,  # Uses your Enum default
        )

        # 6. Attach Category (Many-to-Many relationship)
        if category_val:
            # Match by slug/name depending on your Category model columns
            category = Category.query.filter(
                (Category.id == category_val) | (Category.name.ilike(category_val))
            ).first()
            if category:
                new_event.categories.append(category)

        # 7. Commit transaction safely
        try:
            db.session.add(new_event)
            db.session.commit()
            flash("Event created successfully!", "success")
            return redirect(url_for("event.create_event"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while saving the event.", "error")
            return redirect(url_for("event.create_event"))


    categories = Category.query.all()
    return render_template("views/create_event.html", categories=categories)