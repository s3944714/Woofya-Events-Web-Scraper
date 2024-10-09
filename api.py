from flask import Flask, request, jsonify
import pyodbc

# Flask app setup
app = Flask(__name__)

# Define the connection string for SQL Server
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-9UFQHR5\\WOOFYASERVER;"  # Replace with your server name
    "Database=events_db;"                     # Replace with your database name
    "Trusted_Connection=yes;"                 # Use Windows Authentication (no username and password required)
)

# Print the connection string for debugging (optional)
print(f"Database Connection String: {connection_string}")

# Define a simple root route
@app.route('/', methods=['GET'])
def home():
    return "API is running. Use the /events endpoint to fetch data."

# Define a route to get all events from the database
@app.route('/events', methods=['GET'])
def get_events():
    """
    Endpoint to retrieve all events.
    """
    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Execute the query
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()

        # Convert results to a list of dictionaries
        columns = [column[0] for column in cursor.description]
        events = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()
        return jsonify(events)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define a route to get an event by its ID
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    """
    Endpoint to retrieve a specific event by ID.
    """
    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Execute the query to get the event by ID
        cursor.execute("SELECT * FROM events WHERE id = ?", event_id)
        row = cursor.fetchone()

        if row:
            columns = [column[0] for column in cursor.description]
            event = dict(zip(columns, row))
            cursor.close()
            conn.close()
            return jsonify(event)
        else:
            cursor.close()
            conn.close()
            return jsonify({"error": "Event not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define a route to create a new event
@app.route('/events', methods=['POST'])
def create_event():
    """
    Endpoint to create a new event.
    """
    try:
        new_event = request.json  # Parse the incoming request data as JSON
        title = new_event.get('title', '')
        location = new_event.get('location', '')
        description = new_event.get('description', '')
        features = new_event.get('features', '')
        date_range = new_event.get('date_range', '')
        link = new_event.get('link', '')

        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Insert a new record into the events table
        cursor.execute("""
            INSERT INTO events (title, location, description, features, date_range, link)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, location, description, features, date_range, link))

        # Commit the transaction
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "Event created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define a route to update an existing event by its ID
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """
    Endpoint to update a specific event by ID.
    """
    try:
        update_data = request.json  # Parse the incoming request data as JSON
        title = update_data.get('title', '')
        location = update_data.get('location', '')
        description = update_data.get('description', '')
        features = update_data.get('features', '')
        date_range = update_data.get('date_range', '')
        link = update_data.get('link', '')

        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Update the existing record
        cursor.execute("""
            UPDATE events SET title = ?, location = ?, description = ?, features = ?, date_range = ?, link = ?
            WHERE id = ?
        """, (title, location, description, features, date_range, link, event_id))

        # Commit the transaction
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Event updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define a route to delete an event by its ID
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """
    Endpoint to delete a specific event by ID.
    """
    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Execute the delete command
        cursor.execute("DELETE FROM events WHERE id = ?", event_id)

        # Commit the transaction
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Event deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app on port 5001
if __name__ == '__main__':
    app.run(debug=True)
