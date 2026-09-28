/* Layout audit for the deck. Injected by tools/run_audit.py; never shipped in index.html.
   For every slide (all fragments revealed, animations frozen) it reports:
   - out:     visible element extending beyond the 16:9 stage
   - spill:   text escaping the nearest boxed ancestor (card, note, button with bg/border)
   - overlap: text of two different elements intersecting; cursor: a cursor over text
   - covered: text painted under another element; boxes: boxed elements overlapping
     (opt out with data-overlap-ok); crowd: text within 0.35em of a foreign box;
     grid: left-aligned slide title not on the 7% column (opt out with data-align)
   Result is written as JSON into <pre id="__audit"> so `--dump-dom` can read it. */
(function () {
  function run() {
    var css = document.createElement("style");
    css.textContent = "*,*::before,*::after{transition:none!important;animation:none!important}";
    document.head.appendChild(css);

    var stage = document.querySelector(".stage");
    var slides = Array.prototype.slice.call(document.querySelectorAll("section.slide"));
    var S = stage.getBoundingClientRect();
    var em = parseFloat(getComputedStyle(stage).fontSize);
    var TOL = 1;
    var issues = [];

    function visible(el) {
      for (var n = el; n && n !== stage; n = n.parentElement) {
        var cs = getComputedStyle(n);
        if (cs.display === "none" || cs.visibility === "hidden" || parseFloat(cs.opacity) === 0) return false;
      }
      return true;
    }
    function label(el) {
      var t = (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 40);
      return el.tagName.toLowerCase() + (el.className && typeof el.className === "string" ? "." + el.className.split(" ").join(".") : "") + (t ? ' "' + t + '"' : "");
    }
    function boxed(el) {
      var cs = getComputedStyle(el);
      var bg = cs.backgroundColor, bw = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderLeftWidth);
      return (bg && bg !== "rgba(0, 0, 0, 0)" && bg !== "transparent") || bw > 0 || cs.backgroundImage !== "none";
    }
    function inter(a, b) {
      var w = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      var h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      return w > 2 && h > 2 ? w * h : 0;
    }
    function inflate(r, d) { return { left: r.left - d, top: r.top - d, right: r.right + d, bottom: r.bottom + d }; }

    slides.forEach(function (s, idx) {
      slides.forEach(function (o) { o.classList.remove("active"); o.style.display = "none"; });
      s.style.display = "";
      s.classList.add("active");
      Array.prototype.forEach.call(s.querySelectorAll(".frag"), function (f) { f.classList.add("on"); });
      void s.offsetHeight;
      var id = (idx + 1) + " " + (s.dataset.title || "");

      var els = Array.prototype.slice.call(s.querySelectorAll("*")).filter(function (el) {
        return !el.closest(".notas") && visible(el);
      });

      // out of stage
      els.forEach(function (el) {
        if (el.classList.contains("canvas")) return;
        var r = el.getBoundingClientRect();
        if (r.width < 1 || r.height < 1) return;
        if (r.left < S.left - TOL || r.right > S.right + TOL || r.top < S.top - TOL || r.bottom > S.bottom + TOL) {
          issues.push({ slide: id, type: "out", el: label(el), px: [Math.round(r.left - S.left), Math.round(r.top - S.top), Math.round(r.right - S.left), Math.round(r.bottom - S.top)], stage: [Math.round(S.width), Math.round(S.height)] });
        }
      });

      // text runs
      var runs = [];
      var walker = document.createTreeWalker(s, NodeFilter.SHOW_TEXT, null);
      var tn;
      while ((tn = walker.nextNode())) {
        if (!tn.nodeValue.trim()) continue;
        var el = tn.parentElement;
        if (el.closest(".notas") || !visible(el)) continue;
        var rg = document.createRange(); rg.selectNodeContents(tn);
        Array.prototype.forEach.call(rg.getClientRects(), function (r) {
          if (r.width > 1 && r.height > 1) runs.push({ el: el, r: r });
        });
      }

      // spill: text outside nearest boxed ancestor
      runs.forEach(function (t) {
        for (var n = t.el; n && n !== s; n = n.parentElement) {
          if (boxed(n) && !n.classList.contains("slide")) {
            var b = n.getBoundingClientRect();
            if (t.r.left < b.left - TOL || t.r.right > b.right + TOL || t.r.top < b.top - TOL || t.r.bottom > b.bottom + TOL) {
              issues.push({ slide: id, type: "spill", el: label(t.el), box: label(n) });
            }
            break;
          }
        }
      });

      // overlap between text of different elements
      for (var a = 0; a < runs.length; a++) {
        for (var b = a + 1; b < runs.length; b++) {
          var A = runs[a], B = runs[b];
          if (A.el === B.el || A.el.contains(B.el) || B.el.contains(A.el)) continue;
          if (inter(A.r, B.r) > 0) issues.push({ slide: id, type: "overlap", a: label(A.el), b: label(B.el) });
        }
      }

      // covered: text painted under another element (image, card, bar...). Sample 5 points per run.
      runs.forEach(function (t) {
        if (t.el.closest(".cur")) return;
        var r = t.r, pts = [[.5, .5], [.2, .3], [.8, .3], [.2, .7], [.8, .7]];
        for (var k = 0; k < pts.length; k++) {
          var x = r.left + r.width * pts[k][0], y = r.top + r.height * pts[k][1];
          var top = document.elementFromPoint(x, y);
          if (!top || top === t.el || t.el.contains(top) || top.contains(t.el) || top.closest(".cur")) continue;
          issues.push({ slide: id, type: "covered", text: label(t.el), by: label(top) });
          break;
        }
      });

      // boxes: two boxed elements (neither containing the other) overlapping, unless opted out
      var boxes = els.filter(function (el) {
        return boxed(el) && !el.classList.contains("canvas") && !el.closest(".cur") && !el.closest("[data-overlap-ok]") && el.getBoundingClientRect().width > 4;
      });
      for (var p = 0; p < boxes.length; p++) {
        for (var q = p + 1; q < boxes.length; q++) {
          var X = boxes[p], Y = boxes[q];
          if (X.contains(Y) || Y.contains(X)) continue;
          var rx = X.getBoundingClientRect(), ry = Y.getBoundingClientRect();
          var ar = inter(rx, ry), small = Math.min(rx.width * rx.height, ry.width * ry.height);
          if (ar > 0.01 * small) issues.push({ slide: id, type: "boxes", a: label(X), b: label(Y) });
        }
      }

      // crowd: text closer than 0.35em to a box it does not belong to
      runs.forEach(function (t) {
        if (t.el.closest(".cur")) return;
        boxes.forEach(function (bx) {
          if (bx.contains(t.el) || t.el.contains(bx) || bx.closest("[data-overlap-ok]")) return;
          var br = bx.getBoundingClientRect();
          if (inter(inflate(t.r, 0.35 * em), br) > 0 && inter(t.r, br) === 0) {
            issues.push({ slide: id, type: "crowd", text: label(t.el), box: label(bx) });
          }
        });
      });

      // grid: left-aligned slide titles must start at the 7% column
      var h = s.querySelector("h1, h2");
      if (h && visible(h) && !h.closest("[data-align]")) {
        var ta = getComputedStyle(h).textAlign, hr = h.getBoundingClientRect();
        var rng = document.createRange(); rng.selectNodeContents(h);
        var first = rng.getClientRects()[0];
        if (first && (ta === "left" || ta === "start")) {
          var rel = (first.left - S.left) / S.width;
          if (Math.abs(rel - 0.07) > 0.008) issues.push({ slide: id, type: "grid", el: label(h), leftPct: +(rel * 100).toFixed(1) });
        }
      }

      // cursors over text (inflated by idle-motion amplitude)
      Array.prototype.forEach.call(s.querySelectorAll(".cur"), function (c) {
        if (!visible(c)) return;
        var cr = inflate(c.getBoundingClientRect(), 0.6 * em);
        runs.forEach(function (t) {
          if (c.contains(t.el)) return;
          if (inter(cr, t.r) > 0) issues.push({ slide: id, type: "cursor", cursor: label(c), text: label(t.el) });
        });
      });
    });

    // de-duplicate
    var seen = {}, uniq = [];
    issues.forEach(function (i) { var k = JSON.stringify(i); if (!seen[k]) { seen[k] = 1; uniq.push(i); } });
    var pre = document.createElement("pre");
    pre.id = "__audit";
    pre.textContent = JSON.stringify({ viewport: [innerWidth, innerHeight], slides: slides.length, issues: uniq });
    document.body.appendChild(pre);
  }
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(function () { setTimeout(run, 300); });
})();
