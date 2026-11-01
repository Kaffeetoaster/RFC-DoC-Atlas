
const headerMeta = document.getElementById("header-meta");


// Load about information from JSON and show in oneliner
export function loadAboutInformation() {
    fetch('about/about.json')
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        const version = data.version;
        const lastUpdate = data.last_update;

        if (headerMeta) {
        headerMeta.textContent = [version, lastUpdate].filter(Boolean).join(' | ');
        }

    })
}