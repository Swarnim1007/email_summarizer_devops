from app import create_app, db  # Import the create_app function and db object from app package

# Create the Flask application
app = create_app()

# Add a context processor to make the 'db' object accessible in the Flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db}

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
