html = open('/home/uno/snapchat-viewer/templates/index.html', 'w')
html.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Snap Viewer</title>
<style>
body{background:#111;color:white;font-family:sans-serif;text-align:center;padding:20px}
input{padding:10px;width:300px;border-radius:20px;border:none;font-size:16px}
button{padding:10px 20px;background:#FFFC00;color:black;border:none;border-radius:20px;font-size:16px;cursor:pointer;margin-left:10px}
#stories{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:15px;max-width:1200px;margin:20px auto}
.snap{background:#222;border-radius:12px;overflow:hidden}
.snap video,.snap img{width:100%;height:300px;object-fit:cover;display:block}
.dl{display:block;background:#FFFC00;color:black;padding:8px;text-decoration:none;font-weight:bold}
</style>
</head>
<body>
<h1>Snap Viewer</h1>
<input type="text" id="un" placeholder="Enter username">
<button id="btn">View Stories</button>
<div id="stories"></div>
<script>
document.getElementById("btn").addEventListener("click", async function() {
  var u = document.getElementById("un").value;
  if (!u) { alert("Enter username"); return; }
  var d = document.getElementById("stories");
  d.innerHTML = "Loading...";
  var r = await fetch("/api/stories/" + u);
  var j = await r.json();
  d.innerHTML = "";
  var s = j.props.pageProps.curatedHighlights[0].snapList;
  s.forEach(function(snap) {
    var url = snap.snapUrls ? snap.snapUrls.value : null;
    if (!url) return;
    var div = document.createElement("div");
    div.className = "snap";
    if (snap.snapMediaType === 1) {
      var v = document.createElement("video");
      v.src = url; v.controls = true; div.appendChild(v);
    } else {
      var i = document.createElement("img");
      i.src = "/proxy?url=" + encodeURIComponent(url);
      div.appendChild(i);
    }
    var a = document.createElement("a");
    a.href = "/download?url=" + encodeURIComponent(url);
    a.className = "dl"; a.textContent = "Download";
    div.appendChild(a);
    d.appendChild(div);
  });
});
</script>
</body>
</html>""")
html.close()
print("Done!")
