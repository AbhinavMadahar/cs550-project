document.getElementById('movie').oninput = async function (event) {
    document.getElementById('query-movie').innerHTML = '';
    document.getElementById('recommendations').innerHTML = '';

    const titles = [];

    const query = this.value;
    const response = await fetch(`/recommendation?movie=${query}`);
    const results = await response.text();
    const recommendations = results.matchAll(/\(.*?\),/g);
    for (let recommendation of recommendations) {
        const parts = recommendation[0].match(/(.*)\ (.*)/);
        const title = parts[1].substring(2, parts[1].length-2);
        titles.push(title)
    }

    if (titles.length === 0) {
        return;
    }

    document.getElementById('query-movie').innerHTML = 'Movies similar to ' + titles[0];
    const list = titles.slice(1, titles.length).map(title => `<li class="recommendation">${title}</li>`).reduce((acc, cum) => acc + cum);
    document.getElementById('recommendations').innerHTML = list;
}