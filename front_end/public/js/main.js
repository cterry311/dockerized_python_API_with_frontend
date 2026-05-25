const itemList = document.getElementById("items")
const addButton = document.getElementById("newRecordPush")
const newRecord = document.getElementById("newRecord")
const body = document.getElementById("body")

async function refreshList() {
    const response = await fetch("records")
    const records = await response.json()
    const keys = Object.keys(records.content)
    itemList.innerHTML = ""
    for (const key of keys) {
        const itemElement = document.createElement("li")
        itemElement.id = key
        const deleteButton = document.createElement("button")
        deleteButton.classList.add("deleteButton")
        deleteButton.textContent = "Delete"
        const editButton = document.createElement("button")
        editButton.classList.add("editButton")
        editButton.textContent = "Edit"
        const textContent = document.createElement("p")
        textContent.textContent = JSON.stringify(records.content[key], null, 5)
        deleteButton.addEventListener("click", async () => {
            await fetch("records", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({id: key})
            })
            refreshList()
        });
        editButton.addEventListener("click", async () => {
            if (textContent.contentEditable === "true") {
                let worked;
                try {
                    JSON.parse(textContent.textContent)
                    worked = true
                } catch (e) {
                    worked = false
                }
                if (worked) {
                    fetch("records", {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({id: key, data: textContent.textContent})
                    })
                    refreshList()
                } else {
                    alert("Not a valid JSON")
                }
            } else {
                textContent.contentEditable = "true"
                editButton.textContent = "Save"
            }
        })
        itemElement.appendChild(deleteButton)
        itemElement.appendChild(editButton)
        itemElement.appendChild(textContent)
        itemList.appendChild(itemElement)
    }
}

addButton.addEventListener("click", async () => {
    let correct;
    try {
        JSON.parse(newRecord.textContent)
        correct = true
    } catch (e) {
        correct = false
    }
    if (!correct) {
        alert("Not a valid JSON")
        return
    }
    await fetch("records", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({data: JSON.parse(newRecord.textContent)})
    })
    refreshList()
    newRecord.textContent = "{}"
})

function getRandomBrightHexColor() { // I used AI to get a basic method for this, their implementaiton sucked so I basically completely changed it
    let r;
    let g;
    let b;
    switch (Math.floor(Math.random() * 3)) {
        case 0:
            r = 255;
            if (Math.random() < 0.5) {
                g = Math.floor(Math.random() * 256);
                b = 0
            } else {
                b = Math.floor(Math.random() * 256);
                g = 0
            }
            break;
        case 1:
            g = 255;
            if (Math.random() < 0.5) {
                r = Math.floor(Math.random() * 256);
                b = 0;
            } else {
                b = Math.floor(Math.random() * 256);
                r = 0;
            }
            break;
        case 2:
            b = 255;
            if (Math.random() < 0.5) {
                r = Math.floor(Math.random() * 256);
                g = 0;
            } else {
                g = Math.floor(Math.random() * 256);
                r = 0
            }
            break;
    }

    return (
        "#" +
        r.toString(16).padStart(2, "0") +
        g.toString(16).padStart(2, "0") +
        b.toString(16).padStart(2, "0")
    );
}

function setFunMode() {
    setInterval(() => {
        body.setAttribute("style", "background-color: " + getRandomBrightHexColor() + "; color: " + getRandomBrightHexColor());
    }, 1)
}



// the stuff down here is for the prediction route

const sepalLength = document.getElementById("sepalLength")
const sepalWidth = document.getElementById("sepalWidth")
const petalLength = document.getElementById("petalLength")
const petalWidth = document.getElementById("petalWidth")
const submitButton = document.getElementById("submit")
const prediction = document.getElementById("modelOutput")

submitButton.addEventListener("click", async () => {
    const response = await fetch("predict", {
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": JSON.stringify([sepalLength.value, sepalWidth.value, petalLength.value, petalWidth.value])
    })
    const data = await response.json()
    prediction.textContent = JSON.stringify(data, null, 5)
    sepalLength.value = ""
    sepalWidth.value = ""
    petalLength.value = ""
    petalWidth.value = ""
})

const chatInput = document.getElementById("chatInput")
const chatOutput = document.getElementById("chatOutput")
const chatButton = document.getElementById("chatButton")

chatButton.addEventListener("click", async () => {
    chatOutput.textContent = "waiting..."
    const response = await fetch("chat", {
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": JSON.stringify({message: chatInput.value})
    })
    const data = await response.json()
    console.log(data)
    chatOutput.textContent = data.content
    chatInput.value = ""
})

refreshList()