const aboutToggle = document.getElementById("about-toggle");
const aboutPage = document.getElementById("about-page");
const aboutClose = document.getElementById("about-close");
const aboutTitle = document.getElementById("about-title");
const aboutContent = document.getElementById("about-content");
const headerMeta = document.getElementById("header-meta");


// About page rendering functions
function isAboutLinkObject(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  if (value.type !== 'link') return false;
  return typeof value.url === 'string' && value.url.trim() !== '';
}

function createAboutLink(linkData) {
  const link = document.createElement('a');
  link.href = linkData.url;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.textContent = linkData.label || linkData.text || linkData.url;
  return link;
}

function renderAboutValue(value) {
  if (isAboutLinkObject(value)) {
    const paragraph = document.createElement('p');
    paragraph.appendChild(createAboutLink(value));
    return paragraph;
  }

  if (Array.isArray(value)) {
    const list = document.createElement('ul');
    value.forEach(item => {
      const listItem = document.createElement('li');
      if (item && typeof item === 'object') {
        listItem.appendChild(renderAboutValue(item));
      } else {
        listItem.textContent = item;
      }
      list.appendChild(listItem);
    });
    return list;
  }

  if (value && typeof value === 'object') {
    const container = document.createElement('div');
    Object.entries(value).forEach(([key, item]) => {
      const block = document.createElement('div');
      block.className = 'about-entry';

      const title = document.createElement('h4');
      title.textContent = key;
      block.appendChild(title);
      block.appendChild(renderAboutValue(item));
      container.appendChild(block);
    });
    return container;
  }

  const paragraph = document.createElement('p');
  paragraph.textContent = value;
  return paragraph;
}

function setAboutOpen(isOpen) {
  if (!aboutPage) return;
  aboutPage.classList.toggle('open', isOpen);
  aboutPage.setAttribute('aria-hidden', String(!isOpen));
}

export function initializeAboutPage() {

    if (aboutToggle && aboutPage) {
    aboutToggle.addEventListener('click', () => {
        setAboutOpen(!aboutPage.classList.contains('open'));
    });
    }

    if (aboutClose) {
    aboutClose.addEventListener('click', () => setAboutOpen(false));
    }

    document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        setAboutOpen(false);
    }
    });


    if (aboutPage) {
    document.addEventListener('click', (event) => {
        if (!aboutPage.classList.contains('open')) return;
        if (aboutPage.contains(event.target)) return;
        if (aboutToggle && aboutToggle.contains(event.target)) return;
        setAboutOpen(false);
    });
    }
}


// Load about information from JSON and populate the about page
export function loadAboutInformation() {
    fetch('about/about.json')
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        const aboutData = data.about ?? data.entries ?? {};
        const version = data.version ?? '';
        const lastUpdate = data.last_update ?? data.lastUpdate ?? '';

        if (aboutTitle && data.title) {
        aboutTitle.textContent = data.title;
        }

        if (headerMeta) {
        headerMeta.textContent = [version, lastUpdate].filter(Boolean).join(' | ');
        }

        if (aboutContent) {
        aboutContent.innerHTML = '';

        if (aboutData && typeof aboutData === 'object') {
            Object.entries(aboutData).forEach(([key, value]) => {
            const section = document.createElement('section');
            section.className = 'about-section';

            const title = document.createElement('h4');
            title.textContent = key;
            section.appendChild(title);
            section.appendChild(renderAboutValue(value));
            aboutContent.appendChild(section);
            });
        } else {
            aboutContent.appendChild(renderAboutValue(aboutData));
        }
        }
    })
    .catch(error => {
        console.error('Error loading about.json:', error);
        if (headerMeta) {
        headerMeta.textContent = '';
        }
        if (aboutContent) {
        aboutContent.textContent = 'About information is unavailable.';
        }
    });
}