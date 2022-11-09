$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    // NOTE: https://stackabuse.com/how-to-copy-to-clipboard-in-javascript-with-the-clipboard-api/


    let qrcode_settings = {
        text: '',
        width: 220,
        height: 220,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    }



    function formatToPHP(number) {
        let php_curr = new Intl.NumberFormat('fil-PH', { style: 'currency', currency: 'PHP' }).format(number);
        return php_curr;
    }


    function getDateAndTime(isoDate) {
        let d = new Date(isoDate);
        return d

    }
    $("table tbody").on("click", ".btn-cc", function (e) {


        let id = $(this).siblings('span').text();
        navigator.clipboard.writeText(id).then(() => {
            // Alert the user that the action took place.
            // Nobody likes hidden stuff being done under the hood!
            toastr.info("Copied to clipboard")
        });
    });

    $("table tbody").on('click', "button.btn-check-status", function (e) {
        let url = $(this).data('url');
        let button = $(this);
        $.ajax({
            // https://docs.djangoproject.com/en/2.2/ref/csrf/
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            url: url,
            type: "POST",
            mode: 'same-origin', // Do not send CSRF token to another domain. 
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function () {
                button.prop('disabled', true);

                toastr.info("Please wait, your transaction is being loaded!")
                $('[data-toggle="tooltip"]').tooltip("hide");
            },
            success: (data) => {
                if (data.is_valid) {
                    toastr.success("Transaction status has been successfully loaded!")
                    let response = JSON.parse(data.response)


                    let items = response.basket.reduce((previousValue, currentValue) => (
                        previousValue + `<tr> 
                            <td>Category: ${currentValue.category}</td>
                            <td>Price: ${formatToPHP(currentValue.price)}</td>
                            <td>Qty: ${currentValue.quantity}</td>
                            <td>Name: ${currentValue.name}</td>
                            <td>Type: ${currentValue.type}</td>
                            <td>Buyer: ${currentValue.metadata.buyer}</td>
                        </tr>`
                    ), "")

                    let m = $("#modal-xl").modal("show").find(".modal-content").html(`
                        <div class="modal-header p-3">
                            <h5 class="modal-title">Transaction Status</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div  class="modal-body table-responsive p-0" style="min-height: calc(100vh - 200px);">
                            <table class="table table-bordered">
                        
                                <tbody>
                                    <tr>
                                        <td>Items Details</td>
                                        <td>
                                        <table class="table table-bordered p-0 m-0">
                                            <tbody>
                                                ${items}
                                            </tbody>
                                        </table>
                                        </td>
                                    </tr>
                            
                                    <tr>
                                        <td>Status</td>
                                        <td>${response.status.toLowerCase() === 'SUCCEEDED'.toLowerCase() ? 'Success'.toLocaleUpperCase() : response.status}</td> 
                                    </tr>
                                    <tr>
                                        <td>Currency</td>
                                        <td>${response.currency}</td>
                                    </tr>
                                    <tr>
                                        <td>Charge Amount</td>
                                        <td>${formatToPHP(response.charge_amount)}</td>
                                    </tr>
                                    <tr>
                                        <td>Capture Amount</td>
                                        <td>${formatToPHP(response.capture_amount)}</td>
                                    </tr>
                                    <tr>
                                        <td>Payment</td>
                                        <td>
                                        <table class="table table-bordered p-0 m-0">
                                            <tbody>
                                            
                                                <tr>
                                                        ${
                                                            response.actions.desktop_web_checkout_url ? `
                                                        <td>
                                                            <a href="${response.actions.desktop_web_checkout_url}" target="_blank" class="btn bg-gradient-success btn-block">
                                                                <i class="fas fa-desktop mr-1"></i>
                                                                Pay Desktop URL
                                                            </a> 
                                                        </td>
                                                            `: `` 
                                                        }
                                                        ${
                                                            response.actions.mobile_deeplink_checkout_url ? 
                                                            `
                                                            <td>
                                                                <a href="${response.actions.mobile_deeplink_checkout_url}" target="_blank" class="btn bg-gradient-primary btn-block">
                                                                <i class="fas fa-mobile-alt mr-1"></i>
                                                                    Pay Mobile URL 
                                                                </a>
                                                            </td>
                                                            `
                                                            : 
                                                            ''
                                                        }
                                                   
                                                </tr>
                                            </tbody>
                                        </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Created</td>
                                        <td>${getDateAndTime(response.created)}</td>
                                    </tr>
                                    <tr>
                                        <td>Updated</td>
                                        <td>${getDateAndTime(response.updated)}</td>
                                    </tr>
                                </tbody>

                            </table>
                        </div>   
                    `);

                    // new QRCode(m.find("#qr_code_desktop")[0], { ...qrcode_settings, text: response.actions.desktop_web_checkout_url });
                    // new QRCode(m.find("#qr_code_mobile")[0], { ...qrcode_settings, text: response.actions.desktop_web_checkout_url });


                }else{
                    toastr.error(data.error)
                }
            },
            complete: (data) => {
                button.prop('disabled', false);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toastr.error(thrownError + '\n' + xhr.status + '\n' + ajaxOptions);
            }
        })
    });

    $("table tbody").on('click', "button.btn-send-mail", function (e) {
        let url = $(this).data('url');
        let button = $(this);

        Swal.fire({
            title: 'Are you sure?',
            html: `Do you want to <b class="text-success">Retrieve purchase details of the game you bought</b>  <b class="text-warning"> through E-mail?</b>`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3C92B3',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Please send it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    // https://docs.djangoproject.com/en/2.2/ref/csrf/
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    url: url,
                    type: "POST",
                    mode: 'same-origin', // Do not send CSRF token to another domain. 
                    cache: false,
                    processData: false,
                    contentType: false,
                    beforeSend: function () {
                        button.prop('disabled', true);
                        toastr.info("Please wait, your transaction is being loaded!");
                        $('[data-toggle="tooltip"]').tooltip("hide");
                    },
                    success: (data) => {
                        if (data.is_valid) {
                            Swal.fire(
                                'Email has been sent!',
                                'We have sen\'t the game details and purchase info of the product you bought through your mail.',
                                'success'
                            )
                        } else {
                            Swal.fire(
                                'Unpaid/Voided/Refunded/Failed Transaction',
                                'Please pay the bills on this transaction before you can retrieve the game details you bought!',
                                'error'
                            )
                        }
                    },
                    complete: (data) => {
                        button.prop('disabled', false);
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        toastr.error(thrownError + '\n' + xhr.status + '\n' + ajaxOptions);
                    }
                })
            }
        })

    });

    $("table tbody").on('click', 'button.delete', function (e) {
        let url = $(this).data("url");

        Swal.fire({
            title: 'Are you sure?',
            html: `Do you want to <b class="text-success">Delete</b> this <b class="text-danger">Transction?</b>`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3C92B3',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    url: url,
                    cache: false,
                    type: "POST",
                    dataType: 'json',
                    beforeSend: () => {
                    },
                    success: (data) => {
                        if (data.is_valid) {
                            Swal.fire(
                                'Success!',
                                'Transaction been successfully deleted!',
                                'success'
                            );
                            $("table tbody")
                                .html(data.html_table)
                                .find('[data-toggle="tooltip"]').tooltip();
                        } else {
                            toastr.error("There's an error upon deleting this transaction!")
                        }
                    },
                    complete: (data) => {
                    },
                    error: (data) => {

                    }
                });

            }
        })
    })

    $("table tbody").on('click', 'button.void', function (e) {
        let url = $(this).data("url");

        Swal.fire({
            title: 'Are you sure?',
            html: `Do you want to <b class="text-success">Void</b> this <b class="text-danger">Transction?</b>`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3C92B3',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Void it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    url: url,
                    cache: false,
                    type: "POST",
                    dataType: 'json',
                    beforeSend: () => {
                    },
                    success: (data) => {

                        if (data.is_valid) {
                            Swal.fire(
                                'Success',
                                'Transaction has been successfully voided!',
                                'success'
                            )
                        } else {
                            let response = JSON.parse(data.response);
                            Swal.fire(
                                response.error_code,
                                response.message,
                                'error'
                            )
                        }
                    },
                    complete: (data) => {
                    },
                    error: (data) => {

                    }
                });

            }
        })
    })

    $("table tbody").on('click', 'button.refund', function (e) {
        let url = $(this).data("url");

        Swal.fire({
            title: 'Are you sure?',
            html: `Do you want to <b class="text-success">Refund</b> this <b class="text-danger">Transction?</b>`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3C92B3',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Refund it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    url: url,
                    cache: false,
                    type: "POST",
                    dataType: 'json',
                    beforeSend: () => {
                    },
                    success: (data) => {

                        if (data.is_valid) {
                            Swal.fire(
                                'Success',
                                'Transaction has been successfully refunded!',
                                'success'
                            )
                        } else {
                            let response = JSON.parse(data.response);
                            Swal.fire(
                                response.error_code,
                                response.message,
                                'error'
                            )
                        }
                    },
                    complete: (data) => {
                    },
                    error: (data) => {

                    }
                });

            }
        })
    })

    $("table tbody").on('click', 'button.list-refund', function (e) {
        let url = $(this).data("url");

        Swal.fire({
            title: 'Are you sure?',
            html: `Do you want to show the <b class="text-success">List Refund</b> this <b class="text-warning">Transction?</b>`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3C92B3',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Show the list of refunds!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    url: url,
                    cache: false,
                    type: "POST",
                    dataType: 'json',
                    beforeSend: () => {
                    },
                    success: (data) => {

                        let response = JSON.parse(data.response);

                        if (data.is_valid) {

                            let items = response.data.reduce((previousValue, currentValue) => (
                                previousValue + `<tr> 
                                    <td>${currentValue.status}</td>
                                    <td>${currentValue.currency}</td>
                                    <td>${formatToPHP(currentValue.capture_amount)}</td>
                                    <td>${formatToPHP(currentValue.refund_amount)}</td> 
                                    <td>${getDateAndTime(currentValue.created)}</td>
                                    <td>${getDateAndTime(currentValue.updated)}</td>
                                </tr>`
                            ), "")
                            $("#modal-xl").modal("show").find(".modal-content").html(`
                                <div class="modal-header p-3">
                                    <h5 class="modal-title">Transaction Status</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div  class="modal-body table-responsive p-0" style="min-height: calc(100vh - 200px);">
                                    <table class="table table-bordered">
                                        <thead>
                                            <tr>
                                                <th>Status</th>
                                                <th>Currency</th>
                                                <th>Capture Amount</th>
                                                <th>Refund Amount</th>
                                                <th>Created</th>
                                                <th>Updated</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${items}
                                        </tbody>
                                    </table>
                                </div>   
                            `);

                        } else {

                            Swal.fire(
                                response.error_code,
                                response.message,
                                'error'
                            )
                        }
                    },
                    complete: (data) => {
                    },
                    error: (data) => {

                    }
                });

            }
        })
    })

    $("input[type='search']").on('search', function () {
        let form = $(this);
        $.ajax({
            data: form.serialize(),
            cache: false,
            type: "POST",
            dataType: 'json',
            beforeSend: () => {
            },
            success: (data) => {
                $("table tbody").html(data.html_table).find('[data-toggle="tooltip"]').tooltip();
                toastr.info("Filter successful!")
            },
            complete: (data) => {
            },
            error: (data) => {

            }
        });
    });

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
                    $("table tbody").html(data.html_table).find('[data-toggle="tooltip"]').tooltip();
                    toastr.info("Filter successful!")
                },
                complete: (data) => {
                },
                error: (data) => {

                }
            });
        }

    });

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
                $("table tbody").html(data.html_table).find('[data-toggle="tooltip"]').tooltip();
                toastr.info("Filter successful!")
            },
            complete: (data) => {
            },
            error: (data) => {

            }
        });
    })



})