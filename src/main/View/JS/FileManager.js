let currentModule = null;
let currentFolder = null;
let currentFile = null;

document.addEventListener("DOMContentLoaded", () => {
  fetch("Navigation.html")
    .then((response) => response.text())
    .then((html) => {
      document.getElementById("Navigation").innerHTML = html;
    })
    .catch((error) => console.error("Error loading navigation:", error));
});

//Modules Code
//Display modules and make folders-container visible when a module is clicked
document.addEventListener("DOMContentLoaded", async () => {
  const modules = await getModules();
  displayModules(modules);
});

// backend connection: (GET: list_all_modules)
async function getModules() {
  const url = "http://127.0.0.1:5002/modules";
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: "Bearer Token",
      },
    });

    if (response.ok) {
      const modules = await response.json();
      return modules;
    } else {
      console.error("Failed to fetch modules:", response.statusText);
      return [];
    }
  } catch (error) {
    console.error("Error fetching modules:", error);
    return [];
  }
}

function displayModules(modules) {
  const modulesList = document.getElementById("modules-list");
  modulesList.innerHTML = ""; // Clear existing modules

  modules.forEach((module) => {
    // fill modules list
    const moduleItem = document.createElement("li");
    moduleItem.textContent = module;
    modulesList.appendChild(moduleItem);

    // Make the module clickable
    moduleItem.addEventListener("click", async () => {
      currentModule = module;
      const topics = await getTopics(module);
      displayTopics(topics);
    });

    // Make the module deletable
    deleteModule(moduleItem, module);
  });
}

//Add modules by pressing the add-module icon
document.addEventListener("DOMContentLoaded", () => {
  const addModuleIcon = document.getElementById("add-module");
  const modulesContainer = document
    .getElementById("modules-container")
    .querySelector("ul");

  addModuleIcon.addEventListener("click", () => {
    const moduleName = prompt("Enter the name for the new module:");
    if (moduleName) {
      createModuleInBackend(moduleName).then((success) => {
        if (success) {
          const newListItem = document.createElement("li");
          newListItem.textContent = moduleName;
          modulesContainer.appendChild(newListItem);

          // Make the new child clickable
          newListItem.addEventListener("click", async () => {
            currentModule = moduleName;
            const topics = await getTopics(moduleName);
            displayTopics(topics);
          });

          // Make the new child deletable
          deleteModule(newListItem, moduleName);
        }
      });
    }
  });
});

// backend connection (POST: create_module)
async function createModuleInBackend(moduleName) {
  const url = "http://127.0.0.1:5002/create_module";
  const moduleData = {
    module_name: moduleName,
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer Token",
      },
      body: JSON.stringify(moduleData),
    });

    const result = await response.json();
    if (response.ok) {
      console.log("Module created successfully:", result);
      return true;
    } else {
      console.log("Module already exists:", result);
      alert("Module already exists");
      return false;
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error:", error);
    return false;
  }
}

// Delete module on right-click
function deleteModule(moduleItem, moduleName) {
  moduleItem.addEventListener("contextmenu", (event) => {
    event.preventDefault();

    const deleteOption = confirm("Would you like to delete this element?");
    if (deleteOption) {
      deleteModuleInBackend(moduleName).then((success) => {
        if (success) {
          moduleItem.remove();
          makeFoldersInvisible();
        }
      });
    }
  });
}

// backend connection: (DELETE: delete_module)
async function deleteModuleInBackend(moduleName) {
  const url = "http://127.0.0.1:5002/delete_module/" + moduleName;

  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer Token",
      },
    });

    const result = await response.json();
    if (response.ok) {
      console.log("Module deleted successfully:", result);
      return true;
    } else {
      console.log("Failed to delete module:", result);
      alert("Failed to delete module");
      return false;
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error:", error);
    return false;
  }
}

// Folders Code
// Display folders and make files-container visible when a module is clicked
// backend connection: (GET: list_all_topics_in_a_module)
async function getTopics(moduleName) {
  const url = `http://127.0.0.1:5002/modules/${moduleName}/topics`;
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: "Bearer Token",
      },
    });

    if (response.ok) {
      const topics = await response.json();
      return topics;
    } else {
      console.error("Failed to fetch topics:", response.statusText);
      return [];
    }
  } catch (error) {
    console.error("Error fetching topics:", error);
    return [];
  }
}

function displayTopics(topics) {
  const foldersContainer = document.getElementById("folders-container");
  foldersContainer.innerHTML = ""; // Clear existing folders

  topics.forEach((topic) => {
    // fill folders container
    const newFolder = document.createElement("div");
    newFolder.className = "folder";
    newFolder.innerHTML = `<i class="fas fa-folder folder-icon-design"></i><p>${topic}</p>`;
    foldersContainer.appendChild(newFolder);

    // Make the new folder clickable
    newFolder.addEventListener("click", async () => {
      currentFolder = topic;
      const files = await getFiles(currentModule, topic);
      displayFiles(files);
    });

    // Make the new folder deletable
    deleteFolder(newFolder, currentModule, topic);
  });

  makeFoldersVisible();
}

//Add folders by pressing the add-folder icon
document.addEventListener("DOMContentLoaded", () => {
  const addFolderIcon = document.getElementById("add-folder");

  addFolderIcon.addEventListener("click", () => {
    const folderName = prompt("Enter the name for the new folder:");
    if (folderName) {
      createTopicInBackend(currentModule, folderName).then((success) => {
        if (success) {
          const newFolder = document.createElement("div");
          newFolder.className = "folder";
          newFolder.innerHTML = `<i class="fas fa-folder folder-icon-design"></i><p>${folderName}</p>`;
          foldersContainer.appendChild(newFolder);

          // Make the new folder clickable
          newFolder.addEventListener("click", async () => {
            currentFolder = folderName;
            const files = await getFiles(currentModule, folderName);
            displayFiles(files);
          });

          // Make the new folder deletable
          deleteFolder(newFolder, currentModule, folderName);
        }
      });
    }
  });
});

// backend connection (POST: create_topic)
async function createTopicInBackend(moduleName, folderName) {
  const url = "http://127.0.0.1:5002/create_topic";
  const topicData = {
    module_name: moduleName,
    topic_name: folderName,
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer Token",
      },
      body: JSON.stringify(topicData),
    });

    const result = await response.json();
    if (response.ok) {
      console.log("Topic created successfully:", result);
      return true;
    } else {
      console.log("Topic already exists:", result);
      alert("Topic already exists");
      return false;
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error:", error);
    return false;
  }
}

//Delete folder on right-click
function deleteFolder(folder, moduleName, folderName) {
  folder.addEventListener("contextmenu", (event) => {
    event.preventDefault();

    const deleteOption = confirm("Would you like to delete this element?");
    if (deleteOption) {
      deleteTopicInBackend(moduleName, folderName).then((success) => {
        if (success) {
          folder.remove();
          makeFoldersInvisible();
        }
      });
    }
  });
}

// backend connection: (DELETE: delete_topic)
async function deleteTopicInBackend(moduleName, topicName) {
  const url = `http://127.0.0.1:5002/delete_topic/${moduleName}/${topicName}`;

  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer Token",
      },
      body: JSON.stringify({ module_name: moduleName, topic_name: topicName }),
    });

    const result = await response.json();
    if (response.ok) {
      console.log("Topic deleted successfully:", result);
      return true;
    } else {
      console.log("Failed to delete topic:", result);
      alert("Failed to delete topic");
      return false;
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error:", error);
    return false;
  }
}

// Files Code
// Display files when a folder is clicked
// backend connection: (GET: list_all_files_in_a_topic)
async function getFiles(moduleName, topicName) {
  const url = `http://127.0.0.1:5002/modules/${moduleName}/topics/${topicName}/files`;
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: "Bearer Token",
      },
    });

    if (response.ok) {
      const files = await response.json();
      return files;
    } else {
      console.error("Failed to fetch files:", response.statusText);
      return [];
    }
  } catch (error) {
    console.error("Error fetching files:", error);
    return [];
  }
}

function displayFiles(files) {
  const filesContainer = document.getElementById("files-container");
  filesContainer.innerHTML = ""; // Clear existing files

  files.forEach((file) => {
    // fill files container
    const fileItem = document.createElement("li");
    fileItem.textContent = file;

    // Add Summary button
    const summaryButton = document.createElement("button");
    summaryButton.textContent = "Summary";
    summaryButton.className = "summary-button";
    summaryButton.addEventListener("click", () => {
      getSummary(currentModule, currentFolder, file);
    });

    fileItem.appendChild(summaryButton);
    filesContainer.appendChild(fileItem);

    // Make the file clickable
    fileItem.addEventListener("click", () => {
      currentFile = file;
      openFile(currentModule, currentFolder, file);
    });

    // Make the file deletable
    deleteFile(fileItem, currentModule, currentFolder, file);
  });

  makeFilesVisible();
}

// Open file
async function openFile(moduleName, topicName, fileName) {
  const url = `http://127.0.0.1:5002/files`;
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer Token",
      },
      body: JSON.stringify({ module_name: moduleName, topic_name: topicName, filename: fileName }),
    });

    if (response.ok) {
      const fileUrl = URL.createObjectURL(await response.blob());
      displayFileContent(fileUrl);
    } else {
      console.error("Failed to open file:", response.statusText);
    }
  } catch (error) {
    console.error("Error opening file:", error);
  }
}

function displayFileContent(fileUrl) {
  const modal = document.getElementById("myModal");
  const fileNameElement = document.getElementById("file-name");
  const readTextElement = document.getElementById("read-text");
  const editTextElement = document.getElementById("edit-text");

  fileNameElement.textContent = currentFile;
  readTextElement.innerHTML = `<iframe src="${fileUrl}" width="100%" style="height: calc(100vh - 200px);"></iframe>`;
  editTextElement.value = "";

  modal.style.display = "block";
}

// Get summary
async function getSummary(moduleName, topicName, fileName) {
  const url = `http://127.0.0.1:5002/get_summary`;
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer Token",
      },
      body: JSON.stringify({ module_name: moduleName, topic_name: topicName, filename: fileName }),
    });

    if (response.ok) {
      const result = await response.json();
      alert(`Summary: ${result.data.summary}`);
    } else {
      console.error("Failed to get summary:", response.statusText);
    }
  } catch (error) {
    console.error("Error getting summary:", error);
  }
}

//Delete file on right-click
function deleteFile(fileItem, moduleName, topicName, fileName) {
  fileItem.addEventListener("contextmenu", (event) => {
    event.preventDefault();

    const deleteOption = confirm("Would you like to delete this element?");
    if (deleteOption) {
      deleteFileInBackend(moduleName, topicName, fileName).then((success) => {
        if (success) {
          fileItem.remove();
        }
      });
    }
  });
}

// backend connection: (DELETE: delete_file)
async function deleteFileInBackend(moduleName, topicName, fileName) {
  const url = `http://127.0.0.1:5002/delete_file`;
  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer Token",
      },
      body: JSON.stringify({ module_name: moduleName, topic_name: topicName, filename: fileName }),
    });

    const result = await response.json();
    if (response.ok) {
      console.log("File deleted successfully:", result);
      return true;
    } else {
      console.log("Failed to delete file:", result);
      alert("Failed to delete file");
      return false;
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error:", error);
    return false;
  }
}

// Helper functions
function makeFoldersVisible() {
  const foldersParagraph = document.getElementById("folders-paragraph");
  const foldersContainer = document.getElementById("folders-container");
  const filesHeader = document.getElementById("files-header");
  const filesParagraph = document.getElementById("files-paragraph");
  const filesContainer = document.getElementById("files-container");

  foldersParagraph.style.display = "none";
  foldersContainer.style.display = "flex";
  filesHeader.style.display = "flex";
  filesParagraph.style.display = "flex";
  filesContainer.style.display = "none";
}

function makeFilesVisible() {
  const filesParagraph = document.getElementById("files-paragraph");
  const filesContainer = document.getElementById("files-container");

  filesParagraph.style.display = "none";
  filesContainer.style.display = "flex";
}

function makeFoldersInvisible() {
  const foldersParagraph = document.getElementById("folders-paragraph");
  const foldersContainer = document.getElementById("folders-container");
  const filesHeader = document.getElementById("files-header");
  const filesParagraph = document.getElementById("files-paragraph");
  const filesContainer = document.getElementById("files-container");

  foldersParagraph.style.display = "flex";
  foldersContainer.style.display = "none";
  filesHeader.style.display = "none";
  filesParagraph.style.display = "none";
  filesContainer.style.display = "none";
}

function makeFilesInvisible() {
  const filesParagraph = document.getElementById("files-paragraph");
  const filesContainer = document.getElementById("files-container");

  filesParagraph.style.display = "flex";
  filesContainer.style.display = "none";
}

// Modal Code
const modal = document.getElementById("myModal");
const quitButton = document.getElementById("quit");
const editButton = document.getElementById("edit");
const saveButton = document.getElementById("save");

const modalReadOnly = document.querySelector(".modal-read-only");
const modalTextarea = document.querySelector(".modal-textarea");

// When the user clicks on the quit button, close the modal
quitButton.onclick = () => {
  modalReadOnly.style.display = "flex";
  modalTextarea.style.display = "none";
  modal.style.display = "none";
};

// When the user clicks on the edit button, switch to textarea
editButton.onclick = () => {
  modalReadOnly.style.display = "none";
  modalTextarea.style.display = "flex";
  saveButton.style.display = "flex";
  editButton.style.display = "none";
};

saveButton.onclick = () => {
  modalReadOnly.style.display = "flex";
  modalTextarea.style.display = "none";
  saveButton.style.display = "none";
  editButton.style.display = "flex";
};
