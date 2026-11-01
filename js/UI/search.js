const searchInput = document.getElementById('options-search');



export function initializeSearch() {
    searchInput.addEventListener('input', () => {
        console.log('Search input changed:', searchInput.value);
        const query = searchInput.value.trim().toLowerCase();
        performSearch(query);
    });
}

export function performSearch(query) {
    const details = document.querySelectorAll('details');
    
    details.forEach(detail => {
        const options = detail.querySelectorAll('label.checkbox-container');
        let hasVisibleOptions = false;
        options.forEach(option => {
            const label = option.querySelector('span.label-text');
            const matches = label.textContent.toLowerCase().includes(query);
            
            option.hidden = !matches;
            hasVisibleOptions = hasVisibleOptions || matches;
        });
        detail.hidden = !hasVisibleOptions;
    });
}
