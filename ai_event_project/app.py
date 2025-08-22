from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')

# In-memory event store (replace with DB in prod)
events = []

def generate_ai_promo(event):
    promo = (
        f"Don't miss '{event['title']}' — "
        f"A {event['type']} happening on {event['date']} at {event['location']}. "
        f"Highlights include: {event['description']}. "
        "Register now to reserve your spot!"
    )
    return promo

@app.route('/')
def index():
    return render_template('index.html', events=events)

@app.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        event_type = request.form['type']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']
        event = {
            'id': len(events),
            'title': title,
            'type': event_type,
            'date': date,
            'location': location,
            'description': description,
        }
        events.append(event)
        return redirect(url_for('index'))
    return render_template('create_event.html')

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = events[event_id]
    promo_msg = generate_ai_promo(event)
    return render_template('event_detail.html', event=event, promo=promo_msg)

# ----- NEW: Update Event -----

@app.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    event = events[event_id]
    if request.method == 'POST':
        event['title'] = request.form['title']
        event['type'] = request.form['type']
        event['date'] = request.form['date']
        event['location'] = request.form['location']
        event['description'] = request.form['description']
        return redirect(url_for('event_detail', event_id=event_id))
    return render_template('edit_event.html', event=event)

# ----- NEW: Delete Event -----

@app.route('/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    if 0 <= event_id < len(events):
        events.pop(event_id)
        # Reset event ids to ensure indexing remains correct
        for i, event in enumerate(events):
            event['id'] = i
    return redirect(url_for('index'))

if __name__ == '_main_':
    app.run(debug=True)