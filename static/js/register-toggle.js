document.addEventListener("DOMContentLoaded", function () {
    console.log("register-toggle.js loaded");

    const roleField = document.getElementById("id_role");
    const diplomaNumberWrapper = document.getElementById("div_id_diploma_number");
    const diplomaDateWrapper = document.getElementById("div_id_diploma_issue_date");

    if (!roleField || !diplomaNumberWrapper || !diplomaDateWrapper) {
        console.warn("⚠️ Required fields not found in DOM.");
        return;
    }

    function toggleDiplomaFields() {
        const isDoctor = roleField.value === "doctor";
        console.log("Selected role:", roleField.value);

        if (isDoctor) {
            diplomaNumberWrapper.classList.remove("d-none");
            diplomaDateWrapper.classList.remove("d-none");
        } else {
            diplomaNumberWrapper.classList.add("d-none");
            diplomaDateWrapper.classList.add("d-none");
        }
    }

    roleField.addEventListener("change", toggleDiplomaFields);
    toggleDiplomaFields();
});
