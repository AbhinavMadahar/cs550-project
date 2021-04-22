document.getElementById('movie').oninput = async function (event) {
    const query = this.value;
    const response = await fetch(`/recommendation?query=${query}`);
}