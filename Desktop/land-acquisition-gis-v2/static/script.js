// =========================================
// PAGE NAVIGATION
// =========================================

function showPage(pageId, button) {

    const pages =
        document.querySelectorAll(".page");

    pages.forEach(
        function(page) {

            page.classList.remove(
                "active-page"
            );

        }
    );


    const target =
        document.getElementById(pageId);


    if (target) {

        target.classList.add(
            "active-page"
        );

    }


    const buttons =
        document.querySelectorAll(
            ".nav-item"
        );


    buttons.forEach(
        function(btn) {

            btn.classList.remove(
                "active"
            );

        }
    );


    if (button) {

        button.classList.add(
            "active"
        );

    }


    window.scrollTo(
        {
            top: 0,
            behavior: "smooth"
        }
    );

}


// =========================================
// OPEN PAGE WITHOUT BUTTON
// =========================================

function showPageByName(pageId) {

    const targetButton =
        Array.from(
            document.querySelectorAll(
                ".nav-item"
            )
        ).find(
            function(button) {

                return button
                    .getAttribute("onclick")
                    ?.includes(
                        "'" + pageId + "'"
                    );

            }
        );


    showPage(
        pageId,
        targetButton
    );

}


// =========================================
// PROJECT SEARCH
// =========================================

function filterProjects() {

    const searchInput =
        document.getElementById(
            "projectSearch"
        );


    const query =
        searchInput.value
            .toLowerCase()
            .trim();


    const rows =
        document.querySelectorAll(
            "#projectTable tbody tr"
        );


    rows.forEach(
        function(row) {

            const text =
                row.innerText.toLowerCase();


            if (
                text.includes(query)
            ) {

                row.style.display = "";

            } else {

                row.style.display = "none";

            }

        }
    );

}


// =========================================
// AI PREDICTION
// =========================================

async function runPrediction() {


    const payload = {

        project_id:
            document.getElementById(
                "predictionProject"
            ).value,


        possession:
            Number(
                document.getElementById(
                    "possession"
                ).value
            ),


        land_acquired:
            Number(
                document.getElementById(
                    "land_acquired"
                ).value
            ),


        pending_approvals:
            Number(
                document.getElementById(
                    "pending_approvals"
                ).value
            ),


        compensation_pending:
            Number(
                document.getElementById(
                    "compensation_pending"
                ).value
            ),


        legal_cases:
            Number(
                document.getElementById(
                    "legal_cases"
                ).value
            ),


        affected_families:
            Number(
                document.getElementById(
                    "affected_families"
                ).value
            ),


        rr_completed:
            Number(
                document.getElementById(
                    "rr_completed"
                ).value
            ),


        planned_duration:
            Number(
                document.getElementById(
                    "planned_duration"
                ).value
            ),


        environmental:
            Number(
                document.getElementById(
                    "environmental"
                ).value
            ),


        forest:
            Number(
                document.getElementById(
                    "forest"
                ).value
            )

    };


    try {


        const response =
            await fetch(
                "/api/predict",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )

                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            alert(
                result.error ||
                "Prediction failed."
            );

            return;

        }


        document
            .getElementById(
                "predictionResult"
            )
            .classList.remove(
                "hidden"
            );


        document.getElementById(
            "predictedDelay"
        ).innerText =
            result.predicted_delay
                .toFixed(1)
            + " days";


        document.getElementById(
            "predictedRisk"
        ).innerText =
            result.risk;


        document.getElementById(
            "currentDelay"
        ).innerText =
            result.current_delay
                .toFixed(1)
            + " days";


        document.getElementById(
            "recommendation"
        ).innerText =
            result.recommendation;


    }
    catch (error) {

        console.error(error);


        alert(
            "Prediction server unavailable."
        );

    }

}