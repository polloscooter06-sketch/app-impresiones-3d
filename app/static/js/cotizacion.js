document.getElementById("cotizacionForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;

    const data = {
        cantidad_producto: Number(form.cantidad_producto.value),
        tiempo_impresion: Number(form.tiempo_impresion.value),
        tiempo_postprocesado: Number(form.tiempo_postprocesado.value),
        tiempo_pintado: Number(form.tiempo_pintado.value),
        margenGanancia: Number(form.margenGanancia.value),
        descripcion: form.descripcion.value
    };

    const res = await fetch(`/impresiones/${impresionId}/cotizacion`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("✅ Cotización guardada");
        window.location.href = "/impresiones";
    } else {
        alert("❌ Error");
    }
});
