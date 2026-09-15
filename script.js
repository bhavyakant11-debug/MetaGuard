const uploadInput = document.getElementById("label-upload");
const imagePreview = document.getElementById("image-preview");
const scanButton = document.getElementById("scan-button");

uploadInput.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);

        imagePreview.innerHTML = `
            <img src="${imageURL}" alt="Uploaded product label">
        `;
    }
});

scanButton.addEventListener("click", async function () {

    const file = uploadInput.files[0];

    if (!file) {
        alert("Please upload a product label first.");
        return;
    }

    scanButton.textContent = "Analyzing...";
    scanButton.disabled = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(
            "https://metaguard-d5ow.onrender.com/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        console.log("Backend result:", result);

document.getElementById("results-section").style.display = "block";

document.getElementById("compliance-score").textContent =
    result.compliance.compliance_score + "%";

document.getElementById("compliance-status").textContent =
    result.compliance.compliance_status;

    } catch (error) {
        console.error("Error:", error);
        alert("Could not connect to the backend.");

    } finally {
        scanButton.textContent = "Scan a Label →";
        scanButton.disabled = false;
    }
});