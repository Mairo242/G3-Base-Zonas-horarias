    import React from "react";
    import CalendariosTable from "./components/CalendariosTable";
    import CrearCitaForm from "./components/CrearCitaForm";
    import './App.css';

    function App() {
    return (
        <div className="container">
        <header>
            <h1 className="app-title">Sistema de Gestión de Citas</h1>
        </header>

        <div className="main-content">
            <CalendariosTable />
            <CrearCitaForm />
        </div>

        <footer>
            &copy; 2025 Mi Empresa - Sistema de Citas
        </footer>
        </div>
    );
    }


    export default App;
