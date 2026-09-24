const aboutData = {
  title: "About",
  mission: "Our mission is to build simple, reliable software that gets out of the way.",
  description: [
    "We are a small team focused on clean design and solid engineering.",
    "Every product we ship starts with a real problem and ends with a simple solution.",
  ],
};

function renderAboutPage(data) {
  const main = document.getElementById("app");

  const title = document.createElement("h1");
  title.textContent = data.title;

  const mission = document.createElement("p");
  mission.textContent = data.mission;

  const list = document.createElement("ul");
  data.description.forEach((text) => {
    const li = document.createElement("li");
    li.textContent = text;
    list.appendChild(li);
  });

  main.append(title, mission, list);
}

renderAboutPage(aboutData);
