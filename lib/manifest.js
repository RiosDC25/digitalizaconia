/* Datos de marca y configuración. Único sitio donde tocar valores. */
(function () {
  "use strict";

  window.__BRAND__ = {
    name: "DigitalizaConIA",
    shortName: "DCIA",
    email: "dani@digitalizaconia.com",
    owner: "Daniel Ordás Montorio",
    area: "Zaragoza · Huesca, España",

    /* Panel del hero. Son EJEMPLOS ilustrativos, no tareas reales de ningún
       cliente: la cabecera del panel lo dice. Se pueden editar libremente,
       pero conviene mantener cinco por tanda para que la tarjeta no cambie
       de alto al rotar. */
    taskDemo: {
      batches: [
        [
          "Responder a Marta por WhatsApp",
          "Apuntar el pedido en la hoja",
          "Confirmar la cita del jueves",
          "Avisar al equipo del stock bajo",
          "Preparar el resumen del día"
        ],
        [
          "Leer la factura del proveedor",
          "Pasar los datos al Excel",
          "Cotejar con el albarán",
          "Marcar la incidencia del pedido 4471",
          "Enviar el recordatorio de pago"
        ],
        [
          "Clasificar los 12 leads de la web",
          "Puntuar por probabilidad de cierre",
          "Agendar las 3 llamadas de mañana",
          "Actualizar la ficha del CRM",
          "Avisar a comercial de la oportunidad"
        ]
      ]
    },

    form: {
      /* ------------------------------------------------------------------
         DESTINO DEL FORMULARIO — pendiente de decidir.

         Mientras `endpoint` sea null, al enviar se abre el correo del
         visitante con todo relleno (el mismo comportamiento que la web
         anterior), así que ningún contacto se pierde.

         Para activar un backend, poner aquí la URL y nada más:
           endpoint: "https://<tu-n8n>/webhook/contacto"      // webhook n8n
           endpoint: "https://formspree.io/f/xxxxxxxx"        // Formspree
           endpoint: "https://api.web3forms.com/submit"       // Web3Forms

         El envío es POST con JSON. Si el servicio exige una clave en el
         cuerpo (Web3Forms pide `access_key`), añadirla en `extraFields`.
         ------------------------------------------------------------------ */
      endpoint: null,
      extraFields: {},

      subject: "Consulta desde digitalizaconia.com",
      okMessage: "Mensaje enviado. Te respondemos en menos de 24 h laborables.",
      errMessage:
        "No se ha podido enviar. Escríbenos directamente a dani@digitalizaconia.com.",
      mailtoMessage:
        "Se ha abierto tu programa de correo con el mensaje listo. Si no ocurre nada, escribe a dani@digitalizaconia.com."
    }
  };
})();
