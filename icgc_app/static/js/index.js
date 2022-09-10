$(document).ready(function (e) {
    $("#form-search").on("submit", function (e) {
        e.preventDefault();
        let form = $(this);

        $.ajax({
            data: form.serialize(),
            cache: false,
            type: "POST",
            dataType: 'json',
            beforeSend: () => {
            },
            success: (data) => {
                $(".games-container").html(data.html_table);
                toastr.info("Filter successful!")
            },
            complete: (data) => {
            },
            error: (data) => {

            }
        });
    })

    $("#form-search input[type='search']").keyup(function (e) {
        let form = $('#form-search');
 
        if ($(this).val() === "") {
            $.ajax({
                data: form.serialize(),
                cache: false,
                type: "POST",
                dataType: 'json',
                beforeSend: () => {
                },
                success: (data) => {
                    $(".games-container").html(data.html_table);
                    toastr.info("Filter successful!")
                },
                complete: (data) => {
                },
                error: (data) => {

                }
            });
        }

    });
})