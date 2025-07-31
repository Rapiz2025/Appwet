# Appwet
Revisa 
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestor de Averías - Rapiz (con IA y Zonas)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Estilo para la barra de desplazamiento */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #2563eb; }
        .task-card-enter { animation: fadeIn 0.5s ease-out; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="bg-slate-100 text-slate-800">

    <!-- Contenedor principal -->
    <div class="container mx-auto p-4 md:p-8 max-w-4xl">

        <!-- Cabecera -->
        <header class="text-center mb-8">
            <h1 class="text-4xl md:text-5xl font-bold text-blue-600">Rapiz</h1>
            <p class="text-slate-500 text-lg mt-1">Más que velocidad</p>
        </header>

        <!-- Formulario para agregar nuevas averías -->
        <div class="bg-white p-6 rounded-2xl shadow-lg mb-8">
            <h2 class="text-2xl font-semibold mb-4 border-b pb-3">Registrar Nueva Avería</h2>
            <form id="task-form" class="space-y-4">
                <select id="customer-zone" class="w-full p-3 bg-slate-50 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    <option value="" disabled selected>Seleccionar Zona...</option>
                    <option value="El Puerto">El Puerto</option>
                    <option value="Basima">Basima</option>
                    <option value="Guananito">Guananito</option>
                    <option value="Km61">Km61</option>
                    <option value="Km56">Km56</option>
                    <option value="Km59">Km59</option>
                    <option value="La cumbre">La cumbre</option>
                    <option value="Los mogotes">Los mogotes</option>
                </select>
                <input type="text" id="customer-name" placeholder="Nombre del Cliente" class="w-full p-3 bg-slate-50 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="text" id="customer-nickname" placeholder="Apodo (Opcional)" class="w-full p-3 bg-slate-50 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <input type="text" id="customer-address" placeholder="Dirección del Cliente" class="w-full p-3 bg-slate-50 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <input type="tel" id="customer-phone" placeholder="Número de Teléfono" class="w-full p-3 bg-slate-50 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <textarea id="problem-description" placeholder="Descripción del problema (ej: 'luz roja en el router', 'sin conexión')" class="w-full p-3 bg-slate-50 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" rows="3" required></textarea>
                <input type="date" id="report-date" class="w-full p-3 bg-slate-50 rounded-lg border border-slate-200 text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-300 shadow-md flex items-center justify-center">
                    Agregar Avería
                </button>
            </form>
        </div>

        <!-- Filtro de Zonas -->
        <div class="bg-white p-4 rounded-2xl shadow-lg mb-8">
             <label for="zone-filter" class="block text-sm font-medium text-slate-700 mb-2">Filtrar por Zona:</label>
             <select id="zone-filter" class="w-full p-3 bg-slate-50 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="all">Mostrar Todas las Zonas</option>
                <option value="El Puerto">El Puerto</option>
                <option value="Basima">Basima</option>
                <option value="Guananito">Guananito</option>
                <option value="Km61">Km61</option>
                <option value="Km56">Km56</option>
                <option value="Km59">Km59</option>
                <option value="La cumbre">La cumbre</option>
                <option value="Los mogotes">Los mogotes</option>
             </select>
        </div>

        <!-- Lista de averías -->
        <div id="task-list" class="space-y-4">
            <!-- Las tarjetas de averías se insertarán aquí dinámicamente -->
        </div>

    </div>

    <!-- Modal de Confirmación de Borrado -->
    <div id="delete-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 hidden z-40">
        <div class="bg-white rounded-2xl shadow-xl p-8 max-w-sm w-full text-center">
            <h3 class="text-xl font-bold mb-4">¿Confirmar Eliminación?</h3>
            <p class="text-slate-600 mb-6">Esta acción no se puede deshacer. ¿Estás seguro?</p>
            <div class="flex justify-center gap-4">
                <button id="cancel-delete-btn" class="py-2 px-6 bg-slate-200 text-slate-800 rounded-lg hover:bg-slate-300 transition-colors">Cancelar</button>
                <button id="confirm-delete-btn" class="py-2 px-6 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors">Eliminar</button>
            </div>
        </div>
    </div>

    <!-- Modal para Gemini -->
    <div id="gemini-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 hidden z-50">
        <div class="bg-white rounded-2xl shadow-xl p-6 max-w-2xl w-full max-h-[90vh] flex flex-col">
            <div class="flex justify-between items-center mb-4">
                <h3 id="gemini-modal-title" class="text-xl font-bold"></h3>
                <button id="close-gemini-modal-btn" class="text-slate-500 hover:text-slate-800 text-3xl leading-none">&times;</button>
            </div>
            <div id="gemini-modal-content" class="flex-grow overflow-y-auto bg-slate-50 p-4 rounded-lg border">
                <!-- Contenido generado por Gemini aquí -->
            </div>
            <div class="mt-4 flex justify-end gap-4">
                <button id="copy-gemini-content-btn" class="py-2 px-6 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors">Copiar Texto</button>
            </div>
        </div>
    </div>


    <!-- Módulo de Firebase y Lógica de la App -->
    <script type="module">
        // Importaciones de Firebase
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, collection, addDoc, onSnapshot, doc, updateDoc, deleteDoc, query, setLogLevel, getDoc } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

        // --- CONFIGURACIÓN ---
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'rapiz-averias-app';
        
        const DUMMY_CONFIG = {
            apiKey: "AIzaSy...DEMO...KEY...",
            authDomain: "project-id.firebaseapp.com",
            projectId: "project-id",
            storageBucket: "project-id.appspot.com",
            messagingSenderId: "123456789012",
            appId: "1:123456789012:web:1234567890abcdef"
        };

        const firebaseConfig = JSON.parse(
            typeof __firebase_config !== 'undefined' ? __firebase_config : JSON.stringify(DUMMY_CONFIG)
        );

        let app, db, auth, userId;
        let taskToDeleteId = null;
        let allTasks = []; // Almacenará todas las tareas para filtrar

        // --- INICIALIZACIÓN ---
        async function initialize() {
            try {
                app = initializeApp(firebaseConfig);
                db = getFirestore(app);
                auth = getAuth(app);
                setLogLevel('debug');

                onAuthStateChanged(auth, async (user) => {
                    if (user) {
                        userId = user.uid;
                        console.log("Usuario autenticado:", userId);
                        loadTasks();
                    } else {
                        console.log("Iniciando sesión...");
                        try {
                            if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
                                await signInWithCustomToken(auth, __initial_auth_token);
                            } else {
                                console.log("No hay token de autenticación. La app funcionará en modo local (sin datos).");
                            }
                        } catch (error) {
                            console.error("Error en el inicio de sesión:", error);
                        }
                    }
                });
            } catch (error) {
                console.error("Error inicializando Firebase:", error);
                document.body.innerHTML = '<div class="text-center p-8 text-red-500">Error de configuración. La aplicación no puede iniciarse.</div>';
            }
        }

        // --- REFERENCIAS DEL DOM ---
        const taskForm = document.getElementById('task-form');
        const customerZoneInput = document.getElementById('customer-zone');
        const customerNameInput = document.getElementById('customer-name');
        const customerNicknameInput = document.getElementById('customer-nickname');
        const customerAddressInput = document.getElementById('customer-address');
        const customerPhoneInput = document.getElementById('customer-phone');
        const problemDescriptionInput = document.getElementById('problem-description');
        const reportDateInput = document.getElementById('report-date');
        const taskListContainer = document.getElementById('task-list');
        const zoneFilter = document.getElementById('zone-filter');
        const deleteModal = document.getElementById('delete-modal');
        const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
        const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
        const geminiModal = document.getElementById('gemini-modal');
        const geminiModalTitle = document.getElementById('gemini-modal-title');
        const geminiModalContent = document.getElementById('gemini-modal-content');
        const closeGeminiModalBtn = document.getElementById('close-gemini-modal-btn');
        const copyGeminiContentBtn = document.getElementById('copy-gemini-content-btn');

        // --- LÓGICA DE GEMINI API ---
        async function generateTextWithGemini(prompt) {
            const apiKey = ""; // Se deja vacío, el entorno lo provee.
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
            const payload = { contents: [{ role: "user", parts: [{ text: prompt }] }] };

            try {
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (!response.ok) throw new Error(`Error de API: ${response.statusText}`);
                const result = await response.json();
                if (result.candidates && result.candidates[0]?.content.parts[0]?.text) {
                    return result.candidates[0].content.parts[0].text;
                }
                return "No se pudo obtener una respuesta de la IA.";
            } catch (error) {
                console.error("Error llamando a la API de Gemini:", error);
                return `Error de conexión con la IA. Detalles: ${error.message}`;
            }
        }

        // --- LÓGICA DE LA APLICACIÓN ---
        function loadTasks() {
            if (!userId) {
                console.log("No hay usuario, no se cargarán tareas.");
                return;
            }
            const collectionPath = `/artifacts/${appId}/public/data/averias`;
            const q = query(collection(db, collectionPath));

            onSnapshot(q, (snapshot) => {
                allTasks = [];
                snapshot.forEach((doc) => allTasks.push({ id: doc.id, ...doc.data() }));
                renderFilteredTasks();
            }, (error) => {
                console.error("Error al obtener tareas (esto es esperado en modo local): ", error.message);
                taskListContainer.innerHTML = `<div class="text-center text-slate-500 p-8">No se pueden cargar los datos. Asegúrate de estar usando la aplicación en el modo "Preview".</div>`;
            });
        }

        function renderFilteredTasks() {
            const currentZone = zoneFilter.value;
            const tasksToRender = (currentZone === 'all') 
                ? allTasks 
                : allTasks.filter(task => task.zone === currentZone);

            tasksToRender.sort((a, b) => {
                if (a.status === 'Pendiente' && b.status !== 'Pendiente') return -1;
                if (a.status !== 'Pendiente' && b.status === 'Pendiente') return 1;
                return new Date(a.reportDate) - new Date(b.reportDate);
            });
            
            taskListContainer.innerHTML = '';
            if (tasksToRender.length === 0 && userId) {
                taskListContainer.innerHTML = `<div class="text-center text-slate-500 p-8">No hay averías registradas. ¡Agrega una para comenzar!</div>`;
            } else {
                 tasksToRender.forEach(renderTask);
            }
        }

        function renderTask(task) {
            const card = document.createElement('div');
            card.className = `task-card-enter bg-white p-5 rounded-xl shadow-md border-l-4 transition-all duration-300 ${task.status === 'Completado' ? 'border-green-500 bg-slate-50 opacity-70' : 'border-blue-500'}`;
            card.setAttribute('data-id', task.id);

            const isCompleted = task.status === 'Completado';
            const textDecoration = isCompleted ? 'line-through' : '';
            const mapsLink = `https://www.google.com/maps?q=${encodeURIComponent(task.address)}`;

            let aiButtonsHTML = '';
            if (isCompleted) {
                aiButtonsHTML = `
                    <button class="generate-followup-btn flex items-center justify-center gap-2 w-full py-2 px-3 text-sm font-semibold rounded-lg bg-teal-100 text-teal-700 hover:bg-teal-200 transition-colors">
                        ✨ Generar Seguimiento
                    </button>
                    <button class="generate-plan-btn flex items-center justify-center gap-2 w-full py-2 px-3 text-sm font-semibold rounded-lg bg-indigo-100 text-indigo-700 hover:bg-indigo-200 transition-colors">
                        ✨ Ver Plan de Acción
                    </button>
                `;
            } else {
                aiButtonsHTML = `
                    <button class="generate-causes-btn flex items-center justify-center gap-2 w-full py-2 px-3 text-sm font-semibold rounded-lg bg-amber-100 text-amber-700 hover:bg-amber-200 transition-colors">
                        ✨ Sugerir Causas
                    </button>
                    <button class="generate-plan-btn flex items-center justify-center gap-2 w-full py-2 px-3 text-sm font-semibold rounded-lg bg-indigo-100 text-indigo-700 hover:bg-indigo-200 transition-colors">
                        ✨ ${task.actionPlan ? 'Ver Plan de Acción' : 'Generar Plan de Acción'}
                    </button>
                    <button class="generate-message-btn col-span-full flex items-center justify-center gap-2 w-full py-2 px-3 text-sm font-semibold rounded-lg bg-sky-100 text-sky-700 hover:bg-sky-200 transition-colors">
                        ✨ Crear Mensaje Cliente
                    </button>
                `;
            }

            card.innerHTML = `
                <div class="flex justify-between items-start flex-wrap gap-2">
                    <div>
                        <h3 class="font-bold text-xl ${textDecoration} text-slate-800">${task.name}</h3>
                        ${task.nickname ? `<p class="text-slate-600 font-medium ${textDecoration}">(${task.nickname})</p>` : ''}
                        <p class="text-slate-500 ${textDecoration}">${task.address}</p>
                    </div>
                    <div class="flex items-center gap-2 flex-shrink-0">
                        <span class="text-xs font-semibold px-3 py-1 rounded-full bg-purple-100 text-purple-800">${task.zone}</span>
                        <span class="text-xs font-semibold px-3 py-1 rounded-full ${isCompleted ? 'bg-green-200 text-green-800' : 'bg-blue-100 text-blue-800'}">${task.status}</span>
                    </div>
                </div>

                <div class="mt-4 pt-4 border-t border-slate-200 space-y-3">
                    <p class="text-slate-600"><span class="font-semibold">Problema:</span> ${task.description || 'No especificado'}</p>
                    <p class="text-slate-600 ${textDecoration}"><span class="font-semibold">Teléfono:</span> ${task.phone}</p>
                    <p class="text-slate-600 ${textDecoration}"><span class="font-semibold">Fecha Reporte:</span> ${new Date(task.reportDate).toLocaleDateString('es-ES', { timeZone: 'UTC' })}</p>
                    <a href="${mapsLink}" target="_blank" class="inline-block text-blue-600 hover:underline font-semibold">Ver Ubicación en Mapa &#8599;</a>
                </div>
                
                <div class="mt-4 pt-4 border-t border-slate-200">
                    <h4 class="text-sm font-bold text-slate-600 mb-2">Asistente IA</h4>
                    <div class="grid grid-cols-2 md:grid-cols-2 gap-2">
                        ${aiButtonsHTML}
                    </div>
                </div>

                <div class="flex gap-2 mt-4">
                    <button class="toggle-status-btn w-full py-2 px-4 text-sm font-semibold rounded-lg transition-colors ${isCompleted ? 'bg-yellow-500 text-white hover:bg-yellow-600' : 'bg-green-500 text-white hover:bg-green-600'}">
                        ${isCompleted ? 'Marcar como Pendiente' : 'Marcar como Completado'}
                    </button>
                    <button class="delete-task-btn p-2 bg-red-100 text-red-600 hover:bg-red-200 font-semibold rounded-lg transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/><path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/></svg>
                    </button>
                </div>
            `;
            taskListContainer.appendChild(card);
        }
        
        // --- MANEJADORES DE EVENTOS ---
        taskForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (!customerNameInput.value.trim() || !customerZoneInput.value) return;
            if(!userId) {
                alert("No se pueden agregar tareas en modo local. Por favor, usa la aplicación desde el modo 'Preview'.");
                return;
            }

            const newTask = {
                zone: customerZoneInput.value,
                name: customerNameInput.value,
                nickname: customerNicknameInput.value,
                address: customerAddressInput.value,
                phone: customerPhoneInput.value,
                description: problemDescriptionInput.value,
                reportDate: reportDateInput.value,
                status: 'Pendiente',
                createdAt: new Date().toISOString(),
                createdBy: userId,
                actionPlan: null
            };

            try {
                const collectionPath = `/artifacts/${appId}/public/data/averias`;
                await addDoc(collection(db, collectionPath), newTask);
                taskForm.reset();
                reportDateInput.value = new Date().toISOString().split('T')[0];
            } catch (error) {
                console.error("Error al agregar la tarea: ", error);
            }
        });

        zoneFilter.addEventListener('change', renderFilteredTasks);

        taskListContainer.addEventListener('click', async (e) => {
            const card = e.target.closest('.task-card-enter');
            if (!card) return;

            const taskId = card.getAttribute('data-id');
            const collectionPath = `/artifacts/${appId}/public/data/averias`;
            const taskDocRef = doc(db, collectionPath, taskId);

            if (e.target.closest('.toggle-status-btn')) {
                const docSnap = await getDoc(taskDocRef);
                if (docSnap.exists()) {
                    const newStatus = docSnap.data().status === 'Pendiente' ? 'Completado' : 'Pendiente';
                    await updateDoc(taskDocRef, { status: newStatus });
                }
            }

            if (e.target.closest('.delete-task-btn')) {
                taskToDeleteId = taskId;
                deleteModal.classList.remove('hidden');
            }
            
            const docSnap = await getDoc(taskDocRef);
            if (!docSnap.exists()) return;
            const taskData = docSnap.data();

            if (e.target.closest('.generate-causes-btn')) {
                const prompt = `Eres un asistente de diagnóstico para 'Rapiz', una empresa de internet por fibra óptica. Basado en la descripción del problema de un cliente: "${taskData.description}", y su ubicación en la zona '${taskData.zone}', lista las 3 causas más probables de la avería, explicando brevemente cada una en una línea. Sé conciso y técnico.`;
                showGeminiModal('Sugiriendo Causas Probables...', '<div class="flex justify-center items-center h-full"><div class="loader"></div></div>', false);
                const causes = await generateTextWithGemini(prompt);
                showGeminiModal('Causas Probables', causes);
            }

            if (e.target.closest('.generate-plan-btn')) {
                if (taskData.actionPlan) {
                    showGeminiModal('Plan de Acción Guardado', taskData.actionPlan);
                } else {
                    const prompt = `Eres un técnico experto en fibra óptica para la empresa 'Rapiz'. Un cliente en la zona '${taskData.zone}' reporta el siguiente problema: "${taskData.description}". Crea un plan de acción técnico, claro y conciso, con pasos numerados para que un técnico de campo diagnostique y resuelva la avería.`;
                    showGeminiModal('Generando Plan de Acción...', '<div class="flex justify-center items-center h-full"><div class="loader"></div></div>', false);
                    const plan = await generateTextWithGemini(prompt);
                    await updateDoc(taskDocRef, { actionPlan: plan });
                    showGeminiModal('Plan de Acción Generado', plan);
                }
            }

            if (e.target.closest('.generate-message-btn')) {
                const prompt = `Actúa como el despachador de la empresa de internet 'Rapiz'. Redacta un mensaje de WhatsApp corto, profesional y amable para el cliente '${taskData.name}' (conocido como ${taskData.nickname || 'el cliente'}) para informarle que un técnico visitará su domicilio en '${taskData.address}' (zona de ${taskData.zone}) para resolver la avería reportada. Menciona que el técnico se comunicará antes de llegar.`;
                showGeminiModal('Generando Mensaje para Cliente...', '<div class="flex justify-center items-center h-full"><div class="loader"></div></div>', false);
                const message = await generateTextWithGemini(prompt);
                showGeminiModal('Mensaje para Cliente', message);
            }

            if (e.target.closest('.generate-followup-btn')) {
                const prompt = `Actúa como el gerente de satisfacción al cliente de 'Rapiz'. Redacta un mensaje de WhatsApp corto y muy amable para el cliente '${taskData.name}' (conocido como ${taskData.nickname || 'el cliente'}) para dar seguimiento a una reparación que se completó. Pregúntale si su servicio de internet funciona correctamente y si está satisfecho con la reparación. Finaliza invitándole a dejar una reseña positiva si lo desea.`;
                showGeminiModal('Generando Mensaje de Seguimiento...', '<div class="flex justify-center items-center h-full"><div class="loader"></div></div>', false);
                const message = await generateTextWithGemini(prompt);
                showGeminiModal('Mensaje de Seguimiento', message);
            }
        });

        // Eventos de Modales
        confirmDeleteBtn.addEventListener('click', async () => {
            if (taskToDeleteId) {
                const collectionPath = `/artifacts/${appId}/public/data/averias`;
                await deleteDoc(doc(db, collectionPath, taskToDeleteId));
                hideDeleteModal();
            }
        });

        cancelDeleteBtn.addEventListener('click', hideDeleteModal);
        closeGeminiModalBtn.addEventListener('click', hideGeminiModal);
        copyGeminiContentBtn.addEventListener('click', () => {
            const textToCopy = geminiModalContent.innerText;
            try {
                const textArea = document.createElement("textarea");
                textArea.value = textToCopy;
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                copyGeminiContentBtn.innerText = '¡Copiado!';
                setTimeout(() => { copyGeminiContentBtn.innerText = 'Copiar Texto'; }, 2000);
            } catch (err) {
                console.error('Error al copiar:', err);
            }
        });
        
        function hideDeleteModal() {
            taskToDeleteId = null;
            deleteModal.classList.add('hidden');
        }

        function showGeminiModal(title, content, showCopy = true) {
            geminiModalTitle.innerText = title;
            geminiModalContent.innerHTML = content.replace(/\n/g, '<br>');
            copyGeminiContentBtn.style.display = showCopy ? 'block' : 'none';
            if (showCopy) {
                copyGeminiContentBtn.innerText = 'Copiar Texto';
            }
            geminiModal.classList.remove('hidden');
        }

        function hideGeminiModal() {
            geminiModal.classList.add('hidden');
        }

        // --- INICIO ---
        reportDateInput.value = new Date().toISOString().split('T')[0];
        initialize();

    </script>
</body>
</html>

