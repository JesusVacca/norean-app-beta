window.addEventListener('DOMContentLoaded', function () {
    const $ = (selector) => document.querySelector(selector);
    const $$ = (selector) => document.querySelectorAll(selector);
    // Obtiene la plantilla renderizada para obtener su contenido
    const sectionJs = document.querySelector('#section-data');

    const sidebar = $('#sidebar');
    const toggleButton = $('#sidebar-button');
    const dropdownItems = $$('.menu-item-dropdowm');
    const allLinks = $$('.menu-link');

    // Le da el foco al link dependiendo de la seccion renderizada
    if(sectionJs){
        const sectionIndex = JSON.parse(sectionJs.value);
        if(!isNaN(sectionIndex)){
            localStorage.setItem('activeMenuIndex',sectionIndex);
        }
    }


    // ───────────────────────────────────────
    // 👉 Restaurar estado guardado (menú activo y submenú abierto)
    const savedIndex = localStorage.getItem('activeMenuIndex');
    if (savedIndex !== null) {
        const savedLink = allLinks[savedIndex];
        if (savedLink) {
            savedLink.classList.add('active');
            // Si está en un submenú, abrirlo también
            const parentDropdown = savedLink.closest('.menu-item-dropdowm');
            if (parentDropdown) {
                parentDropdown.classList.add('menu-item-toggle');
                const subMenu = parentDropdown.querySelector('.sub-menu');
                subMenu.style.height = subMenu.scrollHeight + 'px';
                const dropdownLink = parentDropdown.querySelector('.menu-link');
                dropdownLink?.setAttribute('aria-expanded', 'true');
            }
        }
    }
    const sidebarClosed = localStorage.getItem('sidebarClosed') === 'true';
    if (sidebarClosed) {
        sidebar.classList.add('toggle');
    }

    // ───────────────────────────────────────
    // 👉 Alternar visibilidad del sidebar
    toggleButton.addEventListener('click', () => {
        sidebar.classList.toggle('toggle');
        localStorage.setItem('sidebarClosed', sidebar.classList.contains('toggle'));
    });

    // ───────────────────────────────────────
    // 👉 Manejar submenús desplegables
    dropdownItems.forEach((menuItem) => {
        const link = menuItem.querySelector('.menu-link');
        const subMenu = menuItem.querySelector('.sub-menu');

        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');

            // Prevenir navegación solo si es un botón, no una ruta
            if (!href || href === '#') {
                e.preventDefault();
            }

            const isOpen = menuItem.classList.contains('menu-item-toggle');

            // Cierra todos los submenús
            dropdownItems.forEach((item) => {
                item.classList.remove('menu-item-toggle');
                item.querySelector('.sub-menu').style.height = '0';
                item.querySelector('.menu-link')?.setAttribute('aria-expanded', 'false');
            });

            // Abrir solo si no estaba abierto
            if (!isOpen) {
                menuItem.classList.add('menu-item-toggle');
                subMenu.style.height = subMenu.scrollHeight + 'px';
                link.setAttribute('aria-expanded', 'true');
            }
        });
    });

    // ───────────────────────────────────────
    // 👉 Activar enlace y guardar en localStorage
    allLinks.forEach((link, index) => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            // Solo prevenir si es un botón sin navegación
            if (!href || href === '#') {
                e.preventDefault();
            }

            // Activar el enlace visualmente
            allLinks.forEach((l) => l.classList.remove('active'));
            link.classList.add('active');
            // Guardar el índice en localStorage
            localStorage.setItem('activeMenuIndex', index);
        });
    });
});
