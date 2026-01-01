document.addEventListener("DOMContentLoaded", () => {

    const predictBtn = document.getElementById("predict-btn");
    const resultBox = document.getElementById("result");

    predictBtn.addEventListener("click", async () => {

        const bhk = document.getElementById("bhk").value;
        const size = document.getElementById("size").value;
        const bathroom = document.getElementById("bathroom").value;
        const floor = document.getElementById("floor").value;
        const area_type = document.getElementById("area_type").value;
        const area_locality = document.getElementById("area_locality").value;
        const city = document.getElementById("city").value;
        const furnishing = document.getElementById("furnishing").value;

        // basic validation
        if (!bhk || !size || !bathroom || !city) {
            resultBox.innerText = "⚠️ Please fill all required fields";
            return;
        }

        const payload = {
            bhk: bhk,
            size: size,
            bathroom: bathroom,
            floor: floor,
            area_type: area_type,
            area_locality: area_locality,
            city: city,
            furnishing: furnishing
        };

        resultBox.innerText = "⏳ Predicting rent...";

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const text = await response.text();   // safer than response.json()
            const data = JSON.parse(text);

            if (data.prediction) {
                resultBox.innerText = `💰 Predicted Rent: ₹ ${data.prediction}`;
            } else if (data.error) {
                resultBox.innerText = `❌ ${data.error}`;
            } else {
                resultBox.innerText = "❌ Unexpected response from server";
            }

        } catch (err) {
            console.error(err);
            resultBox.innerText = "❌ Server error. Check Flask terminal.";
        }
    });
});
