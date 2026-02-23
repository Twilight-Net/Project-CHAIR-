import os, json, uuid, time
from flask import Flask, request, jsonify, send_from_directory, send_file

app = Flask(__name__, static_folder='static')

ADMIN_PASS = "1258"
DB_FILE    = "db.json"
UPLOAD_DIR = "uploads"

# ── DB helpers ────────────────────────────────────────────────────
def load_db():
    if not os.path.exists(DB_FILE):
        return {"videos": [], "channels": [], "likes": {}, "follows": {}}
    with open(DB_FILE) as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

# ── Static files ──────────────────────────────────────────────────
@app.route("/")
def index():
    return send_file("index.html")

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# ── Admin: upload video ───────────────────────────────────────────
@app.route("/api/upload", methods=["POST"])
def upload_video():
    if request.form.get("pass") != ADMIN_PASS:
        return jsonify({"error": "Unauthorized"}), 403

    video     = request.files.get("video")
    thumbnail = request.files.get("thumbnail")
    title     = request.form.get("title", "Untitled")
    channel   = request.form.get("channel", "General")
    desc      = request.form.get("desc", "")
    vtype     = request.form.get("type", "video")  # video | short

    if not video:
        return jsonify({"error": "No video file"}), 400

    vid_id    = str(uuid.uuid4())[:8]
    vid_ext   = os.path.splitext(video.filename)[1] or ".mp4"
    subdir    = "shorts" if vtype == "short" else "videos"
    vid_name  = f"{vid_id}{vid_ext}"
    video.save(os.path.join(UPLOAD_DIR, subdir, vid_name))

    thumb_path = ""
    if thumbnail:
        th_ext   = os.path.splitext(thumbnail.filename)[1] or ".jpg"
        th_name  = f"{vid_id}{th_ext}"
        thumbnail.save(os.path.join(UPLOAD_DIR, "thumbnails", th_name))
        thumb_path = f"uploads/thumbnails/{th_name}"

    db = load_db()

    # auto-create channel if missing
    ch_names = [c["name"] for c in db["channels"]]
    if channel not in ch_names:
        db["channels"].append({"id": str(uuid.uuid4())[:8], "name": channel, "avatar": ""})

    db["videos"].append({
        "id":        vid_id,
        "title":     title,
        "channel":   channel,
        "desc":      desc,
        "type":      vtype,
        "src":       f"uploads/{subdir}/{vid_name}",
        "thumb":     thumb_path,
        "uploaded":  int(time.time()),
        "views":     0,
    })
    save_db(db)
    return jsonify({"ok": True, "id": vid_id})

# ── Admin: delete video ───────────────────────────────────────────
@app.route("/api/delete/<vid_id>", methods=["POST"])
def delete_video(vid_id):
    if request.json.get("pass") != ADMIN_PASS:
        return jsonify({"error": "Unauthorized"}), 403
    db = load_db()
    video = next((v for v in db["videos"] if v["id"] == vid_id), None)
    if not video:
        return jsonify({"error": "Not found"}), 404
    # delete files
    for path in [video.get("src",""), video.get("thumb","")]:
        if path and os.path.exists(path):
            os.remove(path)
    db["videos"] = [v for v in db["videos"] if v["id"] != vid_id]
    save_db(db)
    return jsonify({"ok": True})

# ── Get all videos ────────────────────────────────────────────────
@app.route("/api/videos")
def get_videos():
    db  = load_db()
    uid = request.args.get("uid", "anon")
    for v in db["videos"]:
        v["likes"]     = len(db["likes"].get(v["id"], []))
        v["liked"]     = uid in db["likes"].get(v["id"], [])
    return jsonify(db["videos"])

# ── Get channels ──────────────────────────────────────────────────
@app.route("/api/channels")
def get_channels():
    db  = load_db()
    uid = request.args.get("uid", "anon")
    for c in db["channels"]:
        c["follows"]   = len(db["follows"].get(c["name"], []))
        c["following"] = uid in db["follows"].get(c["name"], [])
        # video count
        c["videos"]    = len([v for v in db["videos"] if v["channel"] == c["name"]])
    return jsonify(db["channels"])

# ── Like toggle ───────────────────────────────────────────────────
@app.route("/api/like/<vid_id>", methods=["POST"])
def toggle_like(vid_id):
    uid = request.json.get("uid", "anon")
    db  = load_db()
    lst = db["likes"].setdefault(vid_id, [])
    if uid in lst: lst.remove(uid)
    else:          lst.append(uid)
    save_db(db)
    return jsonify({"likes": len(lst), "liked": uid in lst})

# ── Follow toggle ─────────────────────────────────────────────────
@app.route("/api/follow/<channel>", methods=["POST"])
def toggle_follow(channel):
    uid = request.json.get("uid", "anon")
    db  = load_db()
    lst = db["follows"].setdefault(channel, [])
    if uid in lst: lst.remove(uid)
    else:          lst.append(uid)
    save_db(db)
    return jsonify({"follows": len(lst), "following": uid in lst})

# ── View count ────────────────────────────────────────────────────
@app.route("/api/view/<vid_id>", methods=["POST"])
def add_view(vid_id):
    db = load_db()
    for v in db["videos"]:
        if v["id"] == vid_id:
            v["views"] = v.get("views", 0) + 1
    save_db(db)
    return jsonify({"ok": True})

if __name__ == "__main__":
    os.makedirs(os.path.join(UPLOAD_DIR, "videos"),     exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_DIR, "thumbnails"), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_DIR, "shorts"),     exist_ok=True)
    print("🎬 Local Tube running at http://localhost:3001")
    app.run(port=3001, debug=False)
