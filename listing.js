/*// Make sure you're not using IE in 2020
const ua = window.navigator.userAgent;
const msie = ua.indexOf("MSIE ");

if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv:11\./)) window.location.href = "/iebad.html";
*/ // Commented this out, since the corresponding page (iebad.html) was removed, and it only served as personal bias. -- omame

let productList = {};

const repositoryObj = document.querySelector("#repository");
const typeObj = document.querySelector("#type");
const versionObj = document.querySelector("#version");
const editionObj = document.querySelector("#edition");
const downloadURL = document.querySelector("#download");

fetch("/repositories.json").then(data => data.json().then(repositories => {
	repositoryList = repositories;
	for (const i in repositories) {
		repositoryObj.append(new Option(i, i));
	}
}));

fetch("/version.txt").then(data => data.text().then(version => {
	if (data.ok) {
		version = version;
	} else {
		version = "never";
	}
	document.querySelector("#version span").textContent = version;
}));

const updateRepositories = () => {
	repositoryFile = repositoryObj.value.toLowerCase().replace(/\s/g, "_") + ".json";
	repositoryPath = "repositories/" + repositoryFile;

	cleanUpdateType();

	if (repositoryObj.value == 'local') {
		document.querySelector("#note").textContent = "";
		return;
	}

	note = repositoryList[repositoryObj.value].note;
	document.querySelector("#note").textContent = "Note: " + note;

	fetch(repositoryPath).then(data => data.json().then(products => {
		productList = products;
		for (const i in products) {
			typeObj.append(new Option(i, i));
		}
	}));

	updateVersions();
};

const cleanUpdateType = () => {
	let typeOptions = document.querySelectorAll("#type option");

	for (const i of typeOptions) {
		if (!i.disabled) i.remove();
	}

	document.querySelector("#type option[value='placeholder']").selected = true;
}

const updateVersions = () => {
	const versionOptions = document.querySelectorAll("#version option");

	for (const i of versionOptions) {
		if (!i.disabled) i.remove();
	}

	document.querySelector("#version option[value='placeholder']").selected = true;

	for (const i in productList[typeObj.value]) {
		versionObj.append(new Option(i, i));
	}

	updateEditions();
};

const updateEditions = () => {
	let editionOptions = document.querySelectorAll("#edition option");
	for (let i of editionOptions) {
		if (!i.disabled) i.remove();
	}

	document.querySelector("#edition option[value='placeholder']").selected = true;

	for (let i in productList[typeObj.value][versionObj.value]) {
		editionObj.append(new Option(i, i));
	}

	updateURL();
};

const updateURL = () => {
	if (typeObj.value && versionObj.value && editionObj.value) {
		const directoryUrl = '/files';
		const baseUrl = directoryUrl + '/' + repositoryObj.value.toLowerCase().replace(' ', '_');
		let url = productList[typeObj.value][versionObj.value][editionObj.value];
		url = url.replace(/^.*\/\/[^\/]+/, baseUrl);
		downloadURL.href = url;
	} else {
		downloadURL.removeAttr("href");
		downloadURL.disabled = true;
	}
};
