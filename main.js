(function () {
  "use strict";
  /* DigitalizaConIA — comportamiento del sitio.
     Script clásico, IIFE, sin módulos. El HTML se lee entero sin esto;
     aquí solo se enriquece. */

  var data = window.__BRAND__ || {};
  var FORM = data.form || {};

  var $ = function (sel, scope) { return (scope || document).querySelector(sel); };
  var $$ = function (sel, scope) {
    return Array.prototype.slice.call((scope || document).querySelectorAll(sel));
  };
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fineHover = matchMedia("(hover: hover) and (pointer: fine)").matches;

  var escHTML = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };

  function safe(fn, name) {
    try { fn(); } catch (e) { console.warn("[" + name + "]", e); }
  }

  /* ---------------------------------------------------------------
     Mesh reactivo al cursor — el efecto firma.
     Un único bucle rAF para todo el sitio (nada de un rAF por módulo).
     --------------------------------------------------------------- */
  function initMesh() {
    var mesh = $("[data-mesh]");
    if (!mesh) return;

    var root = document.documentElement;
    var tx = 50, ty = 22, cx = 50, cy = 22;
    var running = false;

    function tick() {
      cx += (tx - cx) * 0.06;
      cy += (ty - cy) * 0.06;
      root.style.setProperty("--mx", cx.toFixed(2) + "%");
      root.style.setProperty("--my", cy.toFixed(2) + "%");
      if (Math.abs(tx - cx) > 0.05 || Math.abs(ty - cy) > 0.05) {
        requestAnimationFrame(tick);
      } else {
        running = false;
      }
    }
    function wake() {
      if (!running) { running = true; requestAnimationFrame(tick); }
    }

    if (fineHover) {
      window.addEventListener("mousemove", function (e) {
        tx = (e.clientX / window.innerWidth) * 100;
        ty = (e.clientY / window.innerHeight) * 100;
        wake();
      }, { passive: true });
    }

    // Táctil: sin cursor, el gradiente se mueve con el scroll para que la
    // página no se sienta muerta en móvil.
    window.addEventListener("scroll", function () {
      if (fineHover) return;
      var max = document.body.scrollHeight - window.innerHeight;
      var p = max > 0 ? window.scrollY / max : 0;
      tx = 34 + p * 34;
      ty = 18 + p * 46;
      wake();
    }, { passive: true });

    wake();
  }

  /* ---------------------------------------------------------------
     Navegación: fondo al hacer scroll, menú móvil, enlace activo
     --------------------------------------------------------------- */
  function initNav() {
    var nav = $("[data-nav]");
    if (!nav) return;

    function onScroll() {
      nav.classList.toggle("is-stuck", window.scrollY > 24);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    var toggle = $("[data-nav-toggle]");
    var panel = $("[data-nav-mobile]");
    if (toggle && panel) {
      toggle.addEventListener("click", function () {
        var open = toggle.getAttribute("aria-expanded") === "true";
        toggle.setAttribute("aria-expanded", String(!open));
        panel.hidden = open;
        toggle.querySelector(".sr-only").textContent = open ? "Abrir menú" : "Cerrar menú";
      });
      $$("a", panel).forEach(function (a) {
        a.addEventListener("click", function () {
          toggle.setAttribute("aria-expanded", "false");
          panel.hidden = true;
        });
      });
      addEventListener("keydown", function (e) {
        if (e.key === "Escape" && !panel.hidden) { toggle.click(); toggle.focus(); }
      });
    }
  }

  function initScrollSpy() {
    var links = $$(".nav-links a[href^='#']");
    if (!links.length || !("IntersectionObserver" in window)) return;

    var map = {};
    var targets = [];
    links.forEach(function (a) {
      var el = document.getElementById(a.getAttribute("href").slice(1));
      if (el) { map[el.id] = a; targets.push(el); }
    });

    // Se lleva la cuenta de lo visible: si no hay ninguna sección en la banda
    // central (por ejemplo en el hero), no debe quedarse ningún enlace marcado.
    var visible = [];

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var i = visible.indexOf(en.target.id);
        if (en.isIntersecting && i === -1) visible.push(en.target.id);
        if (!en.isIntersecting && i !== -1) visible.splice(i, 1);
      });

      var current = visible.length ? visible[visible.length - 1] : null;
      links.forEach(function (l) { l.classList.remove("is-active"); });
      if (current && map[current]) map[current].classList.add("is-active");
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });

    targets.forEach(function (t) { spy.observe(t); });
  }

  /* ---------------------------------------------------------------
     Reveals al entrar en pantalla.
     Umbral bajo + red de seguridad: pasados 6 s nada sigue oculto.
     --------------------------------------------------------------- */
  function initReveals() {
    var items = $$(".reveal");
    if (!items.length) return;

    function showAll() { items.forEach(function (el) { el.classList.add("is-in"); }); }

    if (!("IntersectionObserver" in window)) { showAll(); return; }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("is-in");
        io.unobserve(en.target);
      });
    }, { threshold: 0.04, rootMargin: "0px 0px -6% 0px" });

    items.forEach(function (el, i) {
      // escalonado corto dentro de cada bloque, sin retrasos largos
      el.style.transitionDelay = (i % 4) * 60 + "ms";
      io.observe(el);
    });

    setTimeout(showAll, 6000);
  }

  /* ---------------------------------------------------------------
     Contadores
     --------------------------------------------------------------- */
  function initCounters() {
    var nums = $$("[data-count-to]");
    if (!nums.length) return;

    function run(el) {
      var to = parseFloat(el.getAttribute("data-count-to"));
      if (isNaN(to)) return;
      if (reduced || to === 0) { el.textContent = String(to); return; }

      var dur = 1100, t0 = performance.now();
      (function step(now) {
        var p = Math.min(1, (now - t0) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = String(Math.round(to * eased));
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    }

    if (!("IntersectionObserver" in window)) { nums.forEach(run); return; }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        run(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.05 });

    nums.forEach(function (el) { io.observe(el); });
  }

  /* ---------------------------------------------------------------
     Formulario: validación + envío.
     Sin endpoint configurado cae en mailto, igual que la web anterior.
     --------------------------------------------------------------- */
  function initForm() {
    var form = $("[data-form]");
    if (!form) return;

    var status = $("[data-form-status]", form);
    var button = $(".btn-submit", form);
    var label = $("[data-submit-label]", form);
    var originalLabel = label ? label.textContent : "Enviar";

    var RULES = {
      nombre: function (v) { return v.trim().length >= 2 || "Dinos cómo te llamas."; },
      email: function (v) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || "Revisa el email.";
      },
      telefono: function (v) {
        if (!v.trim()) return true;
        return /^[+\d][\d\s().-]{6,}$/.test(v.trim()) || "Revisa el teléfono.";
      },
      web: function (v) {
        if (!v.trim()) return true;
        return /^https?:\/\/.+\..+/.test(v.trim()) || "La web debe empezar por https://";
      },
      mensaje: function (v) { return v.trim().length >= 10 || "Cuéntanos un poco más."; },
      consentimiento: function (_v, el) {
        return el.checked || "Necesitamos tu consentimiento para responderte.";
      }
    };

    function fieldOf(el) { return el.closest(".field"); }

    function setError(name, msg) {
      var slot = $("[data-error-for='" + name + "']", form);
      var input = form.elements[name];
      if (slot) slot.textContent = msg || "";
      if (input && fieldOf(input)) fieldOf(input).classList.toggle("has-error", !!msg);
    }

    function validate(name) {
      var input = form.elements[name];
      if (!input || !RULES[name]) return true;
      var res = RULES[name](input.value || "", input);
      setError(name, res === true ? "" : res);
      return res === true;
    }

    Object.keys(RULES).forEach(function (name) {
      var input = form.elements[name];
      if (!input) return;
      input.addEventListener("blur", function () { validate(name); });
      input.addEventListener("input", function () {
        if (fieldOf(input) && fieldOf(input).classList.contains("has-error")) validate(name);
      });
    });

    function values() {
      var out = {};
      Object.keys(RULES).forEach(function (name) {
        var el = form.elements[name];
        if (!el) return;
        out[name] = el.type === "checkbox" ? el.checked : el.value.trim();
      });
      return out;
    }

    function say(msg, kind) {
      if (!status) return;
      status.textContent = msg;
      status.className = "form-status" + (kind ? " is-" + kind : "");
    }

    function busy(on) {
      if (button) button.disabled = on;
      if (label) label.textContent = on ? "Enviando…" : originalLabel;
    }

    function mailtoFallback(v) {
      var body = [
        "Nombre: " + v.nombre,
        "Email: " + v.email,
        "Teléfono: " + (v.telefono || "—"),
        "Web: " + (v.web || "—"),
        "",
        v.mensaje
      ].join("\n");
      var href =
        "mailto:" + (data.email || "") +
        "?subject=" + encodeURIComponent(FORM.subject || "Consulta") +
        "&body=" + encodeURIComponent(body);
      window.location.href = href;
      say(FORM.mailtoMessage || "Se ha abierto tu programa de correo.", "ok");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var ok = Object.keys(RULES).map(validate).every(Boolean);
      if (!ok) {
        say("Revisa los campos marcados.", "err");
        var bad = $(".field.has-error input, .field.has-error textarea", form);
        if (bad) bad.focus();
        return;
      }

      var v = values();
      say("", "");

      // Sin backend configurado todavía: se abre el correo del visitante.
      if (!FORM.endpoint) { mailtoFallback(v); return; }

      busy(true);
      var payload = {};
      Object.keys(FORM.extraFields || {}).forEach(function (k) {
        payload[k] = FORM.extraFields[k];
      });
      Object.keys(v).forEach(function (k) { payload[k] = v[k]; });
      payload.origen = location.href;

      fetch(FORM.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          form.reset();
          say(FORM.okMessage || "Mensaje enviado.", "ok");
        })
        .catch(function (err) {
          console.warn("[form]", err);
          say(FORM.errMessage || "No se ha podido enviar.", "err");
        })
        .then(function () { busy(false); });
    });
  }

  /* ---------------------------------------------------------------
     Panel del hero: tareas que se completan solas.
     Es un EJEMPLO y así se dice en la cabecera; el contador solo cuenta
     las tareas de la propia demo, no un total real de DCIA.
     --------------------------------------------------------------- */
  function initTaskPanel() {
    var panel = $("[data-taskpanel]");
    if (!panel) return;

    var list = $("[data-tp-list]", panel);
    var countEl = $("[data-tp-count]", panel);
    var batches = (data.taskDemo && data.taskDemo.batches) || [];
    if (!list || !batches.length) return;

    function render(tasks, finished) {
      list.innerHTML = tasks.map(function (t) {
        return '<li class="tp-item' + (finished ? " is-done" : "") + '">' +
                 '<span class="tp-state" aria-hidden="true"></span>' +
                 '<span class="tp-text">' + escHTML(t) + "</span>" +
                 '<span class="tp-time">' + (finished ? "hecho" : "") + "</span>" +
               "</li>";
      }).join("");
    }

    // Con reduced-motion no hay bucle: se enseña el resultado y se queda quieto.
    if (reduced) {
      render(batches[0], true);
      if (countEl) countEl.textContent = String(batches[0].length);
      return;
    }

    var doneTotal = 0;
    var batchIndex = 0;
    var timer = null;

    function wait(ms, fn) { timer = setTimeout(fn, ms); }

    function runBatch() {
      var tasks = batches[batchIndex % batches.length];
      render(tasks, false);
      var items = $$(".tp-item", list);
      var i = 0;

      function nextItem() {
        if (i >= items.length) {
          // tanda terminada: pausa para que se lea, y entra la siguiente
          wait(2000, function () {
            list.classList.add("is-swapping");
            wait(400, function () {
              list.classList.remove("is-swapping");
              batchIndex++;
              runBatch();
            });
          });
          return;
        }

        var el = items[i];
        // duración irregular: si todas tardan lo mismo parece un metrónomo
        var runMs = 700 + Math.round(Math.random() * 900);
        el.classList.add("is-running");

        wait(runMs, function () {
          el.classList.remove("is-running");
          el.classList.add("is-done");
          var t = $(".tp-time", el);
          if (t) {
            t.textContent = "hecho · " + (runMs / 1000).toFixed(1).replace(".", ",") + " s";
          }
          doneTotal++;
          if (countEl) countEl.textContent = String(doneTotal);
          i++;
          wait(240, nextItem);
        });
      }

      nextItem();
    }

    // En segundo plano no corre: si no, al volver a la pestaña el contador
    // habría subido solo y se ve raro.
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) {
        clearTimeout(timer);
      } else {
        clearTimeout(timer);
        runBatch();
      }
    });

    runBatch();
  }

  /* --------------------------------------------------------------- */
  function boot() {
    document.documentElement.classList.remove("no-js");

    safe(initMesh, "initMesh");
    safe(initNav, "initNav");
    safe(initScrollSpy, "initScrollSpy");
    safe(initReveals, "initReveals");
    safe(initCounters, "initCounters");
    safe(initTaskPanel, "initTaskPanel");
    safe(initForm, "initForm");

    document.documentElement.classList.add("is-ready");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
