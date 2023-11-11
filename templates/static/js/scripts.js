(() => {
    const forms = document.getElementsByClassName("form-delete")

    if (forms) {
        for (const form of forms) {
            form.addEventListener("submit", function (e) {
                e.preventDefault()

                const confirmed = confirm("Do you really want to do that?")

                if (confirmed) {
                    form.submit()
                }
            })
        }
    }

})()