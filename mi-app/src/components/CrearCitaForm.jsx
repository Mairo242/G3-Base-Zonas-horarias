import React, { useState, useEffect } from "react";

const CrearCitaForm = () => {
  // -----------------------------
  // Estado de calendarios y formulario
  // -----------------------------
  const [calendarios, setCalendarios] = useState([]);
  const [formData, setFormData] = useState({
    calendarId: "",
    contactId: "",
    startTime: "",
    endTime: "",
    title: ""
  });

  // -----------------------------
  // Cargar calendarios al iniciar el componente
  // -----------------------------
  useEffect(() => {
    fetch("http://127.0.0.1:8000/app/calendars/")
      .then((res) => res.json())
      .then((data) => setCalendarios(data))
      .catch((err) => console.error("Error al cargar calendarios:", err));
  }, []);

  // -----------------------------
  // Manejo de cambios en inputs
  // -----------------------------
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // -----------------------------
  // Manejo de selección de calendario
  // -----------------------------
  const handleCalendarChange = (e) => {
    setFormData({ ...formData, calendarId: e.target.value });
  };

  // -----------------------------
  // Convertir a UTC
  // -----------------------------
  const toUTCISOString = (localDateTimeStr) => {
    // localDateTimeStr: "YYYY-MM-DDTHH:MM"
    if (!localDateTimeStr) return "";
    const localDate = new Date(localDateTimeStr);
    return localDate.toISOString();
  };

  // -----------------------------
  // Envío del formulario
  // -----------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Payload para la API, siempre usando locationId fijo
      const payload = {
        ...formData,
        locationId: "r3UrTfNuQviYjKT9vfVz",
        startTime: toUTCISOString(formData.startTime),
        endTime: toUTCISOString(formData.endTime)
      };

      const res = await fetch("http://127.0.0.1:8000/app/appointments/create/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Error al crear cita");

      alert("✅ Cita creada correctamente");
      console.log("Respuesta API:", data);
    } catch (err) {
      console.error(err);
      alert("❌ Error al crear cita: " + err.message);
    }
  };

  // -----------------------------
  // Render del formulario
  // -----------------------------
  return (
    <div>
      <h2>📝 Crear Cita</h2>
      <form onSubmit={handleSubmit}>
        {/* Selección de calendario */}
        <div>
          <label>Calendario:</label>
          <select
            name="calendarId"
            value={formData.calendarId}
            onChange={handleCalendarChange}
            required
          >
            <option value="">-- Selecciona un calendario --</option>
            {calendarios.map((cal) => (
              <option key={cal.id} value={cal.id}>
                {cal.name}
              </option>
            ))}
          </select>
        </div>

        {/* ID del contacto */}
        <div>
          <label>ID Contacto:</label>
          <input
            type="text"
            name="contactId"
            value={formData.contactId}
            onChange={handleChange}
            required
          />
        </div>

        {/* Título de la cita */}
        <div>
          <label>Título:</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>

        {/* Inicio de la cita */}
        <div>
          <label>Inicio:</label>
          <input
            type="datetime-local"
            name="startTime"
            value={formData.startTime}
            onChange={handleChange}
            required
          />
          {formData.startTime && (
            <p>
              UTC: {toUTCISOString(formData.startTime)} | 
              Perú: {new Date(formData.startTime).toLocaleString("es-PE")}
            </p>
          )}
        </div>

        {/* Fin de la cita */}
        <div>
          <label>Fin:</label>
          <input
            type="datetime-local"
            name="endTime"
            value={formData.endTime}
            onChange={handleChange}
            required
          />
          {formData.endTime && (
            <p>
              UTC: {toUTCISOString(formData.endTime)} | 
              Perú: {new Date(formData.endTime).toLocaleString("es-PE")}
            </p>
          )}
        </div>

        {/* Botón de envío */}
        <button type="submit">Guardar Cita</button>
      </form>
    </div>
  );
};

export default CrearCitaForm;
