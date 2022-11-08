$(document).ready(function () {
    let order_summery = {
        amt_id: '',
        amt: '',
        pm_id: '',
        pm: '',
        pte: '',
    }

    function formatToPHP(number) {
        let php_curr = new Intl.NumberFormat('fil-PH', { style: 'currency', currency: 'PHP' }).format(number);
        return php_curr;
    }
    function load_order_summary(data) {
        let os = $("#order-summary");
        os.find('#pm').text(data.pm);
        os.find('#stotal').text(formatToPHP(data.amt));
        os.find('#total').text(formatToPHP(data.amt));
        os.find('#points_earn_total').text(data.pte);
    }

    $("#card-game-amount .game-item").on("click", function (e) {
        let url = $(this).data('url');

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

            },
            success: (data) => {

                $(this).closest('.game-amount-container').find(".game-item").removeClass("active")
                $(this).addClass("active");

                order_summery = { ...order_summery, ...data }

            },
            complete: (data) => {
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toastr.error(thrownError + '\n' + xhr.status + '\n' + ajaxOptions);
            }
        }).done(function (data) {
            load_order_summary(order_summery)
        });

    })
    $("#card-game-payment .game-item").on("click", function (e) {
        let url = $(this).data('url');
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

            },
            success: (data) => {

                $(this).closest('.game-amount-container').find(".game-item").removeClass("active")
                $(this).addClass("active");

                order_summery = { ...order_summery, ...data }

            },
            complete: (data) => {
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toastr.error(thrownError + '\n' + xhr.status + '\n' + ajaxOptions);
            }
        }).done(function (data) {
            load_order_summary(order_summery)
        });

    });

    $("#btn-checkout").on("click", function (e) {
        e.preventDefault();
        let billingForm = $("#billing-form");
        let button = $(this);
        billingForm.validate({
            ignore: [], // ? ignore NOTHING specially on bootstrap tabs
            submitHandler: function (form) {

                let formData = new FormData(form);

                if (!order_summery.pm_id) {
                    toastr.error('Please select a payment method!');
                    return;
                }
                if (!order_summery.amt_id) {
                    toastr.error('Please select a credit amount!');
                    return;
                }

                formData.append('pm_id', order_summery.pm_id);
                formData.append('amt_id', order_summery.amt_id);
                //  Display the key/value pairs 
                // for (var pair of formData.entries()) {
                //     console.log(pair[0] + ', ' + pair[1]);
                // }

                $.ajax({
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    // url: url,
                    cache: false,
                    contentType: false,
                    processData: false,
                    type: "POST",
                    data: formData,
                    dataType: 'json',
                    beforeSend: (data) => {
                        button.prop("disabled", true);
                    },
                    success: (data) => {
                        if (data.is_valid) {
                            Swal.fire(
                                {
                                    title: 'Checkout Success',
                                    icon: 'info',
                                    html: `
                                        <p>Please check your <b class="text-info text-uppercase">transactions list</b> and pay the amount on the transaction item.</p>
                                        <p>Once the payment is done properly, Please click the <b class="text-warning text-uppercase">send mail verification</b> to view your transaction details and the <b class="text-capitalize text-success">game credit, 
                                        piconde and serial number</b></p>`,
                                    allowOutsideClick: false,
                                    confirmButtonColor: '#44D62C',
                                    confirmButtonText: 'Continue'
                                }

                            ).then((result) => {
                                if (result.isConfirmed) {
                                    window.location.replace('/')
                                }
                            })

                        } else {
                            // data.errors.forEach((currentValue, index) => {
                            //     toastr.error(`${currentValue.value}`, `${currentValue.field}`)
                            // })
                        }

                    },
                    error: (data) => {
                        toastr.error("There was an error on saving your data.", "Error")
                    },
                    complete: (data) => {
                        button.prop("disabled", false);
                    }
                });

            },
            invalidHandler: function (form, validator) {
                var errors = validator.numberOfInvalids();
                if (errors) {

                    // if (validator.errorList.length > 0) {
                    //   for (x = 0; x < validator.errorList.length; x++) {
                    //     errors += validator.errorList[x].message;
                    //   }
                    // }
                    toastr.error("Please provide the required details in the form", "Incomplete data")
                }
            },

            rules: {
                email: {
                    required: true,
                    minlength: 5
                },
                contact: {
                    required: true,
                    minlength: 11
                },

            },

            messages: {
                email: {
                    required: "Please provide your email",
                    minlength: "Your email must be at least 5 characters long"
                },

                contact: {
                    required: "Please provide your contact #",
                    minlength: "Your contact # must be at least 11 characters long"
                },


            },
            errorElement: 'span',
            errorPlacement: function (error, element) {
                error.addClass('invalid-feedback');
                element.closest('.form-group').append(error);
            },
            highlight: function (element, errorClass, validClass) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function (element, errorClass, validClass) {
                $(element).removeClass('is-invalid');

            }
        });

        billingForm.submit();
    })



    $("input[name='toggle-email']").on("click", function(e){

        let email = $('input[name="email"]');
        let contact = $('input[name="contact"]'); 

        if($(this).is(":checked")){
            email.prop('readonly', false);
            contact.prop('readonly', false);
            email.select(); 
        }else{
            email.prop('readonly', true);
            contact.prop('readonly', true);
        }
    })
})