document.addEventListener('DOMContentLoaded', () => {
    const oceanElement = document.getElementById('ocean');
    const rows = 20;
    const cols = 50;

    function createOcean() {
        for (let i = 0; i < rows; i++) {
            const row = document.createElement('div');
            row.className = 'ocean-row';
            row.textContent = '0'.repeat(cols);
            oceanElement.appendChild(row);
        }
    }

    createOcean();
});
