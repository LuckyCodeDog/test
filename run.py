from tmb_app import create_app
from tmb_app.member import member_bp
from tmb_app.moderator import moderator_bp
from tmb_app.admin import admin_bp
from tmb_app.common import common_bp
from flask import g, session
from flask_hashing import Hashing

app = create_app()

# Register blueprints with URL prefixes
app.register_blueprint(member_bp, url_prefix='/member')
app.register_blueprint(moderator_bp, url_prefix='/moderator')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(common_bp)


@app.context_processor
def inject_global_variable():
    return dict(user_role=session['role'] if 'role' in session else None, user_id=session['id'] if 'id' in session else None)

if __name__ == "__main__":
    app.run(debug=True)