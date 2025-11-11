
// dashboard base page script
document.addEventListener('DOMContentLoaded', () => {
    console.log('Web application initialized');

    let info_text = document.querySelector('.infos-text');

    info_text.addEventListener('click', () => {
        window.location.href = '/about';
    });
});
