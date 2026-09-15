const predictBtn = document.getElementById("predictBtn");

const failureProbability = document.getElementById("failureProbability");
const machineStatus = document.getElementById("machineStatus");
const riskLevel = document.getElementById("riskLevel");
const failureTypes = document.getElementById("failureTypes");
const maintenanceAction = document.getElementById("maintenanceAction");
const errorMessage = document.getElementById("errorMessage");

predictBtn.addEventListener("click", async () => {

    errorMessage.textContent = "";

    const payload = {
        machine_type: document.getElementById("machineType").value,
        air_temp: Number(document.getElementById("airTemp").value),
        process_temp: Number(document.getElementById("processTemp").value),
        rpm: Number(document.getElementById("rpm").value),
        torque: Number(document.getElementById("torque").value),
        tool_wear: Number(document.getElementById("toolWear").value)
    };

    try {

        predictBtn.disabled = true;
        predictBtn.textContent = "Predicting...";

        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction failed.");
        }

        failureProbability.textContent =
            `${(data.failure_probability * 100).toFixed(2)}%`;

        machineStatus.textContent =
            data.failure ? "FAILURE DETECTED" : "NORMAL";

        riskLevel.textContent =
            data.risk;

        failureTypes.textContent =
            data.failure_types.length > 0
                ? data.failure_types.join(", ")
                : "None";

        maintenanceAction.textContent =
            data.maintenance_action;

    } catch (error) {

        errorMessage.textContent = error.message;

    } finally {

        predictBtn.disabled = false;
        predictBtn.textContent = "Predict Machine Risk";
    }
});