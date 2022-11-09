$(document).ready(function (e){
    $('[data-toggle="tooltip"]').tooltip();
    $(".select2").select2();
    $("table tbody").on("click", ".btn-cc", function (e) {


        let id = $(this).siblings('span').text();
        navigator.clipboard.writeText(id).then(() => {
            // Alert the user that the action took place.
            // Nobody likes hidden stuff being done under the hood!
            toastr.info("Copied to clipboard")
        });
    });

    const default_selected = $(".form-group.transaction-date-container").data('value'); 
    if(default_selected){
        $(`input[value='${default_selected}']`).prop('checked', true);
    }   

 
    $("#months").val($("#months").data('value')).trigger('change');
    $("#years").val($("#years").data('value')).trigger('change');

    function formatToPHP(number) {
        let php_curr = new Intl.NumberFormat('fil-PH', { style: 'currency', currency: 'PHP' }).format(number);
        return php_curr;
    }


    function getDateAndTime(isoDate) {
        let d = new Date(isoDate);
        return d

    }

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
                      
                        } else {
                            toastr.error("There's an error upon deleting this transaction!")
                        }
                    },
                    complete: (data) => {
                    },
                    error: (data) => {

                    }
                }).done((data) => {
                    window.location.reload();
                });

            }
        })
    })
})