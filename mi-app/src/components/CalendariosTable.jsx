    import React, { useEffect, useState } from "react";

    const CalendariosTable = () => {
    const [calendarios, setCalendarios] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCalendars = async () => {
        try {
            const res = await fetch("http://127.0.0.1:8000/app/calendars/");
            if (!res.ok) throw new Error("Error al obtener calendarios");
            const data = await res.json();
            setCalendarios(data);
        } catch (err) {
            console.error("❌ Error:", err);
        } finally {
            setLoading(false);
        }
        };
        fetchCalendars();
    }, []);

    if (loading) return <p>Cargando calendarios...</p>;

    return (
        <div className="card">
        <h2>📅 Lista de Calendarios</h2>
        <table className="table" >
            <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Estado</th>
            </tr>
            </thead>
            <tbody>
            {calendarios.map((cal) => (
                <tr key={cal.id}>
                <td>{cal.id}</td>
                <td>{cal.name}</td>
                <td>{cal.status}</td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    );
    };

    export default CalendariosTable;
    // ===============================