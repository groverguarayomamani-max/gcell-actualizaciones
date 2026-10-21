# G-CELL: distribución de actualizaciones

Este repositorio distribuye binarios de G-CELL Ventas. No contiene el código fuente privado de Ventas ni de ERP, bases de datos, configuraciones de sucursales ni claves privadas.

El canal `pilot` es para un piloto controlado pendiente de autorización. Su publicación no autoriza instalaciones ni cambios en el servidor central. El canal estable todavía no está habilitado.

Los paquetes se verifican con RSA-PSS/SHA-256, tamaño exacto, SHA-256, canal, secuencia y vigencia del manifiesto. La clave pública debe obtenerse por un medio inicial confiable. Esta firma no es un certificado Authenticode de Windows.

La renovación diaria conserva exactamente el paquete aprobado; no construye ni promueve versiones. Sólo se admiten los eventos programados y la ejecución manual. Registra fecha y hash en channel-health.json para mantener actividad del repositorio. Si falla la renovación, el programa instalado sigue funcionando y rechaza metadatos vencidos. Revisar las alertas de Actions; la programación de GitHub no tiene disponibilidad garantizada.

No habilitar la inmutabilidad global de Releases: el alias `pilot` renueva sus metadatos. El archivo aprobado de una versión se conserva por separado y nunca se sobrescribe.
