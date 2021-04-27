document.getElementById('movie').oninput = async function (event) {
    document.getElementById('query-movie').innerHTML = '';

    const query = this.value;
    const addRecommendationsUsingTechnique = async (technique) => {
        document.getElementById(`${technique}-recommendations`).innerHTML = '';

        const titles = [];
        const response = await fetch(`/recommendation?movie=${query}&technique=${technique}`);
        const results = await response.text();
        const recommendations = results.matchAll(/\(.*?\),/g);
        for (let recommendation of recommendations) {
            const parts = recommendation[0].match(/(.*)\ (.*)/);
            const title = parts[1].substring(2, parts[1].length-2);
            titles.push(title)
        }

        if (titles.length === 0) {
            if (query !== '') {
              document.getElementById('query-movie').innerHTML = `${query} not found`;
            }

            return;
        }

        document.getElementById('query-movie').innerHTML = 'Movies similar to ' + query;
        const list = titles.slice(1, titles.length).map(title => `<li class="recommendation">${title}</li>`).reduce((acc, cum) => acc + cum);
        const techniqueDescription = `<li class="recommendation"><strong>Based on ${technique}</strong></li>`;
        document.getElementById(`${technique}-recommendations`).innerHTML = techniqueDescription + list;
    }
    addRecommendationsUsingTechnique('popularity');
    addRecommendationsUsingTechnique('keyword');
}
