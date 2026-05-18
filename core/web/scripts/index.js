
const hamburger      = document.getElementById('hamburger');
const sidebar        = document.querySelector('.vertical-container');
const overlay        = document.getElementById('sidebarOverlay');

function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('visible');
    hamburger.classList.add('open');
    document.body.style.overflow = 'hidden';
}

function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('visible');
    hamburger.classList.remove('open');
    document.body.style.overflow = '';
}

hamburger.addEventListener('click', () => {
    sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
});

// cloeses with overlay
overlay.addEventListener('click', closeSidebar);

// closes with ESC
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSidebar();
});


// dashboard base page script
document.addEventListener('DOMContentLoaded', () => {
    console.log('Web application initialized');

    let info_text = document.querySelector('.infos-text');

    info_text.addEventListener('click', () => {
        window.location.href = '/about';
    });
});

// menu groups toggle
document.querySelectorAll('.menu-group-header').forEach(btn => {
    btn.addEventListener('click', () => {
        const group = btn.closest('.menu-group');
        group.classList.toggle('open');
    });
});