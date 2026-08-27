#!/usr/bin/env python3
"""Genera las páginas interiores del sitio.

Sin build step en el entregable: esto es una herramienta de desarrollo que
escribe HTML plano. Existe para que cabecera, pie y <head> no se
desincronicen entre siete páginas mantenidas a mano.

    python3 tools/build-pages.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V = "20260827"
BASE = "https://digitalizaconia.com"
EMAIL = "dani@digitalizaconia.com"

NAV = [
    ("chatbots.html", "Chatbots"),
    ("automatizacion.html", "Automatización"),
    ("analisis-de-datos.html", "Datos"),
    ("metodo.html", "Método"),
]


def head(title, desc, slug):
    canon = f"{BASE}/" if slug == "index.html" else f"{BASE}/{slug}"
    return f"""<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.remove("no-js");</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FBFCFC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#070B0C" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{canon}">

<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="DigitalizaConIA">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/assets/img/og.png">

<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="styles.css?v={V}">
</head>
<body>

<a class="skip-link" href="#main">Saltar al contenido</a>

<div class="mesh" data-mesh aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
"""


def nav(slug):
    links = "".join(
        f'\n      <a href="{h}"{" class=\"is-active\"" if h == slug else ""}>{t}</a>'
        for h, t in NAV
    )
    mob = "".join(f'\n    <a href="{h}">{t}</a>' for h, t in NAV)
    return f"""
<header class="nav" data-nav>
  <div class="nav-inner">
    <a class="brand" href="index.html" aria-label="DigitalizaConIA — inicio">
      <img src="assets/img/logo-dcia.webp" alt="" width="256" height="256">
      <span class="brand-name">DigitalizaCon<span class="brand-accent">IA</span></span>
    </a>

    <nav class="nav-links" aria-label="Principal">{links}
    </nav>

    <a class="btn btn-sm btn-primary" href="index.html#contacto">Hablemos</a>

    <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="nav-mobile">
      <span class="sr-only">Abrir menú</span>
      <span class="nav-burger" aria-hidden="true"></span>
    </button>
  </div>

  <div class="nav-mobile" id="nav-mobile" data-nav-mobile hidden>{mob}
    <a href="index.html#contacto">Contacto</a>
  </div>
</header>
"""


FOOT = f"""
<footer class="footer">
  <div class="wrap footer-inner">
    <div class="footer-brand">
      <img src="assets/img/logo-dcia.webp" alt="" width="256" height="256" loading="lazy">
      <span>DigitalizaCon<span class="brand-accent">IA</span></span>
    </div>
    <nav class="footer-links" aria-label="Pie de página">
      <a href="index.html">Inicio</a>
      <a href="metodo.html">Método</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="aviso-legal.html">Aviso legal</a>
      <a href="privacidad.html">Privacidad</a>
    </nav>
    <p class="footer-copy">© 2026 DigitalizaConIA · Zaragoza &amp; Huesca</p>
  </div>
</footer>

<script defer src="lib/manifest.js?v={V}"></script>
<script defer src="main.js?v={V}"></script>
</body>
</html>
"""


def cta(texto):
    return f"""
<section class="section cta-band">
  <div class="wrap">
    <div class="cta-box">
      <div>
        <h2 class="cta-title">{texto}</h2>
        <p class="cta-sub">Diagnóstico gratuito, sin permanencia y con una respuesta clara: si no sale la cuenta, te lo decimos.</p>
      </div>
      <a class="btn btn-primary" href="index.html#contacto">Háblanos de tu negocio</a>
    </div>
  </div>
</section>
"""


def service_page(slug, kicker, h1, lede, incluye, casos, entrada, faq_extra):
    lis = "".join(f"\n        <li><strong>{t}</strong>{d}</li>" for t, d in incluye)
    cs = "".join(
        f"""
      <li class="case">
        <span class="case-num">{i:02d}</span>
        <p>{c}</p>
      </li>"""
        for i, c in enumerate(casos, 1)
    )
    faqs = "".join(
        f"""
      <details class="qa">
        <summary><span>{q}</span><span class="row-icon" aria-hidden="true"></span></summary>
        <div class="qa-body"><p>{a}</p></div>
      </details>"""
        for q, a in faq_extra
    )
    return f"""{head(h1 + " | DigitalizaConIA", lede[:155], slug)}{nav(slug)}
<main id="main">

<section class="page-hero">
  <div class="wrap wrap-narrow">
    <p class="kicker reveal">{kicker}</p>
    <h1 class="page-title reveal">{h1}</h1>
    <p class="page-lede reveal">{lede}</p>
    <div class="hero-actions reveal">
      <a class="btn btn-primary" href="index.html#contacto">Pedir diagnóstico</a>
      <a class="btn btn-ghost" href="metodo.html">Cómo trabajamos</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap-narrow">
    <header class="section-head">
      <p class="kicker reveal">Qué incluye</p>
      <h2 class="section-title reveal">Lo que te llevas</h2>
    </header>
    <div class="panel reveal">
      <ul class="feature-list">{lis}
      </ul>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap wrap-narrow">
    <header class="section-head">
      <p class="kicker reveal">Ejemplos</p>
      <h2 class="section-title reveal">Cómo se usa esto en la práctica</h2>
      <p class="section-sub reveal">Situaciones habituales en pymes. Son ejemplos ilustrativos, no clientes concretos.</p>
    </header>
    <ul class="cases">{cs}
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap wrap-narrow">
    <header class="section-head">
      <p class="kicker reveal">Plazo y coste</p>
      <h2 class="section-title reveal">Qué esperar</h2>
    </header>
    <div class="panel reveal">
      <dl class="spec">
        <dt>Punto de entrada</dt><dd>{entrada}</dd>
        <dt>Plazo del MVP</dt><dd>2–4 semanas, según alcance.</dd>
        <dt>Permanencia</dt><dd>Ninguna. Se trabaja proyecto a proyecto.</dd>
        <dt>Propiedad</dt><dd>El código y las configuraciones específicas del proyecto son tuyos.</dd>
      </dl>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap wrap-narrow">
    <header class="section-head">
      <p class="kicker reveal">Dudas frecuentes</p>
      <h2 class="section-title reveal">Sobre este servicio</h2>
    </header>
    <div class="faq">{faqs}
    </div>
  </div>
</section>
{cta("¿Te encaja para tu negocio?")}
</main>
{FOOT}"""


# ─────────────────────────────────────────────────────────── páginas

PAGES = {}

PAGES["chatbots.html"] = service_page(
    "chatbots.html",
    "Servicio 01 · Chatbots y asistentes",
    "Atención al cliente que no cierra a las ocho",
    "Un asistente que responde por WhatsApp e Instagram, cualifica a quien escribe "
    "y agenda solo. Las personas del equipo entran cuando de verdad hacen falta, "
    "no para copiar un teléfono en una hoja.",
    [
        ("Disponibilidad 24/7. ", "Responde fuera de horario, en fin de semana y en agosto."),
        ("Integración con WhatsApp e Instagram. ", "Donde ya te escriben tus clientes, sin pedirles que cambien de canal."),
        ("Cualificación de leads. ", "Distingue quien pregunta el horario de quien quiere presupuesto, y lo marca."),
        ("Agendamiento automático. ", "Conecta con tu calendario y cierra la cita dentro de la conversación."),
        ("Traspaso a humano. ", "Cuando la conversación se sale del guion, avisa a una persona con el contexto ya resumido."),
    ],
    [
        "Una clínica recibe veinte mensajes al día preguntando horarios y precios. El asistente responde al momento y solo pasa a recepción las peticiones de cita complicadas.",
        "Un restaurante deja de perder reservas de las once de la noche: el bot confirma mesa contra el calendario y manda el recordatorio la víspera.",
        "Una tienda cualifica por Instagram: quien pide catálogo lo recibe solo, y quien pide presupuesto llega a comercial con los datos ya recogidos.",
    ],
    "Desde 200 € para un asistente acotado a un canal y un puñado de intenciones.",
    [
        ("¿Se nota que es un bot?",
         "Sí, y así debe ser. Se presenta como asistente desde el primer mensaje. Fingir que es una persona genera desconfianza en cuanto falla una respuesta, y además el RGPD y las buenas prácticas piden transparencia."),
        ("¿Qué pasa si no sabe responder?",
         "Deriva a una persona con el hilo resumido. Un asistente que se inventa la respuesta hace más daño que uno que dice «esto te lo contesta un compañero»."),
        ("¿Necesito WhatsApp Business API?",
         "Para volumen y automatización seria, sí. Se valora en el diagnóstico: a veces con la app de empresa y una integración más sencilla es suficiente para empezar."),
    ],
)

PAGES["automatizacion.html"] = service_page(
    "automatizacion.html",
    "Servicio 02 · Automatización de procesos",
    "Las tareas que se repiten cada semana",
    "Copiar datos de un sitio a otro, cotejar documentos, mandar recordatorios. "
    "Trabajo que consume horas, no requiere criterio y se equivoca cuando alguien "
    "va con prisa. Eso es lo que se automatiza primero.",
    [
        ("Menos horas en tareas repetitivas. ", "El tiempo se va a lo que sí necesita una persona delante."),
        ("Procesos estandarizados. ", "El mismo paso se hace igual siempre, lo haga quien lo haga."),
        ("Aplicaciones interconectadas. ", "Sheets, calendario, correo, CRM y mensajería dejan de ser islas."),
        ("Menos errores de transcripción. ", "El dato entra una vez y viaja solo al resto de sitios."),
        ("Registro de lo ocurrido. ", "Cada ejecución queda trazada, así que se puede auditar y corregir."),
    ],
    [
        "Llega la factura de un proveedor por correo: se lee, se extraen los importes, se cotejan con el albarán y se anota la discrepancia si la hay.",
        "Un pedido entra por formulario y termina, sin intervención, en la hoja de producción, el calendario de reparto y un aviso al almacén.",
        "Cada lunes se genera y se envía el resumen de la semana anterior a quien lo necesita, con los números ya calculados.",
    ],
    "Desde 200 € para una automatización simple entre dos herramientas.",
    [
        ("¿Qué herramientas usáis?",
         "n8n o Make para orquestar, y las APIs de lo que ya tengas. Se prioriza que puedas mantenerlo tú o cambiar de proveedor sin rehacerlo todo."),
        ("¿Y si el proceso cambia dentro de seis meses?",
         "Se entrega documentado y con la lógica separada de las credenciales, de modo que ajustar un paso no obligue a reconstruir el flujo."),
        ("¿Puede romperse y no enterarme?",
         "Por eso cada flujo lleva aviso de fallo. Si una ejecución se cae, salta una notificación en vez de acumularse el problema en silencio."),
    ],
)

PAGES["analisis-de-datos.html"] = service_page(
    "analisis-de-datos.html",
    "Servicio 03 · Análisis de datos",
    "Decidir con antelación, no a toro pasado",
    "Tus propios datos, puestos a trabajar: cuánta demanda viene, qué cliente tiene "
    "pinta de cerrar y qué se está saliendo de lo normal ahora mismo. Sin cuadros de "
    "mando que nadie abre.",
    [
        ("Dashboards personalizados. ", "Las cuatro cifras que de verdad miras, no cuarenta que no."),
        ("Predicción de demanda. ", "Estimación a semanas vista con su margen de error, no un número suelto."),
        ("Scoring automático. ", "Cada lead o pedido con una probabilidad, para priorizar por dónde empezar."),
        ("Alertas en tiempo real. ", "Avisa cuando algo se sale del rango; no hay que ir a mirar."),
        ("Datos en Europa. ", "Neon o Supabase con alojamiento europeo cuando el caso lo permite."),
    ],
    [
        "Un negocio estacional estima la demanda de las próximas tres semanas y ajusta compras y turnos con margen.",
        "Los leads que entran por la web se puntúan solos y comercial ataca primero los que tienen más probabilidad de cerrar.",
        "Salta un aviso cuando el consumo de un material se desvía de lo previsto, antes de que se convierta en rotura de stock.",
    ],
    "Depende del estado de tus datos. El diagnóstico dice si hay suficiente historial para que un modelo aporte algo.",
    [
        ("¿Cuántos datos hacen falta?",
         "Menos de los que la gente cree para tendencias simples, y bastantes más para predicción fina. La primera respuesta honesta del diagnóstico puede ser «todavía no; primero hay que registrar esto durante unos meses»."),
        ("¿Y si mis datos están en hojas de cálculo hechas un desastre?",
         "Es el punto de partida habitual. Limpiar y estructurar forma parte del trabajo, y a menudo es donde aparece el primer valor, antes incluso de predecir nada."),
        ("¿Me vais a vender un modelo que no necesito?",
         "Buena parte de los casos se resuelven con un buen panel y un par de alertas. Si no hace falta machine learning, no se mete."),
    ],
)

# ─────────────────────────────────────────────────── método (página propia)

PASOS = [
    ("1", "Diagnóstico", "Miramos objetivos, datos y contexto reales, no un cuestionario genérico. Sale de aquí una lista de candidatos a automatizar ordenada por lo que te ahorra frente a lo que cuesta. Gratuito en la mayoría de los casos."),
    ("2", "MVP funcional", "Se construye la versión más pequeña que demuestra el valor, en dos a cuatro semanas. Acotada a propósito: es más barato descubrir que algo no funciona en la semana tres que en el mes seis."),
    ("3", "Medición", "Se acuerdan las métricas antes de empezar, y se itera contra ellas. Si el número no se mueve, se dice y se cambia de enfoque."),
    ("4", "Escalado y soporte", "Seguridad, documentación y formación, para que el sistema no dependa de que nosotros sigamos aquí."),
]

pasos_html = "".join(
    f"""
      <li class="step reveal">
        <span class="step-num">{n}</span>
        <h3 class="step-title">{t}</h3>
        <p>{d}</p>
      </li>"""
    for n, t, d in PASOS
)

STACK = [
    ("OpenAI / Anthropic", "LLMs"), ("Google Sheets", "datos"),
    ("cal.com", "calendarios"), ("n8n / Make", "automatización"),
    ("WhatsApp / Instagram", "mensajería"), ("Neon / Supabase", "bases de datos EU"),
]
stack_html = "".join(
    f'\n          <li><span class="stack-name">{n}</span><span class="stack-role">{r}</span></li>'
    for n, r in STACK
)

PRIV = [
    ("Minimización de datos", "Solo procesamos lo necesario."),
    ("Alojamiento EU", "Servidores en Europa cuando es posible."),
    ("Auditoría RGPD", "Documentación completa de tratamiento."),
    ("NDA disponible", "Protección de propiedad intelectual."),
]
priv_html = "".join(f"\n          <dt>{t}</dt>\n          <dd>{d}</dd>" for t, d in PRIV)

FAQ_GEN = [
    ("¿Plazos típicos?", "Normalmente se consideran 2–4 semanas para implantar un MVP; no obstante, cada proyecto es único y necesita ser estudiado de forma individual."),
    ("¿Quién es propietario de los entregables?", "El cliente es propietario del código y configuraciones específicas del proyecto. Las plantillas y librerías base forman parte de nuestro stack y se licencian para su uso en el proyecto."),
    ("¿Coste orientativo?", "Desde 200 € (tareas puntuales o automatizaciones simples) hasta 20.000 €+ (proyectos a medida con ML e integraciones complejas). Se define tras el diagnóstico."),
    ("¿El diagnóstico tiene coste?", "La evaluación inicial y la propuesta son gratuitas en la mayoría de los casos. Auditorías avanzadas pueden presupuestarse aparte, siempre previo acuerdo."),
]
faq_html = "".join(
    f"""
      <details class="qa"{' open' if i == 0 else ''}>
        <summary><span>{q}</span><span class="row-icon" aria-hidden="true"></span></summary>
        <div class="qa-body"><p>{a}</p></div>
      </details>"""
    for i, (q, a) in enumerate(FAQ_GEN)
)

faq_ld = ",\n    ".join(
    '{ "@type": "Question", "name": "%s", "acceptedAnswer": { "@type": "Answer", "text": "%s" } }'
    % (q, a) for q, a in FAQ_GEN
)

PAGES["metodo.html"] = f"""{head("Método, tecnología y RGPD | DigitalizaConIA",
    "Cómo trabajamos: diagnóstico, MVP en 2–4 semanas, medición y escalado. Stack técnico y cumplimiento RGPD.",
    "metodo.html")}<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {faq_ld}
  ]
}}
</script>
{nav("metodo.html")}
<main id="main">

<section class="page-hero">
  <div class="wrap wrap-narrow">
    <p class="kicker reveal">Cómo trabajamos</p>
    <h1 class="page-title reveal">Sin permanencias.<br>Entregables claros.</h1>
    <p class="page-lede reveal">Cuatro pasos, y en cada uno sabes qué recibes y cuándo.
      El objetivo del primero es decidir si merece la pena el segundo.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <ol class="steps">{pasos_html}
    </ol>
  </div>
</section>

<section class="section section-alt" id="tech">
  <div class="wrap">
    <header class="section-head">
      <p class="kicker reveal">Tech &amp; RGPD</p>
      <h2 class="section-title reveal">Tecnología actual,<br>normativa europea.</h2>
    </header>

    <figure class="flow reveal">
      <figcaption class="flow-cap">Anatomía de una automatización típica</figcaption>
      <svg class="flow-svg" viewBox="0 0 1000 190" role="img"
           aria-label="Diagrama de flujo: un mensaje entra por WhatsApp o Instagram, pasa por n8n o Make, se procesa con un modelo de lenguaje y termina registrado en Google Sheets o en una base de datos europea y agendado en cal.com.">
        <defs>
          <linearGradient id="flowStroke" gradientUnits="userSpaceOnUse" x1="92" y1="0" x2="908" y2="0">
            <stop offset="0%" stop-color="#0A5A78"/>
            <stop offset="50%" stop-color="#12806E"/>
            <stop offset="100%" stop-color="#3E9B45"/>
          </linearGradient>
        </defs>
        <path class="flow-line" d="M 92 95 H 908" stroke="url(#flowStroke)" fill="none" stroke-width="1.5"/>
        <path class="flow-pulse" d="M 92 95 H 908" stroke="currentColor" fill="none" stroke-width="2"
              stroke-dasharray="8 992" stroke-linecap="round"/>
        <g class="flow-node" transform="translate(92,95)"><circle r="7"/><text y="-26">Entrada</text><text class="flow-sub" y="34">WhatsApp · Instagram</text></g>
        <g class="flow-node" transform="translate(296,95)"><circle r="7"/><text y="-26">Orquestación</text><text class="flow-sub" y="34">n8n · Make</text></g>
        <g class="flow-node" transform="translate(500,95)"><circle r="7"/><text y="-26">Razonamiento</text><text class="flow-sub" y="34">OpenAI · Anthropic</text></g>
        <g class="flow-node" transform="translate(704,95)"><circle r="7"/><text y="-26">Registro</text><text class="flow-sub" y="34">Sheets · Neon · Supabase</text></g>
        <g class="flow-node flow-node-end" transform="translate(908,95)"><circle r="7"/><text y="-26">Acción</text><text class="flow-sub" y="34">cal.com · aviso al equipo</text></g>
      </svg>
    </figure>

    <div class="tech-grid">
      <div class="tech-stack reveal">
        <h3 class="minor-title">Stack</h3>
        <ul class="stack-list">{stack_html}
        </ul>
      </div>
      <div class="tech-privacy reveal">
        <h3 class="minor-title">Privacidad y cumplimiento</h3>
        <dl class="privacy-list">{priv_html}
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap wrap-narrow">
    <header class="section-head">
      <p class="kicker reveal">Preguntas frecuentes</p>
      <h2 class="section-title reveal">Lo que suelen preguntarnos</h2>
    </header>
    <div class="faq">{faq_html}
    </div>
  </div>
</section>
{cta("Empecemos por el diagnóstico")}
</main>
{FOOT}"""


for name, html in PAGES.items():
    (ROOT / name).write_text(html, encoding="utf-8")
    print(f"  ✓ {name:26} {len(html) / 1024:5.1f} KB")
